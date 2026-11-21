import numpy as np
import matplotlib.pyplot as plt

def simpson_13(func, a, b, n):
    """
    Calcula la integral definida de una función usando la regla de Simpson 1/3.

    Args:
        func: La función a integrar (definida como una función de Python).
        a: El límite inferior de integración.
        b: El límite superior de integración.
        n: El número de subintervalos (debe ser un número par).

    Returns:
        El valor aproximado de la integral, x, y.
    """

    if n % 2 != 0:
        raise ValueError("El número de subintervalos (n) debe ser par para la regla de Simpson 1/3.")

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)  # Genera puntos x0, x1, ..., xn
    y = func(x)

    # Fórmula de Simpson 1/3
    integral = (h / 3) * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2]) + y[-1])
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
n_values = [2, 3, 4]

for n in n_values:
    # Simpson 1/3 requiere n par. Hacemos la corrección:
    n_corrected = n if n % 2 == 0 else n + 1
    integral_approx, x, y = simpson_13(f, a, b, n_corrected)
    print(f"Integral (n={n}): {integral_approx:.6f}")
    if n % 2 != 0:
        print(f"(Se usó n={n_corrected} internamente para Simpson 1/3)")

    # Gráfica
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, 'b-', label='f(x)')

    # Dibujar las divisiones
    for i in range(n_corrected + 1):
        plt.plot([x[i], x[i]], [0, y[i]], 'k--')

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'Regla de Simpson 1/3 (n={n_corrected})')
    plt.legend()
    plt.grid(True)
    plt.show()
