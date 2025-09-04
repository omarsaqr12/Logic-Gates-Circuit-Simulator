# Digital Circuit Simulator

A comprehensive digital circuit simulation tool written in C++ with Python visualization capabilities. This project simulates the behavior of digital logic circuits, calculates propagation delays, and provides graphical visualization of the simulation results.

## 🚀 Features

- **Circuit Simulation**: Simulates digital logic circuits with custom gate definitions
- **Propagation Delay Calculation**: Accurately calculates and tracks signal propagation delays
- **Multiple File Format Support**: Supports `.lib`, `.cir`, and `.stim` file formats
- **Graphical Visualization**: Python-based plotting of simulation results
- **GUI Interface**: User-friendly graphical interface for easy operation
- **Error Handling**: Comprehensive error checking and validation
- **Multiple Example Circuits**: Includes 5 example circuits for testing and learning

## 📁 Project Structure

```
digital-circuit-simulator/
├── src/                          # Source code
│   ├── main.cpp                  # Main C++ simulator
│   ├── Custom_gates.cpp          # Custom logic gate implementations
│   ├── gui.py                    # GUI application
│   ├── runner.py                 # Command-line runner script
│   └── Graphing/                 # Visualization module
│       ├── SG.py                 # Signal graphing utilities
│       └── simulation_graphing.py # Main graphing script
├── examples/                     # Example circuits and test files
│   ├── circuit_01/              # Example circuit 1
│   ├── circuit_02/              # Example circuit 2
│   ├── circuit_03/              # Example circuit 3
│   ├── circuit_04/              # Example circuit 4
│   ├── circuit_05/              # Example circuit 5
│   └── tests/                   # Test files
├── docs/                        # Documentation
│   ├── project_requirements.pdf # Project requirements
│   └── propagation_delay_graphs.pdf # Delay analysis
└── assets/                      # Images and other assets
```

## 🔧 Installation

### Prerequisites

- **C++ Compiler**: GCC or any C++11 compatible compiler
- **Python 3.7+**: For visualization and GUI
- **Git**: For cloning the repository

### Setup

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/digital-circuit-simulator.git
cd digital-circuit-simulator
```

2. **Install Python dependencies**:

```bash
pip install -r requirements.txt
```

3. **Compile the C++ simulator**:

```bash
g++ -o main src/main.cpp
```

## 📖 Usage

### Command Line Interface

Run the simulator with three input files:

```bash
./main <library_file> <circuit_file> <stimulus_file>
```

**Example**:

```bash
./main examples/tests/cells.lib examples/tests/2.cir examples/tests/1.stim
```

### Graphical User Interface

Launch the GUI application:

```bash
python src/gui.py
```

The GUI allows you to:

- Upload library, circuit, and stimulus files
- Run simulations with a single click
- View simulation results graphically

### Python Runner Script

Use the automated runner script:

```bash
python src/runner.py
```

## 📄 File Formats

### Library File (`.lib`)

Defines logic gates with their behavior and propagation delays:

```
GATE_NAME, NUM_INPUTS, LOGIC_EXPRESSION, DELAY_PS
OR2, 2, i1|i2, 200
NOT, 1, ~i1, 50
```

### Circuit File (`.cir`)

Describes the circuit structure and connections:

```
INPUTS:
A
B

COMPONENTS:
G0, OR2, W0, A, B
G1, NOT, W1, B
```

### Stimulus File (`.stim`)

Provides input signals over time:

```
TIME_PS, INPUT_NAME, VALUE
0, A, 0
100, A, 1
200, B, 1
```

## 🎯 Example Circuits

The project includes 5 example circuits demonstrating different logic configurations:

1. **Circuit 01**: Basic OR and NOT gates
2. **Circuit 02**: Complex combinational logic
3. **Circuit 03**: Multi-level logic circuits
4. **Circuit 04**: Advanced gate combinations
5. **Circuit 05**: Comprehensive test circuit

Each example includes:

- Circuit diagram (`.png`)
- Library file (`.lib`)
- Circuit description (`.cir`)
- Test stimuli (`.stim`)
- Expected simulation results (`.sim`)

## 🔬 How It Works

1. **File Parsing**: The simulator reads and parses library, circuit, and stimulus files
2. **Circuit Construction**: Builds an internal representation of the circuit
3. **Logic Simulation**: Evaluates logic expressions using custom gate implementations
4. **Delay Calculation**: Computes propagation delays through the circuit paths
5. **Result Generation**: Outputs timestamped signal changes to a `.sim` file
6. **Visualization**: Python scripts generate timing diagrams from simulation results

## ⚠️ Error Handling

The simulator includes comprehensive error checking:

- **Gate Definition Errors**: Validates that all gates used in circuits are defined in libraries
- **Input/Output Conflicts**: Ensures inputs are not used as outputs
- **File Format Validation**: Checks file format correctness
- **Logic Expression Validation**: Validates gate logic expressions

## 🛠️ Development

### Building from Source

```bash
# Compile with debug information
g++ -g -o main_debug src/main.cpp

# Compile with optimizations
g++ -O3 -o main_optimized src/main.cpp
```

### Running Tests

Test the simulator with provided examples:

```bash
# Test all example circuits
for i in {1..5}; do
    ./main examples/circuit_0$i/circuit_0$i.lib \
           examples/circuit_0$i/circuit_0$i.cir \
           examples/circuit_0$i/circuit_0$i.stim
done
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Digital Design Team** - Initial work and development

## 🙏 Acknowledgments

- Thanks to the Digital Design course instructors for project guidance
- Circuit simulation algorithms based on standard digital design principles
- Python visualization inspired by modern EDA tools

## 📚 References

- Digital Design and Computer Architecture principles
- Logic simulation and timing analysis methodologies
- Standard file formats for digital circuit description

---

**Note**: This simulator is designed for educational purposes and demonstrates fundamental concepts in digital circuit simulation and timing analysis.
