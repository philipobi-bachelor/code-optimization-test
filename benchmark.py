import docker
import socket
import struct

def readStreamsFromSock(sock, stdout=True, stderr=True):
    # stream identifiers: stdout: 1 , stderr: 2
    buffers = [None, b"", b""]
    
    streams = 0b00
    streams |= stdout
    streams |= stderr << 1
    
    while True:
        header = sock.recv(8)
        if len(header) < 8: break
        (streamID, *_) = struct.unpack(">B", header[0:1])
        (payloadLen, *_) = struct.unpack(">I", header[4:8])
        if ( 
            payloadLen > 0 and
            len(payload := sock.recv(payloadLen)) == payloadLen
        ): 
            if streamID & streams: buffers[streamID] += payload
        else: break
    return dict(
        stdout = buffers[1].decode(errors="ignore"),
        stderr = buffers[2].decode(errors="ignore")
    )

class Benchmarker:            
    def __init__(self):
        self.client = docker.from_env()

    def runCode(self, code, stdout=True, stderr=True):
        compileCommand = (
            "g++ "
            "-w -O3 --std=c++17 "
            "nanobench.o "
            "-x c++ - "
            "-o a.out"
        )

        shellCommand = (
            "sh -c \""
            f"timeout 60 {compileCommand}; "
            "exitCode=$?; "
            "if [ $exitCode -ne 0 ]; then "
                "echo Compilation failed 1>&2; exit 1; "
            "fi; "
            "timeout 600 ./a.out; "
            "exitCode=$?; "
            "if [ $exitCode -ne 0 ]; then "
                "echo Execution failed 1>&2; exit 1; "
            "fi"
            "\""
        )
        container = self.client.containers.run(
            "localhost/benchmark-examples", 
            shellCommand,
            working_dir="/usr/src",
            remove=True, detach=True, stdin_open=True,
        )
        socketIO = container.attach_socket(params=dict(stdin=1, stdout=1, stderr=1, stream=1))
        sock = socketIO._sock
        sock.sendall(code.encode())
        sock.shutdown(socket.SHUT_WR)
        return readStreamsFromSock(sock, stdout=stdout, stderr=stderr)