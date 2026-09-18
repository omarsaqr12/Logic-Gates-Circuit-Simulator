"""Unit tests for the portable runner and waveform parser (no GPU or GUI required)."""
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import run_simulation
from tools.plot_waveform import read_events


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = self.root / "src" / "main.cpp"
        source.parent.mkdir()
        source.write_text("int main() { return 0; }\n", encoding="utf-8")
        self.paths = []
        for name in ("my library.lib", "circuit.cir", "stimulus.stim"):
            path = self.root / name
            path.write_text("fixture\n", encoding="utf-8")
            self.paths.append(path)
        self.output = self.root / "results" / "trace.sim"

    def test_isolates_generated_files_and_keeps_exact_input_paths(self):
        calls = []

        def fake_run(command, **kwargs):
            calls.append((command, kwargs))
            self.assertNotIn("shell", kwargs)
            if len(calls) == 2:
                work = Path(kwargs["cwd"])
                self.assertNotEqual(work, self.root)
                (work / "Graphing" / "output.sim").write_text("0, A, 1\n", encoding="utf-8")
            return subprocess.CompletedProcess(command, 0, stdout="RUN SUCCESSFULLY !!", stderr="")

        with patch.object(run_simulation, "ROOT", self.root), \
             patch.object(run_simulation, "SOURCE", self.root / "src" / "main.cpp"), \
             patch.object(run_simulation.subprocess, "run", side_effect=fake_run):
            result = run_simulation.run(*self.paths, self.output)
        self.assertEqual(result, self.output)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "0, A, 1\n")
        self.assertEqual(calls[1][0][1:], [str(path) for path in self.paths])

    def test_missing_input_does_not_start_compiler(self):
        with patch.object(run_simulation.subprocess, "run") as compiler:
            with self.assertRaises(FileNotFoundError):
                run_simulation.run(self.root / "absent.lib", *self.paths[1:], self.output)
            compiler.assert_not_called()

    def test_missing_output_is_a_failure_even_if_binary_reports_success(self):
        with patch.object(run_simulation, "ROOT", self.root), \
             patch.object(run_simulation, "SOURCE", self.root / "src" / "main.cpp"), \
             patch.object(run_simulation.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, stdout="RUN SUCCESSFULLY !!", stderr="")):
            with self.assertRaisesRegex(RuntimeError, "did not produce"):
                run_simulation.run(*self.paths, self.output)


class WaveformTests(unittest.TestCase):
    def test_three_column_events_are_grouped_by_wire_and_sorted(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "events.sim"
            file.write_text("20, B, 1\n10, A, 1\n0, A, 0\n", encoding="utf-8")
            self.assertEqual(read_events(file), {"B": [(20, 1)], "A": [(0, 0), (10, 1)]})

    def test_malformed_waveforms_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "events.sim"
            for text in ("10, A, 2\n", "-1, A, 0\n", "10, A\n", "\n"):
                with self.subTest(text=text):
                    file.write_text(text, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        read_events(file)


if __name__ == "__main__":
    unittest.main()
