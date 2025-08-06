import json
import re
from IPython.display import display, Markdown, clear_output
from utils import getExamplesSorted, Example, DB, starmap
from processResults import fullDiffRegex
from pathlib import PosixPath as Path
from typing import Literal, Iterator, Iterable
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

# https://www.schemecolor.com/light-red-green-gradient.php
colormapRedGreen = (
    ("cm1", -1.0, -0.7, "#B1D9A3"),
    ("cm2", -0.7, -0.4, "#CBE8BE"),
    good := ("cm3", -0.4, +0.1, "#E4F2D5"),
    ("cm4", +0.1, +0.4, "#FCF6E1"),
    bad := ("cm5", +0.4, +0.7, "#FFCCCB"),
    ("cm6", +0.7, +1.0, "#FCBABA"),
)

(good, *_) = good
(bad, *_) = bad


def getColorName(
    val: float,
    cmap: tuple[tuple[str, float, float, str]],
) -> str | None:
    result = None
    for colorName, min, max, _ in cmap:
        if val < min:
            break
        elif val > max:
            continue
        else:
            result = colorName
            break
    return result


def getBenchRuntimesSorted(
    optimized: bool,
    filenameLike: str,
    filenameReplace: str,
) -> list[float]:
    def fetch() -> Iterator[float]:
        benchmarkColl = (
            DB.benchmarksOptimized if optimized else DB.benchmarksUnoptimized
        )
        query = (
            f"for bench in `{benchmarkColl}`",
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

    runtimeData = list(fetch())
    assert len(runtimeData) == N_EXAMPLES
    return runtimeData


def getExampleRuntimes(
    version: Literal["codeSlow", "codeFast"],
    optimized: bool,
) -> list[float]:
    """
    return runtimes in seconds for examples of given version
    returned runtimes are sorted by example number
    """
    return getBenchRuntimesSorted(
        optimized=optimized,
        filenameLike=f"%.{version}",
        filenameReplace="[^0-9]*",
    )


def getTaskRuntimes(
    testNum: Literal[1, 2],
    model: str,
    optimized: bool,
) -> list[float]:
    """
    return runtimes in seconds for tasks in given model test
    returned runtimes are sorted by task number
    """
    return getBenchRuntimesSorted(
        optimized=optimized,
        filenameLike=f"test{testNum}.{model}.task%",
        filenameReplace=".*task",
    )


@dataclass
class ModelTestResult:
    improvedInfo: list[Literal["y", "n", "~"]]
    runtimes: np.ndarray


def getModelTestResult(
    testNum: Literal[1, 2],
    model: str,
    optimized: bool,
    root: Path,
) -> ModelTestResult:
    with Path.open(root / "evaluation" / f"test{testNum}/{model}.json", "r") as f:
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
            optimized=optimized,
        )
    )

    return ModelTestResult(
        improvedInfo=improvedInfo,
        runtimes=runtimes,
    )


def fmtImprovement(improvement: Literal["y", "n", "~"]) -> str:
    match improvement:
        case "y":
            return r"\fc"
        case "n":
            return r"\ec"
        case "~":
            return r"\hc"
        case _:
            raise ValueError


def fmtBool(val: bool) -> str:
    if val:
        return r"\fc"
    else:
        return r"\ec"


def trfImprovement(
    taskIsFast: Literal[0, 1],
    improvement: Literal["y", "n", "~"],
) -> str:
    cellWrapper = "%(content)s"
    colorName = ""
    if not taskIsFast:
        cellWrapper = r"\cc{%(colorName)s}{%(content)s}"
        if improvement == "n":
            colorName = bad
        elif improvement == "y":
            colorName = good
    return cellWrapper % dict(
        content=fmtImprovement(improvement),
        colorName=colorName,
    )


class Col:
    borderLeft = 0b10
    borderRight = 0b01

    def __init__(
        self,
        name: str,
        rows: Iterable[str],
        colType: str,
        borders: int | None = None,
    ):
        self.name = name
        self.rows = iter(rows)
        self.colType = colType
        self.borders = borders if borders is not None else 0b00

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.rows)


commands = r"""

\let\cc\cellcolor

\providecommand*\ec[1][1ex]{}
\providecommand*\hc[1][1ex]{}
\providecommand*\fc[1][1ex]{}

\renewcommand*\ec[1][1ex]{\adjustbox{valign=c}{\tikz\draw (0,0) circle (#1);}} 
\renewcommand*\hc[1][1ex]{%
  \adjustbox{valign=c}{\begin{tikzpicture}
  \draw[fill] (0,0)-- (90:#1) arc (90:270:#1) -- cycle ;
  \draw (0,0) circle (#1);
  \end{tikzpicture}}}
\renewcommand*\fc[1][1ex]{\adjustbox{valign=c}{\tikz\fill (0,0) circle (#1);}}

"""


