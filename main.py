import dice_functions as df
from math import sqrt

if __name__ == "__main__":
    lista_numeros = [x for x in range(20)]
    lista_numeros2 = [4, 5, 6, 7]
    lista_numeros3 = [x**2 for x in range(5)]
    lista_numeros4 = [x for x in range(50) if round(sqrt(x)) ** 2 == x]
    df.plot_dice_probabilities(*lista_numeros, exibirMedias=False, exibirMediasText=False)



