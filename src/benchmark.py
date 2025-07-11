from __future__ import annotations
import docker
import socket
import struct
from dataclasses import dataclass


class Benchmarker:
    codeTemplate = """\
#include "nanobench.h"
#include <iostream>
#include <chrono>
{includes}

{additionalDefs}

void benchmarkFunc() {{
    {benchmarkBody}
}}

int main() {{
    ankerl::nanobench::Bench benchmark;
    benchmark
    .output(nullptr)
    .epochs({epochs})
    .minEpochIterations({minEpochIterations})
    .minEpochTime(std::chrono::duration_cast<std::chrono::nanoseconds>(
        std::chrono::milliseconds({minEpochTimeMs})
    ));
    benchmark.run("test", []() {{benchmarkFunc();}});
    benchmark.render("{nanobenchOutputTemplate}", std::cerr);
}}
"""

    def renderTemplate(self, code: Code) -> str:

        return Benchmarker.codeTemplate.format(
            includes='\n'.join(code.includes),
            additionalDefs=code.additionalDefs,
            benchmarkBody=code.body,
            epochs=self.nanobenchOptions.epochs,
            minEpochIterations=self.nanobenchOptions.minEpochIterations,
            minEpochTimeMs=self.nanobenchOptions.minEpochTimeMs,
            nanobenchOutputTemplate=self.nanobenchOptions.outputTemplate,
        )

    @dataclass
    class Code:
        includes: list[str]
        additionalDefs: str
        body: str

    @dataclass
    class NanobenchOptions:
        epochs: int = 15
        minEpochIterations: int = 10
        minEpochTimeMs: int = 100
        outputTemplate: str = (
            '{ {{#result}} \\"runtimeAvg\\": {{average(elapsed)}} {{/result}} }'
        )

    @dataclass
    class Output:
        stdout: str
        stderr: str

    @staticmethod
    def readStreamsFromSock(sock, stdout=True, stderr=True) -> Output:
        # stream identifiers: stdout: 1 , stderr: 2
        buffers = [None, b"", b""]

        streams = 0b00
        streams |= stdout
        streams |= stderr << 1

        while True:
            header = sock.recv(8)
            if len(header) < 8:
                break
            (streamID, *_) = struct.unpack(">B", header[0:1])
            (payloadLen, *_) = struct.unpack(">I", header[4:8])
            if payloadLen > 0 and len(payload := sock.recv(payloadLen)) == payloadLen:
                if streamID & streams:
                    buffers[streamID] += payload
            else:
                break
        return Benchmarker.Output(
            stdout=buffers[1].decode(errors="ignore"),
            stderr=buffers[2].decode(errors="ignore"),
        )

    def __init__(
        self,
        benchmarkImg: str = "localhost/benchmark",
        nanobenchOptions: NanobenchOptions = NanobenchOptions(),
    ):
        self.client = docker.from_env()
        self.benchmarkImg = benchmarkImg
        self.nanobenchOptions = nanobenchOptions

    def run(
        self,
        code: str,
        stdout: bool = True,
        stderr: bool = True,
    ) -> Output:
        compileCommand = (
            "g++ " "-w -O3 --std=c++17 " "nanobench.o " "-x c++ - " "-o a.out"
        )

        shellCommand = "; ".join(
            (
                compileCommand,
                "exitCode=$?",
                "if [ $exitCode -ne 0 ]",
                'then echo \\"Compilation failed\\" 1>&2; exit 1',
                "fi",
                "./a.out",
                "exitCode=$?",
                "if [ $exitCode -ne 0 ]",
                'then echo \\"Execution failed\\" 1>&2; exit 1',
                "fi",
            )
        )

        container = self.client.containers.run(
            self.benchmarkImg,
            f'sh -c "{shellCommand}"',
            working_dir="/usr/src",
            remove=True,
            detach=True,
            stdin_open=True,
        )
        socketIO = container.attach_socket(
            params=dict(stdin=1, stdout=1, stderr=1, stream=1)
        )
        sock = socketIO._sock
        sock.sendall(code.encode())
        sock.shutdown(socket.SHUT_WR)
        return Benchmarker.readStreamsFromSock(sock, stdout=stdout, stderr=stderr)
