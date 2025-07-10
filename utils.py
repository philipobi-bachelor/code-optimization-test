from __future__ import annotations
from arango import ArangoClient
from dataclasses import dataclass, asdict
from benchmark import Benchmarker
import json

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

@dataclass
class BenchmarkResult:
    code: str
    benchmarkCode: str
    output: str
    filename: str = ""
    compiled: bool = False
    executed: bool = False
    runtimeAvg: float = -1.0

    def toDBDoc(self) -> dict:
        dump = asdict(self)
        filename = dump.pop("filename")
        dump["_key"] = filename
        return dump

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

        if "Compilation failed" in output.stderr:
            return result
        result.compiled = True
        if "Execution failed" in output.stderr:
            return result
        result.executed = True
        try:
            result.runtimeAvg = json.loads(output.stderr)["runtimeAvg"]
        except (json.JSONDecodeError, KeyError):
            pass
        return result
