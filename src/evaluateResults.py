import json
import re
from IPython.display import display, Markdown, clear_output
from utils import getExamplesSorted, Example, DB, starmap
from processResults import fullDiffRegex
from pathlib import PosixPath as Path
from typing import Literal, Iterator
import pandas as pd
import numpy as np
from dataclasses import dataclass
from pint import UnitRegistry

"""
Helper code to review the edits the agent made to the test file

# Usage:
# modified: y / n
# improved: y / n

output = {}
it = evaluateResult(testNum=2, model="o4-mini", output=output)
next(it)
...

with open("../evaluation/test2/o4-mini.json", "x") as f: json.dump(output, f)
"""

namespaceRegex = re.compile(
    r"namespace task(?P<taskNum>\d+) {.*? \/\/ namespace task\d+\s*",
    flags=re.DOTALL,
)

taskRegex = re.compile(
    r"\/\/ Task (?P<taskNum>\d+).*?(?=\s*\/\/ Task \d+|$)",
    flags=re.DOTALL,
)

reviewTemplate = """\

#### {title}
{description}

<table>
<tr>
<td>

`slow`:

```cpp
{codeSlow}
```

</td>
<td>

`agent ({version})`:

```diff
{agentDiff}
```

</td>
<td>

`fast`:

```cpp
{codeFast}
```

</td>
</tr>
</table>
"""


def prompt(msg: str, valid: tuple[str, ...]):
    while (resp := input(msg)) not in valid:
        pass
    return resp


def reviewAgentEdit(testNum: int, model: str, output: dict) -> Iterator[None]:
    with open(f"../info{testNum}.json", "r") as f:
        info = json.load(f)

    chatLogs = Path("../chat-logs")
    test = f"test{testNum}"

    with Path.open(chatLogs / test / f"{model}.md", "r") as f:
        [match] = re.finditer(fullDiffRegex, f.read())
    fullDiff = match.group("fullDiff")

    namespaces = dict()
    taskBlocks = dict()
    for match in re.finditer(namespaceRegex, fullDiff):
        taskNum = int(match.group("taskNum"))
        namespaces[taskNum] = match.group(0)
    for match in re.finditer(taskRegex, fullDiff):
        taskNum = int(match.group("taskNum"))
        taskBlocks[taskNum] = match.group(0)

    tasks = output["tasks"] = []

    def zipper() -> Iterator[tuple[int, Example, int]]:
        yield from zip(range(1, 51), getExamplesSorted(), info["choices"], strict=True)

    for taskNum, example, taskVersion in zipper():
        assert taskNum == int(example._key)

        md = reviewTemplate.format(
            title=example.title,
            description=example.description,
            codeSlow=example.codeSlow,
            codeFast=example.codeFast,
            agentDiff=f"{namespaces.get(taskNum, "")}\n\n{taskBlocks[taskNum]}",
            version="SLOW" if taskVersion == 0 else "FAST",
        )
        display(Markdown(md))
        yield
        modified = prompt("Modified?", ("y", "n"))
        if "y" in modified:
            if taskVersion == 1:
                improved = "~"  # -> agent made changes to efficient version
            else:
                improved = prompt("Improved?", ("y", "n"))
        else:
            improved = "n"
        tasks.append(dict(taskNum=taskNum, modified=modified, improved=improved))
        yield
        clear_output()


"""
Helper functions for producing the model evaluation tables
"""

N_EXAMPLES = 50


def getBenchRuntimesSorted(filenameLike: str, filenameReplace: str) -> list[float]:
    def fetch() -> Iterator[float]:
        query = (
            f"for bench in {DB.benchmarks}",
            f'  filter bench.filename like "{filenameLike}"',
            f'  let exampleNum = to_number(regex_replace(bench.filename, "{filenameReplace}", ""))',
            "  sort exampleNum asc",
            """
            return {
            "exampleNum" : exampleNum, 
            "runtimeAvg" : bench.runtimeAvg, 
            }
            """,
        )
        for exampleNum, benchDoc in enumerate(
            DB.get().aql.execute("\n".join(query)), start=1
        ):
            assert exampleNum == benchDoc["exampleNum"]
            yield benchDoc["runtimeAvg"]

    runtimes = list(fetch())
    assert len(runtimes) == N_EXAMPLES
    return runtimes


def getExampleRuntimes(version: Literal["codeSlow", "codeFast"]) -> list[float]:
    """
    return runtimes in seconds for examples of given version
    returned runtimes are sorted by example number
    """
    return getBenchRuntimesSorted(
        filenameLike=f"%.{version}",
        filenameReplace="[^0-9]*",
    )


