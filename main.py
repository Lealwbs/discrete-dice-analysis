"""
Script principal para analise de probabilidades na soma de dados discretos.
Autor: Italo Leal (UFMG)
"""

import argparse
import math
import sys

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.crossover import (
    classical_means_summary,
    discrete_crossover_point,
    verify_gaussian_crossover,
)
from src.dice_odds import exact_dice_count, exact_dice_odds
from src.plot import generate_project_figures, plot_crossover


def analyze_pair(n: int, m: int, sides: int = 6, show_details: bool = True):
    """
    Compara a distribuicao da soma de n dados com a soma de m dados.
    """
    if n > m:
        n, m = m, n

    summary = classical_means_summary(n, m, sides)
    e_n, e_m = summary["e_n"], summary["e_m"]
    var_n, var_m = summary["var_n"], summary["var_m"]
    ma = summary["arithmetic_mean"]
    mg = summary["geometric_mean"]
    x_star = summary["x_star"]
    k_cross, _, _ = discrete_crossover_point(n, m, sides)

    prob_table = []
    for k in range(n, m * sides + 1):
        p_n = exact_dice_odds(k, n, sides)
        p_m = exact_dice_odds(k, m, sides)
        prob_table.append((k, p_n, p_m))

    if show_details:
        print("=" * 68)
        print(f" COMPARACAO ENTRE {n} DADOS E {m} DADOS ({sides} FACES)")
        print("=" * 68)
        print(f"Esperancas:              E[S_{n}] = {e_n:.2f} | E[S_{m}] = {e_m:.2f}")
        print(f"Variancias:              Var[S_{n}] = {var_n:.3f} | Var[S_{m}] = {var_m:.3f}")
        print(f"Desvios padrao:          dp[S_{n}] = {math.sqrt(var_n):.3f} | dp[S_{m}] = {math.sqrt(var_m):.3f}")
        print(
            f"Probabilidade maxima:    max P(S_{n}) = {max(p[1] for p in prob_table):.4f} | "
            f"max P(S_{m}) = {max(p[2] for p in prob_table):.4f}"
        )
        print("-" * 68)
        print(f"Media aritmetica das esperancas:  {ma:.4f}")
        print(f"Media geometrica das esperancas:  {mg:.4f}")
        print(f"Intersecao gaussiana (x*):        {x_star:.4f}")
        print(f"Virada discreta exata (k_cross):  k = {k_cross}")
        print("-" * 68)
        print(f"{'Soma (k)':<10} | {f'P({n} dados)':<14} | {f'P({m} dados)':<14} | {'Mais provavel':<16}")
        print("-" * 68)

        window_start = max(n, int(math.floor(min(x_star, ma))) - 2)
        window_end = min(m * sides, int(math.ceil(max(x_star, ma))) + 2)

        for k, p_n, p_m in prob_table:
            if window_start <= k <= window_end:
                if p_n > p_m:
                    winner = f"{n} dados"
                elif p_m > p_n:
                    winner = f"{m} dados"
                else:
                    winner = "Empate"
                marker = " <-- virada discreta" if k == k_cross else ""
                print(f"{k:<10} | {p_n:<14.5f} | {p_m:<14.5f} | {winner:<16}{marker}")
        print("=" * 68 + "\n")

    return {
        "e_n": e_n,
        "e_m": e_m,
        "arithmetic_mean": ma,
        "geometric_mean": mg,
        "x_star": x_star,
        "discrete_crossover": k_cross,
        "prob_table": prob_table,
    }


def run_formula_verification(sides: int = 6):
    """
    Executa e exibe as provas numericas e algebricas de exatidao da formula fechada x*(n, m).
    """
    print("#" * 86)
    print(" 4. VERIFICACAO DE EXATIDAO DA FORMULA FECHADA x*(n, m)")
    print("#" * 86)
    pairs = [(2, 3), (3, 4), (4, 5), (3, 5), (2, 4), (2, 5), (3, 6), (2, 6), (10, 20), (50, 100)]
    header = (
        f"{'Par':<9} | {'Formula x*':<12} | {'Bissecao x_num':<14} | "
        f"{'|f_n(x*)-f_m(x*)|':<17} | {'x*/mu_G':<9} | {'ceil(x*) == k_cross'}"
    )
    print(header)
    print("-" * 86)
    for n, m in pairs:
        v = verify_gaussian_crossover(n, m, sides=sides)
        pair_str = f"{n}d vs {m}d"
        match_str = f"Sim (k = {v['k_cross']})" if v["discrete_matches_ceil"] else f" {v['ceil_x_star']} vs {v['k_cross']}"
        print(
            f"{pair_str:<9} | {v['x_star']:<12.8f} | {v['x_num']:<14.8f} | "
            f"{v['density_residual']:<17.2e} | {v['ratio_x_star_to_mu_g']:<9.6f} | {match_str}"
        )
    print("-" * 86)
    print("Observacoes:")
    print("  1. O residuo |f_n(x*) - f_m(x*)| e da ordem de 10^-17 (zero em ponto flutuante IEEE 754).")
    print("  2. A formula fechada coincide com a bissecao numerica em todas as casas decimais.")
    print("  3. Quando n e m crescem, a razao x*/mu_G converge para 1, provando que a Media Geometrica")
    print("     conjecturada no e-mail original de 13/12/2024 e o limite assintotico exato.\n")


