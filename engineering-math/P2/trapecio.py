import numpy as np

def trapecio_simple(func, a, b):
    """
    Calcula la integral definida de una función usando la regla del trapecio simple.

    Args:
        func: La función a integrar (definida como una función de Python).
        a: El límite inferior de integración.
        b: El límite superior de integración.

    Returns:
        El valor aproximado de la integral.
    """
    return (b - a) * (func(a) + func(b)) / 2

def trapecio_compuesto(func, a, b, n):
    """
    Calcula la integral definida de una función usando la regla del trapecio compuesta.

    Args:
        func: La función a integrar.
        a: Límite inferior de integración.
        b: Límite superior de integración.
        n: Número de subintervalos.

    Returns:
        Aproximación de la integral.
    """
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = func(x)
    return h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])


def f(x):
    """
    La función a integrar: 12x^2 - 1.5x^5 + 2
    """
    return 12 * x**2 - 1.5 * x**5 + 2


# Límites de integración
a = 0.4
b = 2.0

# --- Trapecio Simple (n=1) ---
integral_simple = trapecio_simple(f, a, b)
print(f"Integral (Trapecio Simple, n=1): {integral_simple:.6f}")


# --- Trapecio Compuesto (n=2 y n=4) ---
n_values = [2, 4]  # Usamos trapecio compuesto para n > 1

for n in n_values:
    integral_compuesta = trapecio_compuesto(f, a, b, n)
    print(f"Integral (Trapecio Compuesto, n={n}): {integral_compuesta:.6f}")

# --- Cálculo más preciso (para comparación, opcional) ---
from scipy.integrate import quad

integral_exacta, error = quad(f, a, b)
print(f"\nValor exacto (usando scipy.integrate.quad): {integral_exacta:.6f}")
print(f"Error estimado de la función quad: {error:.6e}")
