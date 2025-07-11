import re
from benchmark import Benchmarker
from dataclasses import dataclass

includeRegex = re.compile(r"#include[^\n]*")
commentRegex = re.compile(r"\/\/[^\n]*")


def stripComments(s: str) -> str:
    return re.sub(commentRegex, "", s)


@dataclass
class CodeBlock:
    start: int
    end: int
    bodyStart: int
    bodyEnd: int


def extractBlock(code: str, blockPreamble: str) -> CodeBlock:
    blockStart = code.find(blockPreamble)
    if blockStart < 0:
        return CodeBlock(0, 0, 0, 0)
    else:
        subs = code[blockStart:]

    bodyStart = blockStart
    bodyEnd = blockStart
    depth = 0
    for char in subs:
        if depth == 0:
            bodyStart += 1

        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                break

        bodyEnd += 1

    return CodeBlock(
        start=blockStart,
        end=bodyEnd + 1,
        bodyStart=bodyStart,
        bodyEnd=bodyEnd,
    )


def extract(code: str) -> Benchmarker.Code:
    includes = [s.strip() for s in re.findall(includeRegex, code)]

    mainInfo = extractBlock(code, blockPreamble="int main")

    mainBody = code[mainInfo.bodyStart : mainInfo.bodyEnd]
    mainBody = mainBody.replace("return 0;", "")
    mainBody = mainBody.strip()

    codeStripped = code[: mainInfo.start] + code[mainInfo.end :]
    codeStripped = re.sub(includeRegex, "", codeStripped)
    additionalDefs = codeStripped.strip()

    return Benchmarker.Code(
        includes=includes,
        additionalDefs=additionalDefs,
        body=mainBody,
    )
