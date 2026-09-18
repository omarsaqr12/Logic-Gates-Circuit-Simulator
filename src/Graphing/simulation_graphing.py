"""Compatibility entry point for the simulator's waveform plotter.

Run from the repository root: python -m src.Graphing.simulation_graphing build/output.sim
"""
from tools.plot_waveform import main


if __name__ == "__main__":
    raise SystemExit(main())
