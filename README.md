# Digital circuit simulator (educational project)

A collaborative C++17 digital-logic simulation project with a small Tkinter launcher and a Python waveform plotter. The C++ program reads gate definitions (`.lib`), a circuit description (`.cir`), and input transitions (`.stim`). It writes timestamped signal changes. The Python tools provide an isolated, cross-platform way to compile/run it and inspect the resulting waveform.

**Scope:** an educational logic-and-delay simulator, **not** a validated HDL simulator, timing-signoff tool, or production EDA system. The original C++ simulation engine remains under review; a successful process exit is not proof that a circuit or its delays were simulated correctly.

## Quickstart (CLI)

Requires Python 3.10+ and a C++17 compiler (`g++` on PATH). Run from the repository root:

```bash
python tools/run_simulation.py \
  examples/circuit_01/circuit_01.lib \
  examples/circuit_01/circuit_01.cir \
  examples/circuit_01/circuit_01.stim
```

**Legacy source workaround:** the first CI run exposed an uninitialized `bool2` in the original C++ `violation_check`: it rejected a valid example with a spurious input/output conflict. To preserve the collaborators' historical engine, the runner copies `src/main.cpp` into its temporary build directory, checks for **exactly one** occurrence of `bool flag, bool2, pushed = 0;`, and initializes all three flags in that disposable copy before compiling. The original tracked engine is **not fixed** and direct `g++ src/main.cpp` can still exhibit this defect; use the documented runner. The workaround does not validate the engine's simulation semantics.

The runner uses a temporary working directory, checks that the engine created a nonempty waveform, and copies it to `build/output.sim`. Isolation is important because the original program writes fixed filenames (`o`, `output.txt`, and `Graphing/output.sim`) relative to its working directory. Use `--output path/to/result.sim` to choose a destination; `--timeout` limits the simulator's runtime for problematic inputs. Missing files and missing output are reported as errors.

For plotting:

```bash
python -m pip install -r requirements.txt
python tools/plot_waveform.py build/output.sim --save build/waveform.png
# Omit --save to show the plot in a desktop window.
```

The parser expects each output row to contain **three** fields: `time_ps, wire_name, binary_value`. Each wire gets its own step trace. The plot assumes a value of zero before the first recorded change; this is a plotting convention, not a separately verified simulator result. The compatibility command `python -m src.Graphing.simulation_graphing build/output.sim` uses the same parser.

To use the GUI, install Tkinter through your operating system if your Python distribution lacks it (for example, `python3-tk` on Debian/Ubuntu), then run `python src/gui.py` from the repository root. Select the actual three files on your computer; the GUI passes their absolute paths to the runner without shell interpolation. Plotting additionally requires Matplotlib.

## Input examples and implementation

An existing, small example is in [`examples/circuit_01/`](examples/circuit_01). Its library defines OR2 and NOT gates with Boolean expressions and delays, its `.cir` declares input wires and gate instances, and its `.stim` lists input changes such as `600, B, 1`. For the exact supported syntax, use the tracked examples rather than assuming compatibility with standard HDL or generic CSV libraries.

- [`src/main.cpp`](src/main.cpp): original C++ file parsing, circuit traversal, logic evaluation, and timestamp generation. It includes [`src/Custom_gates.cpp`](src/Custom_gates.cpp), an expression evaluator for `~`, `&`, and `|`.
- [`tools/run_simulation.py`](tools/run_simulation.py): temporary-copy flag initialization, compiler invocation, isolated working directory, input-path handling, failure/timeout reporting, and output collection.
- [`tools/plot_waveform.py`](tools/plot_waveform.py): three-column output parsing and per-wire digital timing plots.
- [`src/gui.py`](src/gui.py): optional Tkinter file-selection interface.
- [`tests/test_tools.py`](tests/test_tools.py): isolated-runner and waveform-parser tests; [CI](.github/workflows/ci.yml) also attempts an example compile/run and headless plot.

## Known limitations / verification status

- The C++ algorithm has not been independently checked against a reference event-driven simulator. Correctness for simultaneous changes, reconvergent paths, cycles, malformed expressions, and propagation-delay edge cases is **not established**. Avoid using its output for engineering decisions.
- The original C++ parser and error paths assume well-formed input in places. In particular, its gate-library and stimulus handling may fail on malformed files; `--timeout` is a safety limit, not a circuit-validity check.
- [`examples/circuit_05/circuit_05.cir`](examples/circuit_05/circuit_05.cir) contains an incomplete `NAND2` instance and refers to an undefined wire. It is preserved as historical material but **not** a passing example. Files in `examples/tests/` include intentionally invalid cases and are not a passing test suite.
- The test suite verifies tooling, the isolated initialization correction, and file format handling. The CI smoke run checks that one example produces a nonempty file, **not** that its timing or Boolean values agree with an independent oracle. No numerical timing-accuracy claim is made.
- Historical diagrams and PDFs in `assets/` and `docs/` are retained without claiming their figures or conclusions were independently reproduced.

## Contributors and provenance

This is a collaborative project involving [Omar Saqr](https://github.com/omarsaqr12), [AdhamALI68](https://github.com/AdhamALI68), and [BeTechBo](https://github.com/BeTechBo). See the repository history and AdhamALI68's version history for contribution provenance; individual ownership of each component has not been independently established. The existing [MIT license](LICENSE) retains its original copyright notice. No licenses or historical research artifacts were changed as part of this cleanup.
