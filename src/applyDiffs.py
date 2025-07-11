import re
from pathlib import PosixPath as Path
import subprocess

diffRegex = re.compile(
    r"main\d.cpp.*?Squashed changes \(short\).*?```diff\s*(?P<diff>.*?)(?=```)",
    flags=re.DOTALL,
)

def main():
    for i in (1, 2):
        test = f"test{i}"
        outDir = Path("testResults", test)
        Path.mkdir(outDir, exist_ok=True, parents=True)
        for file in filter(
            lambda path: path.is_file(),
            Path("chat-logs", test).iterdir(),
        ):
            with Path.open(file, "r") as f:
                [match] = list(re.finditer(diffRegex, f.read()))
                diff = match.group("diff")

            modelName = file.stem
            inFile = f"main{i}.cpp"
            outFile = outDir / f"{modelName}.cpp"
            print(f"Patching {inFile} to {outFile}")
            cmd = ("patch", "-p2", inFile, "-o", str(outFile))
            result = subprocess.run(
                cmd,
                input=diff,
                text=True,
                capture_output=True,
            )
            print(result.stdout)
            print(result.stderr)


if __name__ == "__main__":
    main()