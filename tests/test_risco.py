import sys
import unittest
from pathlib import Path


DASHBOARD_DIR = Path(__file__).resolve().parents[1] / "src" / "dashboard"
sys.path.insert(0, str(DASHBOARD_DIR))

from risco import calcular_score_risco


class CalcularScoreRiscoTests(unittest.TestCase):
    def test_baixo_com_alta_confianca_tem_score_baixo(self):
        score = calcular_score_risco(
            ["ALTO", "BAIXO", "MEDIO"],
            [0.01, 0.98, 0.01],
        )
        self.assertEqual(score, 1.5)

    def test_alto_com_alta_probabilidade_tem_score_alto(self):
        score = calcular_score_risco(
            ["ALTO", "BAIXO", "MEDIO"],
            [0.80, 0.05, 0.15],
        )
        self.assertEqual(score, 87.5)

    def test_override_critico_forca_score_maximo(self):
        score = calcular_score_risco(
            ["ALTO", "BAIXO", "MEDIO"],
            [0.01, 0.98, 0.01],
            override_alto=True,
        )
        self.assertEqual(score, 100.0)


if __name__ == "__main__":
    unittest.main()
