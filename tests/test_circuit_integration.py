"""Independent known-answer checks for simple acyclic circuits.

These characterize a small subset of the historical engine, not general
simulation scheduling or timing signoff. Each case compiles and runs in isolation.
"""
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.run_simulation import run
from tools.plot_waveform import read_events


@unittest.skipUnless(shutil.which("g++"), "requires a C++17 compiler")
class CircuitIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def simulate(self, library, circuit, stimulus):
        files = []
        for name, data in (("fixture.lib", library), ("fixture.cir", circuit),
                           ("fixture.stim", stimulus)):
            path = self.root / name
            path.write_text(data, encoding="utf-8")
            files.append(path)
        return read_events(run(*files, self.root / "output.sim"))

    def test_inverter_known_answer_and_fifty_ps_delay(self):
        events = self.simulate(
            "NOT, 1, ~i1, 50\n",
            "INPUTS:\nA\nCOMPONENTS:\nG0, NOT, Y, A\n",
            "0, A, 0\n10, A, 1\n")
        self.assertIn("Y", events)
        self.assertEqual(events["Y"], [(50, 1), (60, 0)])

    def test_or_gate_known_answer_and_two_hundred_ps_delay(self):
        events = self.simulate(
            "OR2, 2, i1|i2, 200\n",
            "INPUTS:\nA\nB\nCOMPONENTS:\nG0, OR2, Y, A, B\n",
            "0, A, 0\n0, B, 0\n100, A, 1\n120, B, 1\n140, A, 0\n160, B, 0\n")
        self.assertIn("Y", events)
        self.assertEqual(events["Y"], [(300, 1), (360, 0)])


if __name__ == "__main__":
    unittest.main()
