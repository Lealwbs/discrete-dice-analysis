"""
Funções de visualização gráfica com Matplotlib.
"""

import math
import matplotlib.pyplot as plt
import numpy as np

try:
    from .crossover import dice_parameters, exact_gaussian_crossover, gaussian_pdf
    from .dice_odds import exact_dice_odds
except ImportError:
    from crossover import dice_parameters, exact_gaussian_crossover, gaussian_pdf
    from dice_odds import exact_dice_odds


def plot_discrete(num_dice: int, sides: int = 6):
    """
    Plota as probabilidades discretas em barras para uma quantidade de dados.
    """
    x = list(range(num_dice, sides * num_dice + 1))
    y = [exact_dice_odds(s, num_dice, sides) for s in x]

    plt.figure(figsize=(10, 5))
    plt.bar(x, y, color='#3498db', alpha=0.8, edgecolor='black', linewidth=0.8)
    plt.title(f'Probabilidades de Soma: {num_dice} dado(s) de {sides} faces')
    plt.xlabel('Soma')
    plt.ylabel('Probabilidade')
    plt.xticks(x)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


def plot_comparison(*dice_counts: int, sides: int = 6, show_means: bool = True):
    """
    Compara múltiplas distribuições de soma com esperanças e médias.
    """
    if not dice_counts:
        return

    plt.figure(figsize=(12, 7))
    mu_1, _ = dice_parameters(sides)

    for d in dice_counts:
        x = list(range(d, sides * d + 1))
        y = [exact_dice_odds(s, d, sides) for s in x]
        plt.plot(x, y, marker='o', markersize=4, label=f'{d} dados')

        exp_val = d * mu_1
        plt.axvline(x=exp_val, linestyle='--', alpha=0.35, label=f'E({d}d)={exp_val:.1f}')

    plt.title('Comparação de Distribuições de Soma de Dados')
    plt.xlabel('Soma')
    plt.ylabel('Probabilidade')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_crossover(n: int, m: int, sides: int = 6):
    """
    Plota o crossover analítico x* entre as curvas normais de n e m dados.
    """
    if n > m:
        n, m = m, n

    mu_1, var_1 = dice_parameters(sides)
    mu_n, std_n = n * mu_1, math.sqrt(n * var_1)
    mu_m, std_m = m * mu_1, math.sqrt(m * var_1)

    x_star = exact_gaussian_crossover(n, m, sides)
    y_star = gaussian_pdf(x_star, n, sides)

    x = np.linspace(min(n, m), max(sides * n, sides * m), 1000)
    f_n = gaussian_pdf(x, n, sides)
    f_m = gaussian_pdf(x, m, sides)

    plt.figure(figsize=(10, 6))
    plt.plot(x, f_n, label=f'{n} dados (E={mu_n:.1f})', color='#e67e22', lw=2)
    plt.plot(x, f_m, label=f'{m} dados (E={mu_m:.1f})', color='#2980b9', lw=2)

    plt.scatter([x_star], [y_star], color='#c0392b', s=80, zorder=5,
                label=f'Ponto de Encontro x* = {x_star:.2f}')
    plt.axvline(x=x_star, color='#c0392b', linestyle=':', alpha=0.7)

    plt.title(f'Ponto de Encontro Contínuo ({n}d vs {m}d)')
    plt.xlabel('Soma')
    plt.ylabel('Densidade')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
