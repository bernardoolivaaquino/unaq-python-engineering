import numpy as np
import math
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial

# Datos experimentales
f_values = np.array([7, 9, 15, 25, 40, 75, 100, 150])
k_values = np.array([0.29, 0.37, 0.48, 0.65, 0.80, 0.97, 0.99, 1.07])

# Ajuste del modelo k = k_max * f / (K + f)
def model(params, f):
    k_max, K = params
    return k_max * f / (K + f)

def residuals(params, f, k):
    return k - model(params, f)

# Ajuste por mínimos cuadrados
from numpy.linalg import lstsq
A = np.vstack([f_values / (K + f_values) for K in [1]]).T
params, _, _, _ = lstsq(A, k_values, rcond=None)
k_max = params[0]
K = 1  # Se debe ajustar mejor este valor

print(f"Constante K: {K}")
print(f"Constante k_max: {k_max}")

# Cálculo de r^2
k_pred = model([k_max, K], f_values)
ss_res = np.sum((k_values - k_pred) ** 2)
ss_tot = np.sum((k_values - np.mean(k_values)) ** 2)
r2 = 1 - (ss_res / ss_tot)
print(f"Coeficiente de determinación r²: {r2}")

# Gráfica del ajuste
f_plot = np.linspace(min(f_values), max(f_values), 100)
k_plot = model([k_max, K], f_plot)
plt.scatter(f_values, k_values, label="Datos experimentales", color="red")
plt.plot(f_plot, k_plot, label="Modelo ajustado", color="blue")
plt.xlabel("f (mg/L)")
plt.ylabel("k (1/día)")
plt.legend()
plt.show()

# Integración numérica
def trapezoidal_rule(func, a, b, n):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = func(x)
    return (h / 2) * (y[0] + 2 * np.sum(y[1:n]) + y[n])

def simpson_1_3_rule(func, a, b, n):
    if n % 2 == 1:
        n += 1  # Simpson 1/3 requiere un número par de intervalos
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = func(x)
    return (h / 3) * (y[0] + 4 * np.sum(y[1:n:2]) + 2 * np.sum(y[2:n-1:2]) + y[n])

def simpson_3_8_rule(func, a, b, n):
    if n % 3 != 0:
        n += 3 - (n % 3)  # Simpson 3/8 requiere múltiplo de 3 intervalos
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = func(x)
    return (3 * h / 8) * (y[0] + 3 * np.sum(y[1:n:3]) + 3 * np.sum(y[2:n-1:3]) + 2 * np.sum(y[3:n-2:3]) + y[n])

# Definir función de k para integración
def k_function(f):
    return k_max * f / (K + f)

# Cálculo de integrales
integral_trap = trapezoidal_rule(k_function, 1, 40, 6)
integral_simpson_1_3 = simpson_1_3_rule(k_function, 1, 150, 6)
integral_simpson_3_8 = simpson_3_8_rule(k_function, 1, 300, 6)

print(f"Integral con trapecio (1,40): {integral_trap}")
print(f"Integral con Simpson 1/3 (1,150): {integral_simpson_1_3}")
print(f"Integral con Simpson 3/8 (1,300): {integral_simpson_3_8}")
