# Análise Probabilística da Soma de Dados Discretos: A Falácia da Distância da Média e a Emergência da Média Geométrica no Crossover de Distribuições

**Autor:** Ítalo Leal  
*Graduando em Sistemas de Informação — Universidade Federal de Minas Gerais (UFMG)*  
*Interlocução acadêmica:* Prof. Dr. Jeroen van de Graaf (*Departamento de Ciência da Computação — ICEx / UFMG*)  
*Disciplina de Origem:* Matemática Discreta  

---

## Resumo

Neste repositório investiga-se um problema probabilístico originado na Primeira Avaliação (P1) de Matemática Discreta da UFMG: determinar se a soma 8 é mais provável no lançamento de 2 dados ou de 3 dados de seis faces. Embora a conclusão intuitiva de muitos alunos tenha sido correta ($P(S_2 = 8) > P(S_3 = 8)$), a justificativa comumente apresentada — baseada na menor distância euclidiana entre o alvo e o valor esperado da distribuição — constitui uma falácia estatística formal. 

Demonstramos analiticamente a inconsistência do argumento aritmético através de contraexemplos rígidos (notadamente $2d$ vs $6d$) e derivamos a formulação fechada exata para o ponto de interseção contínuo (crossover de verossimilhança) via Teorema Central do Limite. Provamos que, para somas de variáveis independentes e identicamente distribuídas (i.i.d.), a invariância da razão média/variância anula o termo linear na razão de log-verossimilhança, revelando que a fronteira de decisão é governada pela **Média Geométrica** das esperanças corrigida pela **Média Logarítmica** e pelo **Coeficiente de Variação**.

---

## 1. Origem do Problema e a Questão da P1

Na prova de Matemática Discreta da UFMG, foi formulada a seguinte questão:

> **Problema:** *Considere o lançamento de dados honestos de 6 faces. O que é mais provável: obter soma 8 com 2 dados ou com 3 dados?*

As probabilidades exatas revelam:
- Para 2 dados ($S_2$): Há $5$ combinações favoráveis de um total de $6^2 = 36$ resultados possíveis:
  $$P(S_2 = 8) = \frac{5}{36} \approx 0.13889 \quad (13.89\%)$$
- Para 3 dados ($S_3$): Há $21$ combinações favoráveis de um total de $6^3 = 216$ resultados possíveis:
  $$P(S_3 = 8) = \frac{21}{216} = \frac{7}{72} \approx 0.09722 \quad (9.72\%)$$

Portanto, de fato é mais provável obter soma 8 com 2 dados do que com 3 dados.

### A Heurística dos Alunos
Uma parcela expressiva dos estudantes respondeu à questão sem calcular a contagem combinatória exata, aplicando o seguinte raciocínio métrico:
1. O valor esperado da soma de 2 dados é $E[S_2] = 2 \times 3.5 = 7$.
2. O valor esperado da soma de 3 dados é $E[S_3] = 3 \times 3.5 = 10.5$.
3. Para a soma alvo $X_0 = 8$:
   $$|X_0 - E[S_2]| = |8 - 7| = 1.0$$
   $$|X_0 - E[S_3]| = |8 - 10.5| = 2.5$$
4. Como $1.0 < 2.5$, argumentaram que, por $X_0 = 8$ estar "mais próximo do centro" da distribuição de 2 dados do que da de 3 dados, $2$ dados seria necessariamente a opção mais provável.

O professor Jeroen van de Graaf aceitou a resposta na correção ponderando o raciocínio criativo, ensejando um diálogo científico posterior sobre a validade e generalização desse princípio.

---

## 2. A Falácia da Distância Euclidiana da Média

A heurística de comparar distâncias aritméticas à esperança ($|X_0 - E[S_n]| < |X_0 - E[S_m]|$) assume quatro hipóteses falsas sobre as distribuições:

1. **Variâncias Idênticas:** Pressupõe que a dispersão em torno da média é igual para qualquer número de dados. No entanto, para $n$ variáveis i.i.d., a variância cresce linearmente:
   $$\text{Var}(S_n) = n \cdot \text{Var}(D) = n \cdot \frac{35}{12}$$
