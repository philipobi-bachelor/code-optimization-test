from __future__ import annotations
import json
from dataclasses import dataclass, asdict, field
from typing import Iterator
from arango.collection import StandardCollection
from arango import ArangoClient, DocumentInsertError
from benchmark import Benchmarker


starmap = lambda func, iterable: map(lambda val: func(*val), iterable)


class DB:
    examples = "code-optimization-examples"
    benchmarks = "benchmarks"

    @staticmethod
    def get():
        return ArangoClient("http://localhost:8529").db()

    @staticmethod
    def getCollection(coll):
        return DB.get().collection(coll)


@dataclass
class Example:
    _key: str
    title: str
    description: str
    codeSlow: str
    codeFast: str


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


@dataclass
class BenchmarkResult:
    code: str
    benchmarkCode: str
    output: str
    filename: str = ""
    compiled: bool = False
    executed: bool = False
    runtimeAvg: float = -1.0

    def insertInto(self, collection: StandardCollection):
        try:
            collection.insert(asdict(self), silent=True)
            return
        except DocumentInsertError as e:
            if "unique constraint violated" in str(e):
                collection.delete_match(filters=dict(filename=self.filename))
            else:
                raise
        collection.insert(asdict(self), silent=True)

    @staticmethod
    def create(
        filename: str,
        code: str,
        benchmarkCode: str,
        output: Benchmarker.Output,
    ) -> BenchmarkResult:

        result = BenchmarkResult(
            filename=filename,
            code=code,
            benchmarkCode=benchmarkCode,
            output=output.stderr,
        )

        if Benchmarker.compFailMsg in output.stderr:
            return result
        result.compiled = True
        if Benchmarker.execFailMsg in output.stderr:
            return result
        result.executed = True
        try:
            result.runtimeAvg = json.loads(output.stderr)["runtimeAvg"]
        except (json.JSONDecodeError, KeyError):
            pass
        return result

@dataclass
class TestInfo:
    testFile: str
    choices: list[int] = field(default_factory=list)
