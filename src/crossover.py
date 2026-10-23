"""
Calculo do ponto de virada (crossover) entre distribuicoes de soma de dados
e relacoes entre media aritmetica, media geometrica e media logaritmica.
"""

import math
from typing import Dict, Tuple, Union
import numpy as np

try:
    from .dice_odds import exact_dice_odds
except ImportError:
    from dice_odds import exact_dice_odds


def dice_parameters(sides: int = 6) -> Tuple[float, float]:
    """
    Retorna a esperanca (mu_1) e a variancia (var_1) de um unico dado honesto de 'sides' faces.
    """
    mu_1 = (sides + 1) / 2.0
    var_1 = (sides ** 2 - 1) / 12.0
    return mu_1, var_1


def logarithmic_mean(n: float, m: float) -> float:
    """
    Calcula a media logaritmica L(n, m) = (m - n) / (ln(m) - ln(n)).
    """
    if n <= 0 or m <= 0:
        raise ValueError("Os argumentos da media logaritmica devem ser positivos.")
    if n == m:
        return float(n)
    return (m - n) / math.log(m / n)


def exact_gaussian_crossover(n: int, m: int, sides: int = 6) -> float:
    """
    Calcula o ponto de intersecao positivo x* entre as aproximacoes normais
    das somas de n dados e m dados:

        x* = mu_G * sqrt(1 + CV_1^2 / L(n, m))

    onde:
        mu_G = mu_1 * sqrt(n * m)        (media geometrica das esperancas)
        CV_1^2 = var_1 / mu_1^2          (coeficiente de variacao ao quadrado de 1 dado)
        L(n, m) = (m - n) / ln(m / n)    (media logaritmica entre n e m)
    """
    if n == m:
        mu_1, _ = dice_parameters(sides)
        return float(n * mu_1)

    if n > m:
        n, m = m, n

    mu_1, var_1 = dice_parameters(sides)
    cv_sq = var_1 / (mu_1 ** 2)
    mu_g = mu_1 * math.sqrt(n * m)
    log_mean = logarithmic_mean(n, m)

    return mu_g * math.sqrt(1.0 + (cv_sq / log_mean))


def classical_means_summary(n: int, m: int, sides: int = 6) -> Dict[str, float]:
    """
    Retorna um resumo com as esperancas, media aritmetica, media geometrica,
    media logaritmica e o ponto de intersecao gaussiano x*.
    """
    if n > m:
        n, m = m, n

    mu_1, var_1 = dice_parameters(sides)
    e_n = n * mu_1
    e_m = m * mu_1
    mu_a = (e_n + e_m) / 2.0
    mu_g = math.sqrt(e_n * e_m)
    l_nm = logarithmic_mean(n, m)
    x_star = exact_gaussian_crossover(n, m, sides)

    return {
        "e_n": e_n,
        "e_m": e_m,
        "var_n": n * var_1,
        "var_m": m * var_1,
        "arithmetic_mean": mu_a,
        "geometric_mean": mu_g,
        "logarithmic_mean_nm": l_nm,
        "x_star": x_star,
    }


def discrete_crossover_point(n: int, m: int, sides: int = 6) -> Tuple[int, float, float]:
    """
    Retorna o primeiro inteiro k no qual P(S_m = k) >= P(S_n = k), assumindo m > n.
    Tambem retorna os valores de P(S_n = k) e P(S_m = k) nesse ponto.
    """
    if n > m:
        n, m = m, n

    for k in range(n, m * sides + 1):
        p_n = exact_dice_odds(k, n, sides)
        p_m = exact_dice_odds(k, m, sides)
        if p_m >= p_n and p_m > 0:
            return k, p_n, p_m

    last_k = m * sides
    return last_k, 0.0, exact_dice_odds(last_k, m, sides)


def gaussian_pdf(x: Union[float, np.ndarray], num_dice: int, sides: int = 6) -> Union[float, np.ndarray]:
    """
    Avalia a funcao densidade de probabilidade normal correspondente a soma de num_dice dados.
    Funciona tanto para escalares (float) quanto para arrays do NumPy, sem depender do SciPy.
    """
    mu_1, var_1 = dice_parameters(sides)
    mean = num_dice * mu_1
    std = math.sqrt(num_dice * var_1)
    coeff = 1.0 / (std * math.sqrt(2.0 * math.pi))
    z = (x - mean) / std
    return coeff * np.exp(-0.5 * (z ** 2))


def numerical_gaussian_crossover(n: int, m: int, sides: int = 6, tol: float = 1e-15) -> float:
    """
    Encontra numericamente o ponto de intersecao positivo entre f_n(x) e f_m(x)
    no intervalo [mu_n, mu_m] usando o metodo da bissecao, de forma totalmente
    independente da formula algebrica fechada.
    """
    if n == m:
        mu_1, _ = dice_parameters(sides)
        return float(n * mu_1)

    if n > m:
        n, m = m, n

    mu_1, _ = dice_parameters(sides)
    low = n * mu_1
    high = m * mu_1

    for _ in range(100):
        mid = 0.5 * (low + high)
        diff = float(gaussian_pdf(mid, n, sides) - gaussian_pdf(mid, m, sides))
        if diff == 0.0 or (high - low) <= tol * max(1.0, mid):
            return mid
        if diff > 0:
            low = mid
        else:
            high = mid

    return 0.5 * (low + high)


def verify_gaussian_crossover(n: int, m: int, sides: int = 6) -> Dict[str, Union[int, float, bool]]:
    """
    Executa a verificacao tripla da formula fechada x*(n, m):
    1. Substituicao direta nas densidades normais: |f_n(x*) - f_m(x*)| ~ 0
    2. Comparacao com raiz numerica por bissecao: |x* - x_num| ~ 0
    3. Comparacao do teto ceil(x*) com a virada combinatoria discreta exata k_cross
    """
    if n > m:
        n, m = m, n

    summary = classical_means_summary(n, m, sides)
    x_star = summary["x_star"]
    mu_g = summary["geometric_mean"]
    mu_a = summary["arithmetic_mean"]

    fn_val = float(gaussian_pdf(x_star, n, sides))
    fm_val = float(gaussian_pdf(x_star, m, sides))
    density_residual = abs(fn_val - fm_val)

    x_num = numerical_gaussian_crossover(n, m, sides)
    root_error = abs(x_star - x_num)

    k_cross, p_n_cross, p_m_cross = discrete_crossover_point(n, m, sides)
    ceil_x_star = int(math.ceil(x_star))

    return {
        "n": n,
        "m": m,
        "mu_g": mu_g,
        "mu_a": mu_a,
        "x_star": x_star,
        "x_num": x_num,
        "root_error": root_error,
        "f_n_at_x_star": fn_val,
        "f_m_at_x_star": fm_val,
        "density_residual": density_residual,
        "ratio_x_star_to_mu_g": x_star / mu_g,
        "ceil_x_star": ceil_x_star,
        "k_cross": k_cross,
        "discrete_matches_ceil": ceil_x_star == k_cross,
        "p_n_at_k_cross": p_n_cross,
        "p_m_at_k_cross": p_m_cross,
    }

