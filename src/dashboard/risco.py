"""Funcoes de dominio para transformar probabilidades em score de risco."""

from __future__ import annotations

from collections.abc import Iterable


PESO_RISCO = {
    "BAIXO": 0.0,
    "MEDIO": 50.0,
    "ALTO": 100.0,
}


def calcular_score_risco(
    classes: Iterable[str],
    probabilidades: Iterable[float],
    override_alto: bool = False,
) -> float:
    """Retorna risco esperado de 0 a 100, e nao a confianca do modelo.

    BAIXO vale 0, MEDIO vale 50 e ALTO vale 100. Quando uma regra critica
    deterministica forca a classe ALTO, o score tambem passa a 100.
    """
    if override_alto:
        return 100.0

    pares = list(zip(classes, probabilidades))
    if not pares:
        raise ValueError("Classes e probabilidades nao podem estar vazias.")

    desconhecidas = [classe for classe, _ in pares if classe not in PESO_RISCO]
    if desconhecidas:
        raise ValueError(f"Classe(s) de risco desconhecida(s): {desconhecidas}")

    score = sum(PESO_RISCO[classe] * float(prob) for classe, prob in pares)
    return round(max(0.0, min(100.0, score)), 2)
