import re
from pathlib import PosixPath as Path
from codeProcessing import extractBlock, includeRegex
from benchmark import Benchmarker
from utils import BenchmarkResult, DB

#### Benchmark agent code and write results to db
fullDiffRegex = re.compile(
    r"Edited Files:.*?main\d.cpp.*?Squashed changes \(full\).*?```diff\s*(?P<fullDiff>.*?)(?=```)",
    flags=re.DOTALL,
)


def fullDiffToFile(fullDiff: str) -> str:
    return "\n".join(
        map(
            lambda line: line[1:],
            filter(
                lambda line: not (line[:3] in ("+++", "---", "@@ ") or line[:1] == "-"),
                fullDiff.split("\n"),
            ),
        )
    )


def restoreAgentEdits(chatLog: Path) -> str:
    with Path.open(chatLog, "r") as f:
        [match] = re.finditer(fullDiffRegex, f.read())
    fullDiff = match.group("fullDiff")
    return fullDiffToFile(fullDiff)


taskTemplate = """\
{includes}

{additionalDefs}

{task}
"""

namespaceRegex = re.compile(r"using namespace.*?\n")

def benchmarkTasks(benchmarker: Benchmarker, code: str, filenameStem: str):
    includes = [s.strip() for s in re.findall(includeRegex, code)]

    for taskNum in range(1, 51):
        print("\r", end="")
        print(f"Benchmarking task {taskNum} of 50", end="")

        namespaceBlock = extractBlock(code, blockPreamble=f"namespace task{taskNum} ")
        taskBlock = extractBlock(code, blockPreamble=f"// Task {taskNum}\n")

        body = code[taskBlock.bodyStart : taskBlock.bodyEnd]
        body = re.sub(namespaceRegex, '', body)

        benchmarkCode = benchmarker.renderTemplate(
            Benchmarker.Code(
                includes=includes,
                additionalDefs=code[namespaceBlock.bodyStart : namespaceBlock.bodyEnd],
                body=body,
            )
        )

        output = benchmarker.run(benchmarkCode, stdout=False)

        yield BenchmarkResult.create(
            filename=f"{filenameStem}.task{taskNum}",
            code=taskTemplate.format(
                includes="\n".join(includes),
                additionalDefs=code[namespaceBlock.start : namespaceBlock.end],
                task=code[taskBlock.start : taskBlock.end],
            ),
            benchmarkCode=benchmarkCode,
            output=output,
        )

    print("\nDone")


def benchmarkAgentEdits():
    benchmarker = Benchmarker()
    benchmarks = DB.getCollection(DB.benchmarks)

    logsDir = Path("chat-logs")
    for i in (1, 2):
        test = f"test{i}"
        for chatLog in filter(
            lambda path: path.is_file(),
            Path.iterdir(logsDir / test),
        ):
            modelName = chatLog.stem
            filenameStem = f"{test}.{modelName}"

            print(f"Benchmarking {filenameStem}")

            code = restoreAgentEdits(chatLog)
            for benchResult in benchmarkTasks(
                benchmarker=benchmarker,
                code=code,
                filenameStem=filenameStem,
            ):
                benchResult.insertInto(benchmarks)

if __name__ == "__main__":
    benchmarkAgentEdits()
