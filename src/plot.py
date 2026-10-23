"""
Geracao de graficos para comparacao de somas de dados e visualizacao do ponto de virada.
"""

import os
from typing import Optional
import matplotlib.pyplot as plt
import numpy as np

try:
    from .crossover import (
        classical_means_summary,
        dice_parameters,
        discrete_crossover_point,
        gaussian_pdf,
    )
    from .dice_odds import exact_dice_odds
except ImportError:
    from crossover import (
        classical_means_summary,
        dice_parameters,
        discrete_crossover_point,
        gaussian_pdf,
    )
    from dice_odds import exact_dice_odds


def plot_discrete(
    num_dice: int,
    sides: int = 6,
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    Plota a distribuicao de probabilidade discreta para uma quantidade fixa de dados.
    """
    x = list(range(num_dice, sides * num_dice + 1))
    y = [exact_dice_odds(s, num_dice, sides) for s in x]

    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.bar(x, y, color="#2b5c8f", alpha=0.85, edgecolor="#1b3b5c", linewidth=0.8)
    ax.set_title(f"Distribuição da soma para {num_dice} dado(s) de {sides} faces")
    ax.set_xlabel("Soma (k)")
    ax.set_ylabel("Probabilidade P(S = k)")
    ax.set_xticks(x)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


def plot_comparison(
    *dice_counts: int,
    sides: int = 6,
    show_means: bool = True,
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    Compara as distribuicoes discretas de varias quantidades de dados no mesmo grafico.
    """
    if not dice_counts:
        return

    fig, ax = plt.subplots(figsize=(11, 6))
    mu_1, _ = dice_parameters(sides)
    colors = ["#d95f02", "#1b9e77", "#7570b3", "#e7298a", "#66a61e", "#e6ab02"]

    for idx, d in enumerate(dice_counts):
        color = colors[idx % len(colors)]
        x = list(range(d, sides * d + 1))
        y = [exact_dice_odds(s, d, sides) for s in x]
        ax.plot(
            x,
            y,
            marker="o",
            markersize=4.5,
            linewidth=1.8,
            color=color,
            label=f"{d} dado(s) (E = {d * mu_1:.1f})",
        )

        if show_means:
            ax.axvline(x=d * mu_1, color=color, linestyle=":", alpha=0.55)

    ax.set_title("Distribuições de probabilidade para diferentes quantidades de dados")
    ax.set_xlabel("Soma (k)")
    ax.set_ylabel("Probabilidade exata P(S_n = k)")
    ax.grid(True, linestyle="--", alpha=0.45)
    ax.legend()
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


def plot_crossover(
    n: int,
    m: int,
    sides: int = 6,
    show_discrete: bool = True,
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    Plota as distribuicoes de n e m dados (discreta e aproximacao normal),
    destacando a media aritmetica, a media geometrica e o ponto de intersecao x*.
    """
    if n > m:
        n, m = m, n

    summary = classical_means_summary(n, m, sides)
    mu_n, mu_m = summary["e_n"], summary["e_m"]
    mu_a = summary["arithmetic_mean"]
    mu_g = summary["geometric_mean"]
    x_star = summary["x_star"]
    y_star = float(gaussian_pdf(x_star, n, sides))
    k_cross, _, _ = discrete_crossover_point(n, m, sides)

    x_cont = np.linspace(max(0.5, n - 1), sides * m + 1, 1000)
    f_n = gaussian_pdf(x_cont, n, sides)
    f_m = gaussian_pdf(x_cont, m, sides)

    fig, ax = plt.subplots(figsize=(10.5, 5.8))

    if show_discrete:
        k_n = list(range(n, sides * n + 1))
        p_n = [exact_dice_odds(k, n, sides) for k in k_n]
        k_m = list(range(m, sides * m + 1))
        p_m = [exact_dice_odds(k, m, sides) for k in k_m]

        ax.bar(
            [k - 0.16 for k in k_n],
            p_n,
            width=0.32,
            color="#d95f02",
            alpha=0.28,
            label=f"Discreto {n}d",
        )
        ax.bar(
            [k + 0.16 for k in k_m],
            p_m,
            width=0.32,
            color="#1f78b4",
            alpha=0.28,
            label=f"Discreto {m}d",
        )

    ax.plot(
        x_cont,
        f_n,
        color="#d95f02",
        linewidth=2.2,
        label=f"Normal {n}d (E = {mu_n:.1f})",
    )
    ax.plot(
        x_cont,
        f_m,
        color="#1f78b4",
        linewidth=2.2,
        label=f"Normal {m}d (E = {mu_m:.1f})",
    )

    ax.axvline(
        x=mu_a,
        color="#6c757d",
        linestyle="--",
        linewidth=1.5,
        label=f"Média Aritmética = {mu_a:.2f}",
    )
    ax.axvline(
        x=mu_g,
        color="#27ae60",
        linestyle="-.",
        linewidth=1.5,
        label=f"Média Geométrica = {mu_g:.2f}",
    )
    ax.axvline(
        x=x_star,
        color="#c0392b",
        linestyle=":",
        linewidth=1.9,
        label=f"Interseção Gaussiana x* = {x_star:.2f} (virada em k = {k_cross})",
    )
    ax.scatter([x_star], [y_star], color="#c0392b", s=70, zorder=6)

    if sides * m <= 24:
        ax.set_xticks(range(n, sides * m + 1))
    else:
        ax.set_xticks(range(n, sides * m + 1, 2))

    ax.set_title(f"Comparação entre {n} dados e {m} dados ({sides} faces)")
    ax.set_xlabel("Soma (k)")
    ax.set_ylabel("Probabilidade / Densidade")
    ax.grid(True, linestyle="--", alpha=0.45)
    ax.legend(loc="upper right", framealpha=0.92)
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


def generate_project_figures(
    assets_dir: str = "assets",
    paper_figures_dir: str = "paper/figures",
):
    """
    Gera e salva os graficos principais do projeto para o README e para o artigo em LaTeX.
    """
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(paper_figures_dir, exist_ok=True)

    for n, m in [(2, 3), (2, 5), (2, 6)]:
        plot_crossover(
            n,
            m,
            sides=6,
            show_discrete=True,
            save_path=os.path.join(assets_dir, f"crossover_{n}d_{m}d.png"),
            show=False,
        )
        plot_crossover(
            n,
            m,
            sides=6,
            show_discrete=True,
            save_path=os.path.join(paper_figures_dir, f"crossover_{n}d_{m}d.pdf"),
            show=False,
        )

    plot_comparison(
        1,
        2,
        3,
        4,
        5,
        6,
        sides=6,
        show_means=True,
        save_path=os.path.join(assets_dir, "distribuicoes_1d_a_6d.png"),
        show=False,
    )
    plot_comparison(
        1,
        2,
        3,
        4,
        5,
        6,
        sides=6,
        show_means=True,
        save_path=os.path.join(paper_figures_dir, "distribuicoes_1d_a_6d.pdf"),
        show=False,
    )