2. **Alturas Máximas Iguais:** Pressupõe que a probabilidade no pico (moda) é idêntica. Pelo Teorema Central do Limite, a altura máxima decai a uma taxa de $O(1/\sqrt{n})$:
   $$\max_k P(S_2 = k) = P(S_2 = 7) = \frac{6}{36} \approx 0.1667$$
   $$\max_k P(S_6 = k) = P(S_6 = 21) \approx 0.0928$$
3. **Ponto de Crossover no Ponto Médio Aritmético:** Para que a distância aritmética fosse um classificador ótimo, a fronteira onde $P(S_n = X) = P(S_m = X)$ teria de coincidir com a média aritmética das esperanças:
   $$X_{\text{aritmético}} = \frac{E[S_n] + E[S_m]}{2}$$

### Contraexemplo Formal: 2 Dados vs 6 Dados

Sejam $n = 2$ e $m = 6$ dados de 6 faces:
- $E[S_2] = 2 \times 3.5 = 7$
- $E[S_6] = 6 \times 3.5 = 21$
- Ponto médio aritmético das esperanças:
  $$X_m = \frac{7 + 21}{2} = 14.0$$

#### Teste no Ponto Médio ($X_0 = 14$):
Pela heurística dos alunos, em $X_0 = 14$ as distâncias são idênticas ($|14 - 7| = 7$ e $|14 - 21| = 7$), logo as probabilidades deveriam ser iguais.
- Probabilidade real de 2 dados: $P(S_2 = 14) = 0$ (o valor máximo de 2 dados é 12).
- Probabilidade real de 6 dados: $P(S_6 = 14) \approx 2.49\%$.

#### Teste em $X_0 = 13$:
Avalie a soma alvo $X_0 = 13$:
- Distância a $E[S_2]$: $|13 - 7| = 6$
- Distância a $E[S_6]$: $|13 - 21| = 8$

Como $6 < 8$, a heurística da distância afirma categoricamente que $13$ é **mais provável de ocorrer com 2 dados do que com 6 dados**.
No entanto:
$$P(S_2 = 13) = 0.0\% \quad \text{vs} \quad P(S_6 = 13) \approx 1.62\%$$
O evento é **impossível** com 2 dados, mas plenamente plausível com 6 dados. A heurística baseada na média aritmética, portanto, falha de forma absoluta.

---

## 3. Derivação Analítica Contínua: A Emergência da Média Geométrica

Pelo Teorema Central do Limite (TCL), à medida que o número de variáveis somadas cresce, a distribuição de probabilidade de $S_n$ converge rapidamente para uma distribuição normal contínua:
$$S_n \sim \mathcal{N}(\mu_n, \sigma_n^2)$$
com:
$$\mu_n = n \mu_1, \quad \sigma_n^2 = n \sigma_1^2$$
onde $\mu_1 = 3.5$ e $\sigma_1^2 = \frac{35}{12} \approx 2.9167$ para um dado de 6 faces.

Buscamos o ponto de corte $x^*$ no qual a densidade de probabilidade de $n$ dados se iguala à de $m$ dados ($m > n$):
$$f_n(x) = f_m(x)$$
$$\frac{1}{\sigma_n \sqrt{2\pi}} \exp\left( -\frac{(x - \mu_n)^2}{2\sigma_n^2} \right) = \frac{1}{\sigma_m \sqrt{2\pi}} \exp\left( -\frac{(x - \mu_m)^2}{2\sigma_m^2} \right)$$

Aplicando o logaritmo natural em ambos os lados:
$$-\ln \sigma_n - \frac{(x - \mu_n)^2}{2\sigma_n^2} = -\ln \sigma_m - \frac{(x - \mu_m)^2}{2\sigma_m^2}$$
$$\frac{(x - \mu_n)^2}{2\sigma_n^2} - \frac{(x - \mu_m)^2}{2\sigma_m^2} = \ln\left( \frac{\sigma_m}{\sigma_n} \right) = \frac{1}{2}\ln\left( \frac{m}{n} \right)$$

Substituindo $\mu_n = n\mu_1$, $\mu_m = m\mu_1$, $\sigma_n^2 = n\sigma_1^2$ e $\sigma_m^2 = m\sigma_1^2$:
$$\frac{(x - n\mu_1)^2}{n} - \frac{(x - m\mu_1)^2}{m} = \sigma_1^2 \ln\left( \frac{m}{n} \right)$$

