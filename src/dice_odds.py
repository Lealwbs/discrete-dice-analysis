"""
Calculo exato de probabilidades para a soma de dados honestos.
Inclui programacao dinamica com memoizacao e a formula classica de De Moivre.
"""

from functools import lru_cache
from math import comb
from typing import Dict


@lru_cache(maxsize=8192)
def exact_dice_count(sum_value: int, num_dice: int, sides: int = 6) -> int:
    """
    Retorna o numero exato de tuplas ordenadas (d_1, ..., d_n) em {1, ..., sides}^n
    cuja soma vale sum_value.
    """
    if num_dice < 1 or sum_value < num_dice or sum_value > sides * num_dice:
        return 0

    if num_dice == 1:
        return 1 if 1 <= sum_value <= sides else 0

    # Aproveita a simetria da distribuicao em torno de n * (sides + 1) / 2
    total_center = (sides + 1) * num_dice
    if sum_value > total_center // 2:
        sum_value = total_center - sum_value

    ways = 0
    dice_rem = num_dice - 1
    min_face = max(1, sum_value - sides * dice_rem)
    max_face = min(sides, sum_value - dice_rem)

    for face in range(min_face, max_face + 1):
        ways += exact_dice_count(sum_value - face, dice_rem, sides)

    return ways


def exact_dice_odds(sum_value: int, num_dice: int, sides: int = 6) -> float:
    """
    Retorna a probabilidade exata P(S_n = sum_value) no lancamento de num_dice dados.
    """
    if num_dice < 1 or sum_value < num_dice or sum_value > sides * num_dice:
        return 0.0

    favorable_ways = exact_dice_count(sum_value, num_dice, sides)
    total_outcomes = sides ** num_dice
    return favorable_ways / total_outcomes


def de_moivre_dice_probability(sum_value: int, num_dice: int, sides: int = 6) -> float:
    """
    Calcula P(S_n = sum_value) pela formula de inclusao-exclusao de Abraham de Moivre (1711).
    """
    if num_dice < 1 or sum_value < num_dice or sum_value > sides * num_dice:
        return 0.0

    k = sum_value
    n = num_dice
    s = sides
    max_j = (k - n) // s

    total_ways = 0
    for j in range(max_j + 1):
        sign = -1 if (j % 2 == 1) else 1
        total_ways += sign * comb(n, j) * comb(k - s * j - 1, n - 1)

    return total_ways / (s ** n)


def dice_distribution(num_dice: int, sides: int = 6) -> Dict[int, float]:
    """
    Retorna um dicionario {soma: probabilidade} para todas as somas possiveis.
    """
    return {
        k: exact_dice_odds(k, num_dice, sides)
        for k in range(num_dice, num_dice * sides + 1)
    }


# Nome original mantido para compatibilidade com as primeiras versoes do repositorio
what_are_the_odds = exact_dice_odds