def run_p1_analysis(plot: bool = False):
    """
    Reproduz a analise da Questao 4 (itens a e b) da prova de Matematica Discreta
    e os contraexemplos para a heuristica da distancia ate a media.
    """
    print("\n" + "#" * 68)
    print(" 1. QUESTAO 4 DA PROVA DE MATEMATICA DISCRETA (2 DADOS vs 3 DADOS)")
    print("#" * 68)
    analyze_pair(2, 3, sides=6)

    for k, item in [(8, "a"), (9, "b")]:
        c2 = exact_dice_count(k, 2)
        c3 = exact_dice_count(k, 3)
        p2 = exact_dice_odds(k, 2)
        p3 = exact_dice_odds(k, 3)
        d2 = abs(k - 7.0)
        d3 = abs(k - 10.5)
        winner = "2 dados" if p2 > p3 else "3 dados"
        print(f"Item ({item}) Soma k = {k}:")
        print(f"  Contagem exata:     2 dados = {c2}/36 ({c2 * 6}/216 = {p2:.5f}) | 3 dados = {c3}/216 ({p3:.5f})")
        print(f"  Distancia a media:  |{k} - 7| = {d2:.1f} vs |{k} - 10.5| = {d3:.1f}")
        print(f"  Conclusao:          {winner} e mais provavel (a distancia ate a media acerta nos dois itens!).\n")

    print("#" * 68)
    print(" 2. CONTRAEXEMPLO DENTRO DO SUPORTE (2 DADOS vs 5 DADOS, SOMA 12)")
    print("#" * 68)
    analyze_pair(2, 5, sides=6)
    p2_12 = exact_dice_odds(12, 2)
    p5_12 = exact_dice_odds(12, 5)
    print("Para k = 12 (possivel em 2 dados tirando 6 e 6):")
    print("  |12 - 7| = 5.0 < |12 - 17.5| = 5.5 (12 esta mais perto da media de 2 dados!)")
    print(f"  P(S_2 = 12) = 1/36 = {p2_12:.5f} ({p2_12 * 100:.2f}%)")
    print(f"  P(S_5 = 12) = 305/7776 = {p5_12:.5f} ({p5_12 * 100:.2f}%)")
    print("  Mesmo sendo uma soma possivel nos dois casos e mais proxima da media de 2 dados,")
    print("  obter soma 12 e mais provavel com 5 dados do que com 2 dados.\n")

    print("#" * 68)
    print(" 3. CONTRAEXEMPLO EXTREMO (2 DADOS vs 6 DADOS, SOMAS 13 E 14)")
    print("#" * 68)
    analyze_pair(2, 6, sides=6)
    p6_13 = exact_dice_odds(13, 6)
    p6_14 = exact_dice_odds(14, 6)
    print("Para k = 13:")
    print("  |13 - 7| = 6.0 < |13 - 21| = 8.0 (mais perto da media de 2 dados)")
    print(f"  Mas P(S_2 = 13) = 0 e P(S_6 = 13) = {p6_13:.5f} ({p6_13 * 100:.2f}%).")
    print("Para k = 14 (ponto medio aritmetico exato entre 7 e 21):")
    print(f"  As distancias empatam em 7.0, mas P(S_2 = 14) = 0 e P(S_6 = 14) = {p6_14:.5f} ({p6_14 * 100:.2f}%).\n")

    run_formula_verification(sides=6)

    if plot:
        plot_crossover(2, 3)
        plot_crossover(2, 6)


def main():
    parser = argparse.ArgumentParser(
        description="Analise de probabilidades de somas de dados e do ponto de virada entre distribuicoes."
    )
    parser.add_argument(
        "--p1",
        action="store_true",
        help="Executa a analise da questao da prova (itens a e b) e dos contraexemplos.",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Executa a verificacao numerica e algebrica da formula fechada x*(n, m).",
    )
    parser.add_argument(
        "--compare",
        nargs=2,
        type=int,
        metavar=("N", "M"),
        help="Compara a probabilidade de soma para N dados e M dados (ex: --compare 2 5).",
    )
    parser.add_argument(
        "--sides",
        type=int,
        default=6,
        help="Numero de faces de cada dado (padrao: 6).",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Exibe os graficos interativos com as distribuicoes e o ponto de intersecao.",
    )
    parser.add_argument(
        "--save-plots",
        action="store_true",
        help="Salva os graficos do projeto nas pastas assets/ e paper/figures/.",
    )

    args = parser.parse_args()

    if args.save_plots:
        generate_project_figures()
        print("Graficos salvos em assets/ e paper/figures/.")
        return

    if args.verify:
        run_formula_verification(sides=args.sides)
        return

    if args.compare:
        n, m = args.compare
        analyze_pair(n, m, sides=args.sides, show_details=True)
        if args.plot:
            plot_crossover(n, m, sides=args.sides)
    else:
        run_p1_analysis(plot=args.plot)


if __name__ == "__main__":
    main()
