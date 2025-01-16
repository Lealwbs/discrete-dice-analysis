import dice_odds as do
import matplotlib.pyplot as plt

def plot_unique_dice_probabilities(dices):
    # Calcula as probabilidades para todas as somas possíveis.
    min_sum = dices
    max_sum = 6 * dices
    probabilities = [do.what_are_the_odds(sum_value, dices) for sum_value in range(min_sum, max_sum + 1)]

    # Plota o gráfico.
    plt.figure(figsize=(10, 6))
    plt.bar(range(min_sum, max_sum + 1), probabilities, color='blue', alpha=0.7)
    plt.title(f'Probabilidades de soma com {dices} dado(s)')
    plt.xlabel('Soma')
    plt.ylabel('Probabilidade')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def plot_dice_probabilities_oldv1(*dices_list):
    plt.figure(figsize=(12, 8))

    # Para cada número de dados fornecido, calcula e plota as probabilidades.
    for dices in dices_list:
        min_sum = dices
        max_sum = 6 * dices
        probabilities = [do.what_are_the_odds(sum_value, dices) for sum_value in range(min_sum, max_sum + 1)]

        # Plota com linhas e pontos conectados.
        plt.plot(range(min_sum, max_sum + 1), probabilities, marker='o', label=f'{dices} dado(s)')

    # Configurações do gráfico.
    plt.title('Probabilidades de soma para diferentes quantidades de dados')
    plt.xlabel('Soma')
    plt.ylabel('Probabilidade')
    plt.legend(title='Quantidade de dados')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def plot_dice_probabilities_oldv2(*dices_list):
    plt.figure(figsize=(12, 8))

    max_y = 0
    probabilities_list = []

    # Para cada número de dados fornecido, calcula e plota as probabilidades.
    for dices in dices_list:
        min_sum = dices
        max_sum = 6 * dices
        probabilities = [do.what_are_the_odds(sum_value, dices) for sum_value in range(min_sum, max_sum + 1)]
        probabilities_list.append((range(min_sum, max_sum + 1), probabilities))

        # Plota com linhas e pontos conectados.
        plt.plot(range(min_sum, max_sum + 1), probabilities, marker='o', label=f'{dices} dado(s)')

        # Adiciona linha vertical na esperança.
        expected_value = dices * 3.5
        plt.axvline(x=expected_value, color='red', linestyle='--', alpha=0.7, label=f'Esperança {dices} dado(s)')

        # Atualiza o valor máximo de Y para uso posterior.
        max_y = max(max_y, max(probabilities))

    # Adiciona interseções entre gráficos.
    for i in range(len(probabilities_list)):
        for j in range(i + 1, len(probabilities_list)):
            x1, y1 = probabilities_list[i]
            x2, y2 = probabilities_list[j]

            for k in range(len(x1)):
                if x1[k] in x2:
                    index = list(x2).index(x1[k])
                    if abs(y1[k] - y2[index]) < 1e-6:  # Verifica interseção considerando precisão.
                        plt.scatter(x1[k], y1[k], color='purple', marker='x', zorder=5, label='Interseção')

    # Configurações do gráfico.
    plt.title('Probabilidades de soma para diferentes quantidades de dados')
    plt.xlabel('Soma')
    plt.ylabel('Probabilidade')
    plt.xticks(range(min(dices_list) * 1, max(dices_list) * 6 + 1, 1))
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.legend(title='Quantidade de dados')
    plt.ylim(0, max_y + 0.05)
    plt.show()

def plot_dice_probabilities(*dices_list, exibirMedias=False, exibirMediasText=False):
    if exibirMediasText:
        exibirMedias = True

    plt.figure(figsize=(12, 8))

    max_y = 0
    probabilities_list = []
    expected_values = []

    # Para cada número de dados fornecido, calcula e plota as probabilidades.
    for dices in dices_list:
        min_sum = dices
        max_sum = 6 * dices
        probabilities = [do.what_are_the_odds(sum_value, dices) for sum_value in range(min_sum, max_sum + 1)]
        probabilities_list.append((list(range(min_sum, max_sum + 1)), probabilities))

        # Plota com linhas e pontos conectados.
        plt.plot(range(min_sum, max_sum + 1), probabilities, marker='o', label=f'{dices} dado(s)')

        # Adiciona linha vertical na esperança.
        expected_value = dices * 3.5
        expected_values.append(expected_value)
        plt.axvline(x=expected_value, color='red', linestyle='-', alpha=0.3, label=f'Esperança {dices} dado(s)')

        # Atualiza o valor máximo de Y para uso posterior.
        max_y = max(max_y, max(probabilities))

    # Adiciona interseções entre gráficos.
    for i in range(len(probabilities_list)):
        for j in range(i + 1, len(probabilities_list)):
            x1, y1 = probabilities_list[i]
            x2, y2 = probabilities_list[j]

            for k in range(len(x1)):
                if x1[k] in x2:
                    index = x2.index(x1[k])
                    if abs(y1[k] - y2[index]) <= 0:  # Verifica interseção considerando precisão.
                        plt.scatter(x1[k], y1[k], color='purple', marker='x', zorder=5, label=f'Interseção {i} & {j}')

    # Se exibirMedias for verdadeiro, calcula e plota as médias.
    if exibirMedias:
        media_color = 'blue'
        for i in range(len(expected_values)):
            for j in range(i + 1, len(expected_values)):
                media = (expected_values[i] + expected_values[j]) / 2
                plt.axvline(x=media, color=media_color, linestyle=':', alpha=0.6)

                if exibirMediasText:
                    plt.text(media, (i + 1) * 0.02,
                             f'M({round(expected_values[i] / 3.5)},{round(expected_values[j] / 3.5)})',
                             rotation=90, verticalalignment='center', color=media_color, fontsize=10)

    # Configurações do gráfico.
    plt.title('Probabilidades de soma para diferentes quantidades de dados')
    plt.xlabel('Soma')
    plt.ylabel('Probabilidade')
    xticks_range = range(min(dices_list) * 1, max(dices_list) * 6 + 1, 1)
    plt.xticks(xticks_range)
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.legend(title='Quantidade de dados')
    plt.ylim(0, max_y + 0.05)
    plt.show()
