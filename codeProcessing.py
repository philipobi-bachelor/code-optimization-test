from pydantic import BaseModel
import re
from benchmark import Benchmarker

includeRegex = re.compile(r"#include[^\n]*")
commentRegex = re.compile(r"\/\/[^\n]*")


def stripComments(s: str) -> str:
    return re.sub(commentRegex, "", s)


class FuncRange(BaseModel):
    funcStart: int
    funcEnd: int
    bodyStart: int
    bodyEnd: int


def findMainBody(code: str) -> FuncRange:
    funcStart = code.find("int main")
    if funcStart < 0:
        return ""
    else:
        subs = code[funcStart:]

    bodyStart = funcStart
    bodyEnd = funcStart
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

    return FuncRange(
        funcStart=funcStart,
        funcEnd=bodyEnd + 1,
        bodyStart=bodyStart,
        bodyEnd=bodyEnd,
    )


def extract(code: str) -> Benchmarker.Code:
    includes = [s.strip() for s in re.findall(includeRegex, code)]

    mainInfo = findMainBody(code)

    mainBody = code[mainInfo.bodyStart : mainInfo.bodyEnd]
    mainBody = mainBody.replace("return 0;", "")
    mainBody = mainBody.strip()

    codeStripped = code[: mainInfo.funcStart] + code[mainInfo.funcEnd :]
    codeStripped = re.sub(includeRegex, "", codeStripped)
    additionalDefs = codeStripped.strip()

    return Benchmarker.Code(
        includes=includes,
        additionalDefs=additionalDefs,
        body=mainBody,
    )
