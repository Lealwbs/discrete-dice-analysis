import numpy as np
from math import pow, sqrt

def what_are_the_odds(sum_value, dices):
    # Verifica se a soma desejada é impossível com a quantidade de dados fornecida.
    if dices < 1 or sum_value < dices or sum_value > 6 * dices:
        return 0

    # Cria uma matriz de memoização para armazenar os resultados parciais.
    mem = np.zeros((dices, sum_value), dtype=np.int64)

    # Calcula o número de combinações e divide pela probabilidade total possível.
    n = what_are_the_odds_rec(sum_value, dices, mem)
    return n / pow(6, dices)

def what_are_the_odds_rec(sum_value, dices, mem):
    # Caso base: se restar apenas 1 dado, só há uma combinação possível se a soma estiver no intervalo válido.
    if dices == 1:
        return 1 if 1 <= sum_value <= 6 else 0

    n = 0
    dices_rem = dices - 1

    # Calcula os limites mínimos e máximos possíveis para a face do dado atual.
    min_face = max(sum_value - 6 * dices_rem, 1)
    max_face = min(sum_value - dices_rem, 6)

    # Itera por todos os valores possíveis para o dado atual.
    for i in range(min_face, max_face + 1):
        sum_rem = sum_value - i

        # Verifica se o resultado já foi calculado e armazenado na memoização.
        if mem[dices_rem - 1][sum_rem - 1] == 0:
            mem[dices_rem - 1][sum_rem - 1] = what_are_the_odds_rec(sum_rem, dices_rem, mem)

        n += mem[dices_rem - 1][sum_rem - 1]

    return n
