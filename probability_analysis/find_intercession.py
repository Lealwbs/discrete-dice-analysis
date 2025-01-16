import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def monte_carlo_intersection(n, m, num_samples=100000, tolerance=1e-5):
    # Definir parâmetros das distribuições
    mu_n = n * 3.5
    sigma_n = np.sqrt(n) * np.sqrt(35 / 12)
    mu_m = m * 3.5
    sigma_m = np.sqrt(m) * np.sqrt(35 / 12)
    
    # Gerar valores de x no intervalo relevante
    x_min = min(n, m)
    x_max = max(6*n, 6*m)
    x_samples = np.linspace(x_min, x_max, num_samples)
    
    # Calcular densidades para cada ponto de x
    f_n = norm.pdf(x_samples, mu_n, sigma_n)
    f_m = norm.pdf(x_samples, mu_m, sigma_m)
    
    # Encontrar interseção: onde densidades são iguais
    intersection_points = []
    for x, y_n, y_m in zip(x_samples, f_n, f_m):
        if abs(y_n - y_m) <= tolerance:
            intersection_points.append((x, y_n))  # x = ponto de interseção, y_n = densidade
    
    return intersection_points


# Plotar as distribuições e interseções
def plot_distributions_with_intersections(n, m, intersections):
    mu_n = n * 3.5
    sigma_n = np.sqrt(n) * np.sqrt(35 / 12)
    mu_m = m * 3.5
    sigma_m = np.sqrt(m) * np.sqrt(35 / 12)

    x = np.linspace(min(n, m), max(6*n, 6*m), 1000)
    f_n = norm.pdf(x, mu_n, sigma_n)
    f_m = norm.pdf(x, mu_m, sigma_m)

    plt.plot(x, f_n, label=f'{n} dados')
    plt.plot(x, f_m, label=f'{m} dados')

    # Verifique se há interseções antes de usar scatter()
    if intersections:
        plt.scatter(*zip(*intersections), color='red', label='Interseções', zorder=5)
    else:
        print("Nenhuma interseção encontrada!")

    plt.title('Interseção entre distribuições normais')
    plt.xlabel('Soma')
    plt.ylabel('Densidade de probabilidade')
    plt.legend()
    plt.grid()
    plt.show()



# Exemplo: 2 dados e 3 dados
def plot_and_define_points(a,b):
    intersections = monte_carlo_intersection(a, b)
    print("Pontos de interseção encontrados:")
    for point in intersections:
        print(f"x = {point[0]:.2f}, y = {point[1]:.6f}")

    plot_distributions_with_intersections(a, b, intersections)

plot_and_define_points(2,3)
plot_and_define_points(2,4)
plot_and_define_points(3,4)