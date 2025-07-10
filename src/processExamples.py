import re
from utils import DB, starmap, Example, BenchmarkResult, TestInfo
import codeProcessing
from benchmark import Benchmarker
from typing import Iterator
from dataclasses import asdict
import random
import json

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


#### Extraction
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




#### Benchmarking
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
    benchmarks = DB.getCollection(DB.benchmarks)

    for example in getExamplesSorted():
        print("\r", end="")
        print(f"Benchmarking example {example._key}", end="")
        benchResultSlow = runBenchmark(
            benchmarker,
            f"{DB.examples}/{example._key}.codeSlow",
            example.codeSlow,
        )
        benchResultSlow.insertInto(benchmarks)

        benchResultFast = runBenchmark(
            benchmarker,
            f"{DB.examples}/{example._key}.codeFast",
            example.codeFast,
        )
        benchResultFast.insertInto(benchmarks)

    print("\nDone")

#### Testing
namespaceTemplate = """\
namespace {namespaceName} {{
    {namespaceBody}
}}
"""

codeTemplate = """\
// Task {exampleNumber}
{{
    {usingStatement}
    {codeBody}
}}
"""

testTeamplate = """\
{includes}

{additionalDefs}

int main () {{
    {mainBody}
}}
"""

def renderTest(testTasks: list[Benchmarker.Code]):
    includes = set((
        include
        for code in testTasks
            for include in code.includes
    ))

    def renderCode(exampleNumber: int, code : Benchmarker.Code):
        namespace = None
        if code.additionalDefs:
            namespace = namespaceTemplate.format(
                namespaceName=f"task{exampleNumber}",
                namespaceBody=code.additionalDefs
            )
        
        codeStr = codeTemplate.format(
            exampleNumber = exampleNumber,
            usingStatement = (
                f"using namespace task{exampleNumber};" 
                if namespace is not None else ""
            ),
            codeBody = code.body
        )

        return (namespace, codeStr)
    
    (namespaces, codeBlocks) = zip(
        *starmap(
            renderCode, 
            enumerate(testTasks, start=1)
        )
    )

    return testTeamplate.format(
        includes = "\n".join(includes),
        additionalDefs = "\n".join(filter(
            lambda namespace: namespace is not None,
            namespaces
        )),
        mainBody = "\n\n".join(codeBlocks)
    )

def makeTests():
    random.seed(123)
    
    testTasks1 : list[Benchmarker.Code] = []
    testInfo1 = TestInfo(testFile="main1.cpp")
    
    testTasks2 : list[Benchmarker.Code] = []
    testInfo2 = TestInfo(testFile="main2.cpp")

    choices = ["codeSlow", "codeFast"]
    
    for i, example in enumerate(getExamplesSorted(), start=1):
        assert str(i) == example._key
        choice1 = random.binomialvariate(n=1, p=0.5)
        choice2 = int(not choice1)
        
        testInfo1.choices.append(choice1)
        code = getattr(example, choices[choice1])
        testTasks1.append(codeProcessing.extract(codeProcessing.stripComments(code)))
        
        testInfo2.choices.append(choice2)
        code = getattr(example, choices[choice2])
        testTasks2.append(codeProcessing.extract(codeProcessing.stripComments(code)))

    with open("main1.cpp", "w") as f: f.write(renderTest(testTasks1))
    with open("info1.json", "w") as f: json.dump(asdict(testInfo1), f)
    
    with open("main2.cpp", "w") as f: f.write(renderTest(testTasks2))
    with open("info2.json", "w") as f: json.dump(asdict(testInfo2), f)
    
if __name__ == "__main__":
    makeTests()
