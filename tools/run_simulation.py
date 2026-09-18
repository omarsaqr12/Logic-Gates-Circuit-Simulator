"""Compile and run the educational C++ circuit simulator in an isolated directory.

The original program writes fixed relative paths. It also has an uninitialized
validation flag; the runner patches *only* that exact statement in a temporary
copy while retaining the historical source unchanged for provenance. This does
not establish correctness of the original timing algorithm or input parser.
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
LEGACY_FLAG = "bool flag, bool2, pushed = 0;"
INITIALIZED_FLAG = "bool flag = false, bool2 = false, pushed = false;"


def prepare_source(source: Path, destination: Path) -> None:
    """Apply one documented initialization correction to a disposable source copy."""
    content = source.read_text(encoding="utf-8")
    if content.count(LEGACY_FLAG) != 1:
        raise RuntimeError("Cannot safely locate original validation flag; inspect source")
    destination.write_text(content.replace(LEGACY_FLAG, INITIALIZED_FLAG), encoding="utf-8")


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
        patched_source = work / "main.cpp"
        prepare_source(SOURCE, patched_source)
        executable = work / "simulator"
        subprocess.run([compiler, "-std=c++17", "-O2", "-I", str(SOURCE.parent),
                        "-o", str(executable), str(patched_source)],
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
