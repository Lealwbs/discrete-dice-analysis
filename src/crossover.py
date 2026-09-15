"""
Cálculo analítico do ponto de encontro (crossover) e parâmetros estatísticos.
"""

import math
from typing import Tuple
from scipy.stats import norm

try:
    from .dice_odds import exact_dice_odds
except ImportError:
    from dice_odds import exact_dice_odds


def dice_parameters(sides: int = 6) -> Tuple[float, float]:
    """
    Retorna a média (mu) e a variância (var) de 1 dado justo de 'sides' faces.
    """
    mu = (sides + 1) / 2.0
    var = (sides**2 - 1) / 12.0
    return mu, var


def exact_gaussian_crossover(n: int, m: int, sides: int = 6) -> float:
    """
    Calcula a fórmula analítica fechada do ponto de encontro contínuo x*
    entre as distribuições aproximadas de n dados e m dados:

        x* = mu_g * sqrt(1 + (CV^2) / L(n, m))

    Onde:
        mu_g = mu * sqrt(n * m) = sqrt(E_n * E_m)  -> Média Geométrica das esperanças
        CV = sigma / mu                            -> Coeficiente de Variação de 1 dado
        L(n, m) = (m - n) / ln(m / n)              -> Média Logarítmica de n e m
    """
    if n == m:
        mu, _ = dice_parameters(sides)
        return float(n * mu)

    if n > m:
        n, m = m, n

    mu, var = dice_parameters(sides)
    cv_sq = var / (mu ** 2)

    # Média Geométrica das Esperanças
    mu_g = mu * math.sqrt(n * m)

    # Média Logarítmica
    log_mean = (m - n) / math.log(m / n)

    # Crossover exato
    x_star = mu_g * math.sqrt(1.0 + (cv_sq / log_mean))
    return x_star


def discrete_crossover_point(n: int, m: int, sides: int = 6) -> Tuple[int, float, float]:
    """
    Retorna o primeiro inteiro k onde P(m dados = k) >= P(n dados = k), com m > n.
    """
    if n > m:
        n, m = m, n

    for k in range(n, m * sides + 1):
        p_n = exact_dice_odds(k, n, sides)
        p_m = exact_dice_odds(k, m, sides)
        if p_m >= p_n:
            return k, p_n, p_m

    return m * sides, 0.0, exact_dice_odds(m * sides, m, sides)


def gaussian_pdf(x, num_dice: int, sides: int = 6):
    """
    Densidade contínua normal da soma de num_dice dados.
    """
    mu_1, var_1 = dice_parameters(sides)
    mean = num_dice * mu_1
    std = math.sqrt(num_dice * var_1)
    return norm.pdf(x, mean, std)