Expandindo os binômios:
$$\frac{x^2 - 2n\mu_1 x + n^2\mu_1^2}{n} - \frac{x^2 - 2m\mu_1 x + m^2\mu_1^2}{m} = \sigma_1^2 \ln\left( \frac{m}{n} \right)$$
$$\left( \frac{1}{n} - \frac{1}{m} \right) x^2 - (2\mu_1 - 2\mu_1)x + \mu_1^2(n - m) = \sigma_1^2 \ln\left( \frac{m}{n} \right)$$

### Teorema do Cancelamento Linear em Somas I.I.D.
Observe que o coeficiente linear em $x$ se anula identicamente:
$$-2\mu_1 x - (-2\mu_1 x) = 0$$
Isso ocorre porque a razão entre média e variância de uma soma de variáveis i.i.d. é uma **invariante universal**:
$$\frac{E[S_n]}{\text{Var}(S_n)} = \frac{n\mu_1}{n\sigma_1^2} = \frac{\mu_1}{\sigma_1^2} \quad (\text{constante independente de } n)$$

Com o cancelamento do termo linear ($B = 0$), a equação quadrática simplifica-se para uma forma pura:
$$\left( \frac{m - n}{nm} \right) x^2 = \mu_1^2 (m - n) + \sigma_1^2 \ln\left( \frac{m}{n} \right)$$

Multiplicando ambos os lados por $\frac{nm}{m - n}$:
$$x^2 = nm \mu_1^2 + \sigma_1^2 nm \frac{\ln(m/n)}{m - n}$$
$$x^2 = (nm \mu_1^2) \left[ 1 + \frac{\sigma_1^2}{\mu_1^2} \frac{\ln(m/n)}{m - n} \right]$$

### A Relação Fundamental com Médias Clássicas

Definindo:
1. **Média Geométrica ($\mu_g$)** das esperanças:
   $$\mu_g = \sqrt{E[S_n] E[S_m]} = \sqrt{(n\mu_1)(m\mu_1)} = \mu_1 \sqrt{nm}$$
2. **Coeficiente de Variação ($CV$)** do dado individual:
   $$CV = \frac{\sigma_1}{\mu_1} \implies CV^2 = \frac{\sigma_1^2}{\mu_1^2} = \frac{35/12}{(7/2)^2} = \frac{5}{21} \approx 0.2381$$
3. **Média Logarítmica ($L(n, m)$)** entre $n$ e $m$:
   $$L(n, m) = \frac{m - n}{\ln(m) - \ln(n)}$$