def getTaskRuntimes(testNum: Literal[1, 2], model: str) -> list[float]:
    """
    return runtimes in seconds for tasks in given model test
    returned runtimes are sorted by task number
    """
    return getBenchRuntimesSorted(
        filenameLike=f"test{testNum}.{model}.task%",
        filenameReplace=".*task",
    )


@dataclass
class ModelTestResults:
    improvedInfo: list[Literal["y", "n", "~"]]
    runtimes: np.ndarray


def getModelTestResults(
    testNum: Literal[1, 2],
    model: str,
) -> ModelTestResults:
    with open(f"../evaluation/test{testNum}/{model}.json", "r") as f:
        evalData = json.load(f)

    def unpack(taskNum: int, taskInfo: dict) -> Literal["y", "n", "~"]:
        assert taskInfo["taskNum"] == taskNum
        improved = taskInfo["improved"]
        assert improved in ("y", "n", "~")
        return improved

    improvedInfo = list(
        (
            unpack(taskNum, taskInfo)
            for taskNum, taskInfo in enumerate(evalData["tasks"], start=1)
        )
    )

    runtimes = np.array(
        getTaskRuntimes(
            testNum=testNum,
            model=model,
        )
    )

    return ModelTestResults(
        improvedInfo=improvedInfo,
        runtimes=runtimes,
    )


def fmtImprovement(improvement: Literal["y", "n", "~"]) -> str:
    match improvement:
        case "y":
            return r"\fullcirc"
        case "n":
            return r"\emptycirc"
        case "~":
            return r"\halfcirc"
        case _:
            raise ValueError


def trfImprovement(
    taskIsFast: Literal[0, 1],
    improvement: Literal["y", "n", "~"],
) -> str:
    cellWrapper = "%(content)s"
    if not taskIsFast:
        if improvement == "n":
            cellWrapper = r"\cellcolor{red!25}{%(content)s}"
        elif improvement == "y":
            cellWrapper = r"\cellcolor{green!25}{%(content)s}"
    return cellWrapper % dict(content=fmtImprovement(improvement))


def fmtQty(val: float) -> str:
    return r"\num{" + f"{val:.2f}" + "}"


def trfRuntimeProp(runtimeProp: float) -> str:
    cellWrapper = "%(content)s"
    if runtimeProp > 0:
        cellWrapper = r"\cellcolor{red!25}{%(content)s}"
    else:
        cellWrapper = r"\cellcolor{green!25}{%(content)s}"
    return cellWrapper % dict(content=fmtQty(runtimeProp))


def makeTestResultTable(
    testNum: int,
    root=Path.cwd(),
) -> pd.DataFrame:
    models = [
        "claude-sonnet-4",
        "gemini-2.5-pro",
        "gpt-4o",
        "o4-mini",
    ]

    with Path.open(root / "evaluation" / "titles.json", "r") as f:
        exTitles = tuple(json.load(f))
    with Path.open(root / f"info{testNum}.json", "r") as f:
        testInfo = json.load(f)
        testTaskIsFast = tuple(testInfo["choices"])

    runtimesBaseline = runtimesFast = np.array(getExampleRuntimes("codeFast"))
    runtimesSlow = np.array(getExampleRuntimes("codeSlow"))

    modelTestResults = {
        model: getModelTestResults(testNum=testNum, model=model) for model in models
    }

    def trfModelTestResults(
        model: str,
        testResults: ModelTestResults,
    ):
        trfdImprovements = list(
            starmap(
                trfImprovement,
                zip(testTaskIsFast, testResults.improvedInfo),
            )
        )

        runtimeProps = np.log10(testResults.runtimes / runtimesBaseline)
        trfdRuntimes = list(map(trfRuntimeProp, runtimeProps))

        return {
            f"test{testNum}.{model}.improved": trfdImprovements,
            f"test{testNum}.{model}.log10(rt/bl)": trfdRuntimes,
        }

    ureg = UnitRegistry()
    trfdRuntimesFast = list(
        map(
            lambda t: "{0:.1f~#Lx}".format(t * ureg.second),
            runtimesFast,
        )
    )

    colData = {
        "ex.title": exTitles,
        "ex.codeFast.rt (:= bl)": trfdRuntimesFast,
        "ex.codeSlow.log10(rt/bl)": list(
            map(fmtQty, np.log10(runtimesSlow / runtimesBaseline))
        ),
        **{
            k: v
            for d in (
                trfModelTestResults(
                    model,
                    getModelTestResults(testNum, model),
                )
                for model in models
            )
            for k, v in d.items()
        },
    }

    return pd.DataFrame(colData)
