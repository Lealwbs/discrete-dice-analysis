"""
Ponto de Entrada Principal para Análise e Pesquisa: Discrete Dice Analysis
Autor: Ítalo Leal (UFMG)
Contexto: Investigação do problema da P1 de Matemática Discreta (DCC/ICEx/UFMG)
"""

import argparse
import math
import sys

# Configuração de encoding para suporte robusto a UTF-8 no terminal Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.dice_odds import exact_dice_odds
from src.crossover import (
    dice_parameters,
    exact_gaussian_crossover,
    discrete_crossover_point,
)
from src.plot import plot_crossover, plot_comparison


def analyze_pair(n: int, m: int, sides: int = 6, show_details: bool = True):
    """
    Realiza a comparação completa e rigorosa entre a soma de n dados e m dados.
    """
    if n > m:
        n, m = m, n

    mu_1, var_1 = dice_parameters(sides)

    e_n = n * mu_1
    e_m = m * mu_1
    var_n = n * var_1
    var_m = m * var_1

    # Médias
    ma = (e_n + e_m) / 2.0
    mg = math.sqrt(e_n * e_m)
    x_star = exact_gaussian_crossover(n, m, sides)
    discrete_crossover, _, _ = discrete_crossover_point(n, m, sides)

    prob_table = []
    for k in range(n, m * sides + 1):
        p_n = exact_dice_odds(k, n, sides)
        p_m = exact_dice_odds(k, m, sides)
        prob_table.append((k, p_n, p_m))

    if show_details:
        print("=" * 65)
        print(f" COMPARACAO ESTATISTICA: {n}d{sides} vs {m}d{sides}")
        print("=" * 65)
        print(f"* Esperancas (Medias):         E({n}d) = {e_n:.2f} | E({m}d) = {e_m:.2f}")
        print(f"* Variancias:                  Var({n}d) = {var_n:.3f} | Var({m}d) = {var_m:.3f}")
        print(f"* Desvios Padrao:              sigma({n}d) = {math.sqrt(var_n):.3f} | sigma({m}d) = {math.sqrt(var_m):.3f}")
        print(f"* Altura dos Picos:            P_max({n}d) = {max(p[1] for p in prob_table):.4f} | P_max({m}d) = {max(p[2] for p in prob_table):.4f}")
        print("-" * 65)
        print(f"* Ponto Medio Aritmetico (MA):  {ma:.4f}  <- Heuristica falha da distancia euclidiana")
        print(f"* Media Geometrica (MG):        {mg:.4f}  <- Heuristica aproximada (Italo Leal)")
        print(f"* Ponto de Encontro Exato (x*): {x_star:.4f}  (Formula fechada: MG + Media Logaritmica)")
        print(f"* Ponto de Crossover Discreto:  k = {discrete_crossover} (primeiro k onde P({m}d) >= P({n}d))")
        print("-" * 65)
        print(f"{'Soma (k)':<10} | {f'P({n} dados)':<14} | {f'P({m} dados)':<14} | {'Mais Provavel':<15}")
        print("-" * 65)

        # Exibir janela ao redor do ponto de transição
        window_start = max(n, int(math.floor(x_star)) - 2)
        window_end = min(m * sides, int(math.ceil(x_star)) + 3)

        for k, p_n, p_m in prob_table:
            if window_start <= k <= window_end:
                winner = f"{n} dados" if p_n > p_m else (f"{m} dados" if p_m > p_n else "Empate")
                marker = " <== Crossover Discreto" if k == discrete_crossover else ""
                print(f"{k:<10} | {p_n:<14.5f} | {p_m:<14.5f} | {winner:<15}{marker}")
        print("=" * 65 + "\n")

    return {
        'e_n': e_n, 'e_m': e_m,
        'arithmetic_mean': ma,
        'geometric_mean': mg,
        'x_star': x_star,
        'discrete_crossover': discrete_crossover,
        'prob_table': prob_table
    }