class Table:
    defs = [
        r"\definecolor{%s}{HTML}{%s}" % (colorName, colorHex.lstrip("#"))
        for colorName, _, _, colorHex in colormapRedGreen
    ] + [commands]

    def __init__(
        self,
        *cols: Col,
        rowLines: bool = False,
        colLines: bool = False,
    ):
        self.cols = cols
        self.rowLines = rowLines
        self.colLines = colLines

    def lines(self) -> Iterator[str]:
        preamble = ""
        if not self.colLines:
            for colLeft, colRight in zip(self.cols[:-1], self.cols[1:]):
                sep = (
                    " | "
                    if (
                        colLeft.borders & Col.borderRight
                        | colRight.borders & Col.borderLeft
                    )
                    else " "
                )
                preamble += sep + colRight.colType
            firstCol = self.cols[0]
            lastCol = self.cols[-1]
            preamble = (
                ("| " if firstCol.borders & Col.borderLeft else "")
                + firstCol.colType
                + preamble
                + ("|" if lastCol.borders & Col.borderRight else "")
            )
        else:
            preamble = "| " + " | ".join((col.colType for col in self.cols)) + " |"

        linesep = r" \\\hline" if self.rowLines else r" \\"
        
        yield from Table.defs
        yield r"\begin{tabular}{" + preamble + "}"
        yield " & ".join((col.name for col in self.cols)) + linesep
        for rowCells in zip(*self.cols):
            yield " & ".join(rowCells) + linesep
        yield r"\end{tabular}"

    def render(self) -> str:
        return "\n".join(self.lines())


class QtyFmt:
    @staticmethod
    def fmt(val: float) -> str:
        return "{0:.1f}".format(x if (x := round(val, 1)) != 0 else 0.0)


def trfRuntimeProp(
    runtimeProp: float,
    runtimePropMapped: float,
    taskIsFast: Literal[0, 1],
) -> str:
    cellWrapper = "%(content)s"
    if taskIsFast and (-0.1 < runtimeProp and runtimeProp < 0.1):
        return QtyFmt.fmt(runtimeProp)

    colorName = getColorName(runtimePropMapped, colormapRedGreen)
    if colorName is not None:
        cellWrapper = r"\cc{%(colorName)s}{%(content)s}"
    return cellWrapper % dict(content=QtyFmt.fmt(runtimeProp), colorName=colorName)


def makeTestResultTable(
    testNum: int,
    optimized: bool,
    root: Path = Path.cwd(),
) -> tuple[Table, pd.DataFrame]:
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
        testTaskIsFastInfo = tuple(testInfo["choices"])

    runtimesBaseline = runtimesFast = np.array(
        getExampleRuntimes("codeFast", optimized=optimized)
    )
    runtimesSlow = np.array(getExampleRuntimes("codeSlow", optimized=optimized))

    modelTestResults = {
        model: getModelTestResult(
            testNum,
            model=model,
            optimized=optimized,
            root=root,
        )
        for model in models
    }

    def trfModelTestResult(
        model: str,
        testResult: ModelTestResult,
    ) -> Iterator[Col]:

        runtimeProps = np.log10(testResult.runtimes / runtimesBaseline)
        runtimePropsMapped = np.atan(runtimeProps) / (np.pi / 2)

        yield Col(
            f"test{testNum}.{model}.improved",
            starmap(
                trfImprovement,
                zip(testTaskIsFastInfo, testResult.improvedInfo),
            ),
            colType="c",
        )

        yield Col(
            f"test{testNum}.{model}.log10(rt/bl)",
            starmap(trfRuntimeProp, zip(runtimeProps, runtimePropsMapped, testTaskIsFastInfo)),
            colType="r",
        )

    ureg = UnitRegistry()
    trfdRuntimesFast = list(
        map(
            lambda t: "{0:.0f~#Lx}".format(t * ureg.second),
            runtimesFast,
        )
    )

    df = pd.DataFrame(
        {
            "ex.title": exTitles,
            "ex.codeFast.rt": runtimesFast,
            "ex.codeSlow.rt": runtimesSlow,
            f"test{testNum}.isFast": testTaskIsFastInfo,
        }
        | {
            k: v
            for d in (
                {
                    f"test{testNum}.{model}.improved": testResults.improvedInfo,
                    f"test{testNum}.{model}.rt": testResults.runtimes,
                }
                for model, testResults in modelTestResults.items()
            )
            for k, v in d.items()
        },
        index=pd.RangeIndex(start=1, stop=N_EXAMPLES + 1),
    )

    tab = Table(
        Col(
            "Example / Task",
            map(str, range(1, N_EXAMPLES + 1)),
            colType="r",
        ),
        Col("ex.title", exTitles, colType="l"),
        Col("ex.codeFast.rt (:= bl)", trfdRuntimesFast, colType="r"),
        Col(
            "ex.codeSlow.log10(rt/bl)",
            map(QtyFmt.fmt, np.log10(runtimesSlow / runtimesBaseline)),
            colType="r",
        ),
        Col(
            f"test{testNum}.task.isSlow",
            map(lambda isFast: fmtBool(not isFast), testTaskIsFastInfo),
            colType="c",
        ),
        *(
            col
            for model, testResult in modelTestResults.items()
            for col in trfModelTestResult(model, testResult)
        ),
        rowLines=True,
        colLines=True,
    )

    return (tab, df)
