"""Compile and run the educational C++ circuit simulator in an isolated directory.

The program writes fixed relative paths, so execution uses a temporary working
directory. The checked-in C++ source is compiled directly, without modifying a
temporary source copy. This does not establish general timing-algorithm or
input-parser correctness.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "main.cpp"
DEFAULT_OUTPUT = ROOT / "build" / "output.sim"
def run(library: Path, circuit: Path, stimulus: Path, output: Path = DEFAULT_OUTPUT,
        *, compiler: str = "g++", timeout: int = 20) -> Path:
    inputs = [Path(p).expanduser().resolve() for p in (library, circuit, stimulus)]
    for path in inputs:
        if not path.is_file():
            raise FileNotFoundError(f"Input file not found: {path}")
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Simulator source not found: {SOURCE}")

    output = Path(output).expanduser().resolve()
    with tempfile.TemporaryDirectory(prefix="logic-simulator-") as directory:
        work = Path(directory)
        (work / "Graphing").mkdir()
        executable = work / "simulator"
        subprocess.run([compiler, "-std=c++17", "-O2", "-I", str(SOURCE.parent),
                        "-o", str(executable), str(SOURCE)],
                       cwd=ROOT, check=True, timeout=90)
        completed = subprocess.run([str(executable), *(str(path) for path in inputs)],
                                   cwd=work, capture_output=True, text=True,
                                   check=True, timeout=timeout)
        generated = work / "Graphing" / "output.sim"
        if not generated.is_file() or generated.stat().st_size == 0:
            raise RuntimeError("Simulator did not produce nonempty Graphing/output.sim. "
                               f"stdout: {completed.stdout.strip()} "
                               f"stderr: {completed.stderr.strip()}")
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(generated, output)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("library", type=Path, help="Gate library (.lib)")
    parser.add_argument("circuit", type=Path, help="Circuit description (.cir)")
    parser.add_argument("stimulus", type=Path, help="Stimulus (.stim)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=int, default=20, help="Simulation timeout in seconds")
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    try:
        output = run(args.library, args.circuit, args.stimulus, args.output,
                     timeout=args.timeout)
    except (FileNotFoundError, RuntimeError, subprocess.SubprocessError, OSError) as error:
        print(f"Simulation failed: {error}", file=sys.stderr)
        return 1
    print(f"Simulation file: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
