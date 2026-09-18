"""Plot timestamped digital changes emitted by the C++ simulator."""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def read_events(path: Path) -> dict[str, list[tuple[int, int]]]:
    events: dict[str, list[tuple[int, int]]] = defaultdict(list)
    with Path(path).open(newline="", encoding="utf-8") as stream:
        for line_number, row in enumerate(csv.reader(stream), start=1):
            if not row or not any(item.strip() for item in row):
                continue
            if len(row) != 3:
                raise ValueError(f"Line {line_number}: expected time, wire, value")
            time = int(row[0].strip())
            wire = row[1].strip()
            value = int(row[2].strip())
            if time < 0 or not wire or value not in (0, 1):
                raise ValueError(f"Line {line_number}: invalid time, wire or binary value")
            events[wire].append((time, value))
    if not events:
        raise ValueError("Simulation output has no events to plot")
    for wire in events:
        events[wire].sort(key=lambda event: event[0])
    return dict(events)


def plot_events(events: dict[str, list[tuple[int, int]]], save: Path | None = None) -> None:
    import matplotlib.pyplot as plt

    wires = sorted(events)
    figure, axes = plt.subplots(len(wires), 1, figsize=(11, max(2.4, len(wires) * 1.7)),
                                sharex=True, squeeze=False)
    maximum = 0
    for axis, wire in zip(axes[:, 0], wires):
        changes = events[wire]
        maximum = max(maximum, changes[-1][0])
        times = [0] + [time for time, _ in changes]
        values = [0] + [value for _, value in changes]
        axis.step(times, values, where="post", linewidth=1.8)
        axis.set(yticks=[0, 1], ylim=(-0.2, 1.2), ylabel=wire)
        axis.grid(axis="x", alpha=0.25)
    axes[-1, 0].set(xlabel="Time (ps)", xlim=(0, max(1, maximum * 1.05)))
    figure.tight_layout()
    if save is None:
        plt.show()
    else:
        save = Path(save)
        save.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(save, dpi=150)
    plt.close(figure)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("simulation", type=Path, nargs="?", default=Path("build/output.sim"))
    parser.add_argument("--save", type=Path, help="Write a PNG instead of opening a window")
    args = parser.parse_args(argv)
    try:
        plot_events(read_events(args.simulation), args.save)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Could not plot waveform: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
