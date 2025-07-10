import re
from utils import DB, starmap, Example, BenchmarkResult
import codeProcessing
from benchmark import Benchmarker
from typing import Iterator
from dataclasses import asdict

exampleRegex = re.compile(
    r"## Example \d+: (?P<title>[^\n]*)\s*"
    r"```cpp\s*(?P<codeSlow>[^`]*)```\s*"
    r"```cpp\s*(?P<codeFast>[^`]*)```\s*"
    r"Description: (?P<description>[^\n]*)\s*",
    flags=re.DOTALL,
)


def extractExamples(path: str) -> Iterator[Example]:
    with open(path, "r") as f:
        fileContent = f.read()

    return starmap(
        lambda i, match: Example(
            _key=str(i),
            title=match.group("title"),
            description=match.group("description"),
            codeSlow=match.group("codeSlow"),
            codeFast=match.group("codeFast"),
        ),
        enumerate(exampleRegex.finditer(fileContent), start=1),
    )


def insertExamples(examples: Iterator[Example]):
    DB.getCollection(DB.examples).import_bulk(
        documents=list((asdict(example) for example in examples)),
        on_duplicate="replace",
    )


def getExamplesSorted() -> Iterator[Example]:
    query = (
        f"for example in `{DB.examples}` "
        "sort to_number(example._key) asc "
        'return unset(example, "_id", "_rev")'
    )
    
    return map(
        lambda doc: Example(**doc),
        DB.get().aql.execute(query),
    )


def runBenchmark(
    benchmarker: Benchmarker,
    filename: str,
    code: str,
) -> BenchmarkResult:
    codeExtracted = codeProcessing.extract(code)
    benchmarkCode = benchmarker.renderTemplate(codeExtracted)
    output = benchmarker.run(benchmarkCode, stdout=False)

    return BenchmarkResult.create(
        filename=filename,
        code=code,
        benchmarkCode=benchmarkCode,
        output=output,
    )


def benchmarkExamples():
    benchmarker = Benchmarker()

    benchResults: list[dict] = []

    for example in getExamplesSorted():
        print("\r", end="")
        print(f"Benchmarking example {example._key}", end="")
        benchResultSlow = runBenchmark(
            benchmarker,
            f"{DB.examples}/{example._key}.codeSlow",
            example.codeSlow,
        )

        benchResultFast = runBenchmark(
            benchmarker,
            f"{DB.examples}/{example._key}.codeFast",
            example.codeFast,
        )

        benchResults.append(benchResultSlow.toDBDoc())
        benchResults.append(benchResultFast.toDBDoc())

    DB.getCollection(DB.benchmarks).import_bulk(benchResults, on_duplicate="replace")

    print("\nDone")


if __name__ == "__main__":
    insertExamples(extractExamples("examples.md"))