def run_p1_analysis(plot: bool = False):
    """
    Reproduz e analisa formalmente os casos da P1 de Matemática Discreta da UFMG:
    1) Caso da Prova: 2d vs 3d (Soma 8)
    2) Contraexemplo Formal: 2d vs 6d (Somas 13 e 14)
    """
    print("\n" + "#" * 65)
    print(" CASO 1: QUESTAO ORIGINAL DA P1 (2 DADOS vs 3 DADOS, SOMA = 8)")
    print("#" * 65)
    analyze_pair(2, 3, sides=6)

    p2_8 = exact_dice_odds(8, 2)
    p3_8 = exact_dice_odds(8, 3)
    print(f"-> Para X0 = 8:")
    print(f"   Distancia a E(2d)=7:    |8 - 7| = 1.0")
    print(f"   Distancia a E(3d)=10.5: |8 - 10.5| = 2.5")
    print(f"   Probabilidades reais:   P(S2 = 8) = {p2_8:.5f} ({p2_8*100:.2f}%)")
    print(f"                           P(S3 = 8) = {p3_8:.5f} ({p3_8*100:.2f}%)")
    print(f"   Resultado: 2 dados e mais provavel ({p2_8:.5f} > {p3_8:.5f}).")
    print(f"   Nota: Os alunos acertaram a conclusao, mas a explicacao pela distancia da media e falaciosa!\n")

    print("#" * 65)
    print(" CASO 2: CONTRAEXEMPLO FORMAL (2 DADOS vs 6 DADOS, SOMAS 13 E 14)")
    print("#" * 65)
    analyze_pair(2, 6, sides=6)

    p2_13 = exact_dice_odds(13, 2)
    p6_13 = exact_dice_odds(13, 6)
    p2_14 = exact_dice_odds(14, 2)
    p6_14 = exact_dice_odds(14, 6)

    print("-> Por que a heuristica da distancia da media falha categoricamente:")
    print("   E(2d) = 7 | E(6d) = 21 | Ponto Medio Aritmetico MA = 14.0")
    print(f"   Para X0 = 13:")
    print(f"     |13 - 7| = 6 < |13 - 21| = 8  (Mais perto da esperanca de 2 dados!)")
    print(f"     Probabilidades: P(S2=13) = {p2_13:.5f} (0%) vs P(S6=13) = {p6_13:.5f} ({p6_13*100:.2f}%)")
    print(f"     A heuristica diria 2 dados, mas 2 dados e IMPOSSIVEL e 6 dados tem ~1.62% de chance!")
    print(f"   Para X0 = 14 (Ponto Medio Aritmetico Exato):")
    print(f"     |14 - 7| = |14 - 21| = 7  (Distancias identicas!)")
    print(f"     Probabilidades: P(S2=14) = {p2_14:.5f} (0%) vs P(S6=14) = {p6_14:.5f} ({p6_14*100:.2f}%)")
    print(f"     No ponto medio exato, as probabilidades NAO sao iguais (0% vs 2.49%)!\n")

    if plot:
        print("Exibindo graficos de comparacao...")
        plot_crossover(2, 3)
        plot_crossover(2, 6)


def main():
    parser = argparse.ArgumentParser(
        description="Discrete Dice Analysis: Estudo e Pesquisa sobre Probabilidades, Falacia da Esperanca e Ponto de Encontro Analitico."
    )
    parser.add_argument("--p1", action="store_true", help="Executa a analise completa da questao da P1 e o contraexemplo formal.")
    parser.add_argument("--compare", nargs=2, type=int, metavar=('N', 'M'), help="Compara a probabilidade de soma para N dados e M dados (ex: --compare 2 4).")
    parser.add_argument("--sides", type=int, default=6, help="Numero de faces dos dados (padrao: 6).")
    parser.add_argument("--plot", action="store_true", help="Exibe o grafico de densidades com o ponto de encontro.")

    args = parser.parse_args()

    if args.compare:
        n, m = args.compare
        analyze_pair(n, m, sides=args.sides, show_details=True)
        if args.plot:
            plot_crossover(n, m, sides=args.sides)
    else:
        # Padrão: executa a análise da P1
        run_p1_analysis(plot=args.plot)


if __name__ == "__main__":
    main()