Obtemos a equação fechada analítica exata para a raiz positiva:
$$\bbox[15px,border:2px solid #2980b9]{x^* = \mu_g \sqrt{1 + \frac{CV^2}{L(n, m)}}}$$

### Interpretação Epistemológica
A intuição empírica apresentada por Ítalo Leal ao professor — sugerindo que a fronteira real estaria associada à **Média Geométrica** e não à média aritmética — é matematicamente validada:
- A **Média Geométrica** ($\mu_g$) é rigorosamente o **termo assintótico dominante de ordem zero** da interseção.
- O termo $\sqrt{1 + \frac{CV^2}{L(n, m)}}$ funciona como um fator de correção estocástico induzido pela variabilidade relativa das distribuições.

---

## 4. Distribuição Discreta Combinatória Exata

No domínio discreto exato, a função de probabilidade da soma de $n$ dados de $s$ faces é obtida por funções geradoras:
$$G(x) = \left( \frac{x + x^2 + \dots + x^s}{s} \right)^n = \frac{x^n}{s^n} \left( \frac{1 - x^s}{1 - x} \right)^n$$

A expansão em séries fornece a fórmula de De Moivre–Laplace / Uspensky:
$$P(S_n = k) = \frac{1}{s^n} \sum_{j=0}^{\lfloor \frac{k - n}{s} \rfloor} (-1)^j \binom{n}{j} \binom{k - sj - 1}{n - 1}$$

### Comparação entre os Modelos

| Par de Dados | $E(nd)$ | $E(md)$ | Média Aritmética ($X_m$) | Média Geométrica ($\mu_g$) | Crossover Gaussiano Analítico ($x^*$) | Crossover Discreto Exato ($k_{\text{cross}}$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2d vs 3d** | 7.00 | 10.50 | 8.7500 | 8.5732 | **8.9775** | **k = 9** |
| **2d vs 4d** | 7.00 | 14.00 | 10.5000 | 9.8995 | **10.2998** | **k = 11** |
| **2d vs 6d** | 7.00 | 21.00 | 14.0000 | 12.1244 | **12.5145** | **k = 13** |
| **3d vs 4d** | 10.50 | 14.00 | 12.2500 | 12.1244 | **12.5327** | **k = 13** |
| **3d vs 6d** | 10.50 | 21.00 | 15.7500 | 14.8492 | **15.2522** | **k = 16** |

#### Conclusões da Tabela:
- Para **2d vs 3d**: A média aritmética prevê transição em 8.75, a geométrica em 8.57 e o crossover analítico em 8.98. No discreto, para somas $k \le 8$, $2$ dados domina; para $k \ge 9$, $3$ dados passa a ser mais provável.
- Para **2d vs 6d**: A média aritmética prevê transição em 14.00 (onde 2 dados já tem probabilidade zero!), enquanto a média geométrica prevê 12.12 e o analítico 12.51. No discreto, o crossover ocorre exatamente em $k = 13$.
- Em todos os casos, a aproximação $x^*$ baseada na média geométrica e logarítmica prediz com precisão o primeiro inteiro de transição ($\lceil x^* \rceil$ ou $\lfloor x^* \rceil$).

---

## 5. Estado da Arte e Pesquisa na Literatura

### O problema já foi solucionado anteriormente?
1. **No Contexto Geral de Estatística e Aprendizado de Máquina:**
   A igualdade de duas densidades normais é a fronteira de decisão da **Análise Discriminante Quadrática (QDA)** e do critério de razão de verossimilhança de **Neyman-Pearson** / Decisão Bayesiana sob custo uniforme. Nos livros-texto gerais, a equação resultante é resolvida genericamente pela fórmula quadrática de Bhaskara ($Ax^2 + Bx + C = 0$).
2. **A Propriedade Algébrica Específica para Somas I.I.D.:**
   A literatura raramente destaca que, para somas de variáveis i.i.d., o termo linear $B$ anula-se identicamente devido à constância da razão média/variância, colapsando a solução geral na forma fechada elegante expressa em termos da **Média Geométrica** e da **Média Logarítmica**. 
3. **No Contexto Didático da Matemática Discreta:**
   O problema é um exemplo pedagógico formidável de como heurísticas intuitivas de distância euclidiana (muito comuns em estudantes) podem produzir conclusões acidentalmente corretas a partir de premissas estatisticamente falsas.

---

## 6. Como Reproduzir e Executar o Código

Todas as instruções detalhadas de instalação de bibliotecas, execução de scripts e uso como pacote Python estão descritas no arquivo:

👉 **[Consulte o Guia de Uso (USAGE.md)](file:///c:/Users/Italo/Documents/Github/discrete-dice-analysis/USAGE.md)**

Comandos rápidos:
```bash
# Instalar dependências
pip install numpy scipy matplotlib

# Executar a análise da questão da P1 e contraexemplo formal
python main.py

# Comparar quaisquer quantidades de dados (ex: 2d vs 4d)
python main.py --compare 2 4

# Exibir os gráficos interativos com curvas de densidade e crossover
python main.py --p1 --plot
```

---

## 7. Referências Bibliográficas

1. **De Moivre, A.** (1718). *The Doctrine of Chances: Or, A Method of Calculating the Probability of Events in Play*. W. Pearson, London.
2. **Feller, W.** (1968). *An Introduction to Probability Theory and Its Applications*, Vol. 1 (3rd ed.). John Wiley & Sons.
3. **Carlson, B. C.** (1972). *The Logarithmic Mean*. The American Mathematical Monthly, 79(6), 615–618.
4. **Hogg, R. V., McKean, J., & Craig, A. T.** (2018). *Introduction to Mathematical Statistics* (8th ed.). Pearson.
5. **Uspensky, J. V.** (1937). *Introduction to Mathematical Probability*. McGraw-Hill Book Company, New York.
6. **van de Graaf, J.** *Notas de Aula de Matemática Discreta*. Departamento de Ciência da Computação (DCC), ICEx, Universidade Federal de Minas Gerais (UFMG).