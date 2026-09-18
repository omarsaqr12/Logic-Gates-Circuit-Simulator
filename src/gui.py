"""Small Tkinter interface for running and plotting a selected circuit."""
from __future__ import annotations

import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

ROOT = Path(__file__).resolve().parents[1]
selected: dict[str, Path] = {}


def choose_file(kind: str) -> None:
    chosen = filedialog.askopenfilename(title=f"Select {kind.upper()} file")
    if chosen:
        selected[kind] = Path(chosen).resolve()
        selection_label.config(text="\n".join(
            f"{name.upper()}: {selected[name].name if name in selected else '(not selected)'}"
            for name in ("lib", "cir", "stim")))


def execute(command: list[str]) -> bool:
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True,
                                text=True, check=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as error:
        details = getattr(error, "stderr", "") or str(error)
        messagebox.showerror("Execution failed", details)
        return False
    if result.stdout.strip():
        messagebox.showinfo("Simulator", result.stdout.strip())
    return True


def simulate() -> None:
    if any(kind not in selected for kind in ("lib", "cir", "stim")):
        messagebox.showwarning("Missing files", "Select a library, circuit and stimulus file.")
        return
    execute([sys.executable, str(ROOT / "tools" / "run_simulation.py"),
             *(str(selected[kind]) for kind in ("lib", "cir", "stim"))])


def plot() -> None:
    output = ROOT / "build" / "output.sim"
    if not output.is_file():
        messagebox.showwarning("Missing output", "Run a simulation before plotting.")
        return
    execute([sys.executable, str(ROOT / "tools" / "plot_waveform.py"), str(output)])


root = tk.Tk()
root.title("Digital Circuit Simulator")
root.geometry("500x360")
root.configure(bg="#334257")

tk.Label(root, text="Digital Circuit Simulator", bg="#334257", fg="white",
         font=("Helvetica", 17, "bold")).pack(pady=12)
selection_label = tk.Label(root, text="Select three input files", justify="left",
                           bg="#476072", fg="white", padx=12, pady=8)
selection_label.pack(fill="x", padx=18)
for kind in ("lib", "cir", "stim"):
    tk.Button(root, text=f"Select .{kind}",
              command=lambda value=kind: choose_file(value)).pack(fill="x", padx=18, pady=3)
tk.Button(root, text="Run simulation", command=simulate).pack(fill="x", padx=18, pady=5)
tk.Button(root, text="Plot last output", command=plot).pack(fill="x", padx=18, pady=5)

if __name__ == "__main__":
    root.mainloop()
