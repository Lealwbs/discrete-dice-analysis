"""
Cálculo exato de probabilidades de somas de dados.
"""

from functools import lru_cache
from math import comb, pow
from typing import Dict


@lru_cache(maxsize=4096)
def exact_dice_count(sum_value: int, num_dice: int, sides: int = 6) -> int:
    """
    Retorna a quantidade de combinações favoráveis para a soma em num_dice dados.
    """
    if num_dice < 1 or sum_value < num_dice or sum_value > sides * num_dice:
        return 0

    if num_dice == 1:
        return 1 if 1 <= sum_value <= sides else 0

    # Simetria da distribuição
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
    Retorna a probabilidade exata P(Soma = sum_value) com num_dice dados.
    """
    if num_dice < 1 or sum_value < num_dice or sum_value > sides * num_dice:
        return 0.0

    total_outcomes = pow(sides, num_dice)
    favorable_ways = exact_dice_count(sum_value, num_dice, sides)
    return favorable_ways / total_outcomes


def de_moivre_dice_probability(sum_value: int, num_dice: int, sides: int = 6) -> float:
    """
    Fórmula clássica de Abraham de Moivre (1718) para somas de dados.
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
        c1 = comb(n, j)
        c2 = comb(k - s * j - 1, n - 1)
        total_ways += sign * c1 * c2

    return total_ways / pow(s, n)


def dice_distribution(num_dice: int, sides: int = 6) -> Dict[int, float]:
    """
    Retorna um dicionário {soma: probabilidade} para todas as somas possíveis.
    """
    return {s: exact_dice_odds(s, num_dice, sides) for s in range(num_dice, num_dice * sides + 1)}


# Alias para compatibilidade
what_are_the_odds = exact_dice_odds
