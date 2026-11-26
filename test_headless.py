import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class HeadlessSmokeTest(unittest.TestCase):
    def test_one_local_turn_without_desktop(self):
        env = os.environ.copy()
        env.pop("DISPLAY", None)
        env.pop("WAYLAND_DISPLAY", None)
        env["PYTHONPATH"] = str(Path(__file__).resolve().parent)
        with tempfile.TemporaryDirectory() as workdir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "from pathlib import Path; import log_turno, main, sys; "
                    "log_turno.PASTA = Path('logs'); main.main(); "
                    "assert 'pyautogui' not in sys.modules",
                    "--rapido", "--sem-janelas", "--seed", "7", "--max-turns", "1",
                ],
                cwd=workdir,
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("disparo executado", output)
        self.assertIn("Total de turnos jogados: 1", output)
