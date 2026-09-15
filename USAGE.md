# Guia de Uso dos Códigos (USAGE)

Todos os módulos de cálculo e funções do projeto estão organizados dentro da pasta `src/`, mantendo a raiz limpa apenas com o ponto de entrada `main.py` e os documentos.

---

## 1. Dependências Necessárias

O projeto requer Python 3.8+ e as seguintes bibliotecas:

```bash
pip install numpy scipy matplotlib
```

---

## 2. Estrutura do Repositório

```text
discrete-dice-analysis/
├── main.py               # Ponto de entrada CLI (executável direto no terminal)
├── README.md             # Artigo e fundamentação teórica da pesquisa
├── USAGE.md              # Este guia de uso
├── LICENSE               # Licença MIT
└── src/                  # PASTA COM TODOS OS ARQUIVOS DE CÓDIGO (.py)
    ├── __init__.py       # Inicializador do pacote
    ├── dice_odds.py      # Cálculo combinatório exato (memoização e De Moivre)
    ├── crossover.py      # Cálculo analítico do ponto de encontro (x*), esperanças e médias
    ├── monte_carlo.py    # Simulação estocástica de Monte Carlo de alta performance
    └── plot.py           # Funções para gerar gráficos com Matplotlib
```

---

## 3. Como Executar no Terminal (`main.py`)

Você pode rodar as análises diretamente a partir da raiz:

### 3.1. Reproduzir a questão da P1 e o contraexemplo formal:
```bash
python main.py
```

### 3.2. Comparar quaisquer números de dados:
```bash
python main.py --compare 2 4
python main.py --compare 2 6
```

### 3.3. Exibir gráficos das curvas com o ponto de encontro:
```bash
python main.py --p1 --plot
```

---

## 4. Como Importar os Módulos nos Seus Próprios Scripts

Para criar novos scripts e experimentos, você pode importar os módulos da pasta `src/`:

### 4.1. Probabilidades Combinatórias Exatas (`src/dice_odds.py`):
```python
from src.dice_odds import exact_dice_odds, dice_distribution

# Probabilidade de soma 8 com 2 dados de 6 faces:
p2 = exact_dice_odds(sum_value=8, num_dice=2, sides=6)
print(f"P(2d = 8): {p2:.5f}")  # 0.13889 (5/36)

# Probabilidade de soma 8 com 3 dados de 6 faces:
p3 = exact_dice_odds(sum_value=8, num_dice=3, sides=6)
print(f"P(3d = 8): {p3:.5f}")  # 0.09722 (21/216)

# Distribuição completa para 3 dados:
dist = dice_distribution(num_dice=3, sides=6)
print(dist)
```

### 4.2. Ponto de Encontro Analítico e Médias (`src/crossover.py`):
```python
from src.crossover import exact_gaussian_crossover, discrete_crossover_point, dice_parameters

# Parâmetros de 1 dado justo de 6 faces (mu = 3.5, var = 35/12):
mu, var = dice_parameters(sides=6)

# Ponto de encontro analítico contínuo (x*) entre 2d e 3d:
x_star = exact_gaussian_crossover(n=2, m=3, sides=6)
print(f"Ponto de encontro analítico: {x_star:.4f}")  # 8.9775

# Ponto de transição real discreto (k_cross):
k_cross, p_2d, p_3d = discrete_crossover_point(n=2, m=3, sides=6)
print(f"Crossover discreto: k = {k_cross}")  # k = 9
```

### 4.3. Simulação de Monte Carlo (`src/monte_carlo.py`):
```python
from src.monte_carlo import monte_carlo_odds

# 100.000 lançamentos simulados:
prob_sim = monte_carlo_odds(target_sum=8, num_dice=3, num_rolls=100_000)
print(f"Monte Carlo P(3d = 8): {prob_sim:.5f}")
```

### 4.4. Gerar Gráficos com Matplotlib (`src/plot.py`):
```python
from src.plot import plot_discrete, plot_crossover, plot_comparison

# Gráfico de barras de 2 dados:
plot_discrete(num_dice=2, sides=6)

# Curvas de densidade e ponto de encontro entre 2 e 6 dados:
plot_crossover(n=2, m=6, sides=6)
```
