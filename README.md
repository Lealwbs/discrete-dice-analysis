# Dice Probabilities Calculator

## Descrição do Projeto

Este projeto tem como objetivo explorar a probabilidade de somas possíveis ao lançar diferentes quantidades de dados. O sistema utiliza cálculos combinatórios otimizados para determinar as chances de cada soma, e oferece representações gráficas para facilitar a compreensão dos resultados.

## Estrutura do Projeto

O projeto foi modularizado para facilitar a manutenção e expansão, e está organizado da seguinte forma:

- **`main.py`**: Ponto de entrada principal do programa. Contém exemplos de uso das funções principais para gerar gráficos e explorar diferentes listas de dados.
- **`dice_functions.py`**: Contém funções responsáveis por plotar gráficos de probabilidades e realizar cálculos relacionados a médias e interseções entre gráficos.
- **`dice_odds.py`**: Implementa as funções para cálculo das probabilidades de cada soma possível para uma quantidade específica de dados. Inclui otimizações com uso de memoização.

## Funcionalidades

### 1. Cálculo de Probabilidades

A função principal, `what_are_the_odds`, determina a probabilidade de uma soma específica para um número fixo de dados. Ela utiliza uma abordagem recursiva com memoização para otimizar o desempenho.

### 2. Visualização Gráfica

- Gráficos de barras para representar probabilidades de somas com uma quantidade fixa de dados.
- Gráficos de linhas para comparar probabilidades de diferentes números de dados em um único gráfico.
- Destaque para interseções entre gráficos e exibição de valores médios (esperança).

### 3. Configurações Avançadas

- **Exibição de médias**: Opção para calcular e mostrar médias entre diferentes quantidades de dados diretamente no gráfico.
- **Texto explicativo**: Exibição opcional de textos indicando médias calculadas dentro do gráfico.

## Exemplo de Uso

### `main.py`
```python
import dice_functions as df
from math import sqrt

if __name__ == "__main__":
    lista_numeros = [x for x in range(20)]
    lista_numeros2 = [4, 5, 6, 7]
    lista_numeros3 = [x**2 for x in range(5)]
    lista_numeros4 = [x for x in range(50) if round(sqrt(x)) ** 2 == x]
    df.plot_dice_probabilities(*lista_numeros, exibirMedias=False, exibirMediasText=False)
```

## Dependências

Certifique-se de ter os seguintes pacotes instalados:

- `numpy`
- `matplotlib`

Você pode instalá-los usando o pip:
```bash
pip install numpy matplotlib
```

## Estrutura de Pastas
```
.
├── main.py
├── dice_functions.py
├── dice_odds.py
└── README.md
```

## Contribuindo

Este projeto ainda está em construção. Contribuições são bem-vindas! Caso tenha sugestões ou encontre problemas, sinta-se à vontade para abrir uma issue ou enviar um pull request no repositório.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---