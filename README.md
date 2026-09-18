# Digital circuit simulator (educational project)

A collaborative C++17 digital-logic simulator with a Tkinter launcher and Python waveform plotting. The C++ engine reads gate definitions (`.lib`), a circuit (`.cir`), and input transitions (`.stim`), then emits timestamped wire changes. The Python runner provides reproducible, isolated execution.

**Scope:** an educational logic-and-delay simulator, not a validated HDL simulator, timing-signoff tool, or production EDA system. The tests establish only the specific cases described below.

## Run an example

Requires Python 3.10+ and a C++17 compiler (`g++` on PATH). From the repository root:

```bash
python tools/run_simulation.py \
  examples/circuit_01/circuit_01.lib \
  examples/circuit_01/circuit_01.cir \
  examples/circuit_01/circuit_01.stim
```

The runner checks its three input paths, builds in an isolated temporary directory, enforces a simulator timeout, and copies nonempty output to `build/output.sim`. Use `--output path/to/result.sim` to specify another output destination or `--timeout 10` to adjust the simulation limit. The original engine writes fixed files relative to its working directory; the runner keeps these out of your checkout.

**Historical C++ defect and workaround:** the original `src/main.cpp` declares `bool flag, bool2, pushed = 0;`, leaving `bool2` uninitialized. The first CI run demonstrated that this can spuriously reject a valid circuit. To preserve the original collaborative source, the runner checks for the exact statement and initializes all three flags *only in a disposable source copy* before compiling. Directly compiling `src/main.cpp` still has the defect. This narrow correction does not establish that the timing algorithm is generally correct.

To plot a result:

```bash
python -m pip install -r requirements.txt
python tools/plot_waveform.py build/output.sim --save build/waveform.png
# Omit --save to display the graph on a desktop.
```

Each `.sim` row is `time_ps, wire_name, binary_value`; the plotter groups and sorts transitions per wire. It assumes a value of zero before a wire's first recorded event for visualization only. The original module entry point `python -m src.Graphing.simulation_graphing build/output.sim` delegates to the same plotter. For the optional GUI, install Tkinter through your Python/OS distribution (for example `python3-tk` on Ubuntu) and run `python src/gui.py`; the GUI passes the files you select as paths rather than interpolating them into a shell command.

## Source and tests

- [`src/main.cpp`](src/main.cpp) and [`src/Custom_gates.cpp`](src/Custom_gates.cpp): original input parsing, circuit evaluation and delay logic, plus Boolean expression evaluation for `~`, `&` and `|`.
- [`tools/run_simulation.py`](tools/run_simulation.py), [`tools/plot_waveform.py`](tools/plot_waveform.py) and [`src/gui.py`](src/gui.py): isolated execution, waveform visualization and optional file-selection interface.
- [`tests/gate_truth.cpp`](tests/gate_truth.cpp): 26 independently calculated basic-gate truth-table cases and rejection of an undefined gate operand.
- [`tests/test_tools.py`](tests/test_tools.py): six tests of file handling, runner isolation, the narrow source correction, and waveform parsing.
- [`tests/test_circuit_integration.py`](tests/test_circuit_integration.py): independently specified output transitions and 50 ps/200 ps delays for simple inverter and OR circuits, run through the full simulator.
- [GitHub Actions](.github/workflows/ci.yml) runs the tests, compiles and executes `circuit_01`, and generates a nonempty waveform image on Ubuntu.

Run Python checks with `python -m unittest discover -s tests -v`. The `examples/` directory illustrates the accepted input syntax; do not assume it accepts Verilog/VHDL or arbitrary CSV formats.

## Limitations and provenance

The full engine has **not** been validated against a reference event-driven simulator. Simultaneous transitions, reconvergent paths, event cancellation, cycles, malformed inputs, and propagation-delay edge cases remain unverified. Do not use its output for engineering decisions. The original parser assumes well-formed inputs in places; a timeout prevents indefinite runs but does not validate circuit semantics. [`examples/circuit_05/circuit_05.cir`](examples/circuit_05/circuit_05.cir) contains an incomplete NAND instance and an undefined wire; it is retained as historical material, not advertised as a passing example. The `examples/tests/` directory includes intentionally invalid inputs. Historical diagrams and PDFs have been preserved, not independently reproduced.

This is a collaborative project involving [Omar Saqr](https://github.com/omarsaqr12), [AdhamALI68](https://github.com/AdhamALI68), and [BeTechBo](https://github.com/BeTechBo); see commit history for provenance. Ownership of each individual component has not been independently established. The original [MIT license](LICENSE), its copyright notice, and historical files remain unchanged.
