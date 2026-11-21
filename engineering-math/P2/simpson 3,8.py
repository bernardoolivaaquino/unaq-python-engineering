import numpy as np
import matplotlib.pyplot as plt

def simpson_3_8(func, a, b, n):
    """
    Calcula la integral definida de una función usando la regla de Simpson 3/8.

    Args:
        func: La función a integrar (definida como una función de Python).
        a: El límite inferior de integración.
        b: El límite superior de integración.
        n: El número de subintervalos (debe ser un múltiplo de 3).

    Returns:
        El valor aproximado de la integral, x, y.
    """

    if n % 3 != 0:
        raise ValueError("El número de subintervalos (n) debe ser un múltiplo de 3 para la regla de Simpson 3/8.")

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = func(x)

    # Fórmula de Simpson 3/8
    integral = (3 * h / 8) * (y[0] + 3 * np.sum(y[1:-1:3]) + 3 * np.sum(y[2:-1:3]) + 2 * np.sum(y[3:-1:3]) + y[-1])
    return integral, x, y  # También devuelve x e y para la gráfica


def f(x):
    """
    La función a integrar: 12x^2 - 1.5x^5 + 2
    """
    return 12 * x**2 - 1.5 * x**5 + 2


# Límites de integración
a = 0.4
b = 2.0

# Calcular la integral con diferentes valores de n
n_values = [3, 6, 9]  # Valores de n dados, que son múltiplos de 3

for n in n_values:
    integral_approx, x, y = simpson_3_8(f, a, b, n)
    print(f"Integral (n={n}): {integral_approx:.6f}")

    # Gráfica
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, 'b-', label='f(x)')

    # Dibujar las divisiones
    for i in range(n + 1):
        plt.plot([x[i], x[i]], [0, y[i]], 'k--')

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'Regla de Simpson 3/8 (n={n})')
    plt.legend()
    plt.grid(True)
    plt.show()


# --- Cálculo más preciso (para comparación, opcional) ---
from scipy.integrate import quad

integral_exacta, error = quad(f, a, b)
print(f"\nValor exacto (usando scipy.integrate.quad): {integral_exacta:.6f}")
print(f"Error estimado de la función quad: {error:.6e}")
