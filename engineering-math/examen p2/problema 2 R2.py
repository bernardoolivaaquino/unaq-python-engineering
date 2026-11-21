import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math # Usado para sqrt si se elige esa opción para r

# --- Datos Experimentales (Problema 2) ---
# Fuentes: [source: 26, 61-62] en los documentos PDF proporcionados.
f_values = np.array([7, 9, 15, 25, 40, 75, 100, 150])
k_values = np.array([0.29, 0.37, 0.48, 0.65, 0.80, 0.97, 0.99, 1.07])

# --- 1. Ajuste del Modelo ---
# Modelo de velocidad de crecimiento de saturación: k = k_max * f / (K + f)
# Fuentes: [source: 23, 59]
# Este es un modelo no lineal, por lo que usamos curve_fit.

# Definir la función del modelo para curve_fit
def saturation_model(f, k_max, K):
    """Modelo de crecimiento de saturación."""
    return k_max * f / (K + f)

# Estimaciones iniciales para los parámetros [k_max, K]
# k_max podría ser cercano al valor máximo de k observado.
# K es la constante de saturación media (valor de f donde k es k_max/2),
# podría estar en el rango medio de f.
k_max_guess = max(k_values)
K_guess = np.median(f_values) # Usar la mediana de f como una estimación inicial
initial_guess = [k_max_guess, K_guess]
print(f"Estimación Inicial para curve_fit: k_max ≈ {initial_guess[0]:.2f}, K ≈ {initial_guess[1]:.2f}")

# Límites para los parámetros (k_max y K deben ser positivos)
parameter_bounds = ([0, 0], [np.inf, np.inf]) # [k_max_min, K_min], [k_max_max, K_max]

try:
    # Realizar el ajuste no lineal usando mínimos cuadrados
    params, covariance = curve_fit(
        saturation_model,
        f_values,
        k_values,
        p0=initial_guess,
        bounds=parameter_bounds, # Aplicar límites
        maxfev=5000 # Incrementar número máximo de iteraciones si es necesario
    )

    # Extraer los parámetros ajustados
    k_max_fit, K_fit = params

    print("\n--- Resultados del Ajuste del Modelo ---")
    # Inciso 3: Obtener el valor de la constante k_max
    # Fuentes: [source: 28, 64] (similar para K)
    print(f"[Inciso 3] Constante k_max ajustada: {k_max_fit:8f}")
    # Inciso 2: Obtener el valor de la constante K
    # Fuentes: [source: 28, 64]
    print(f"[Inciso 2] Constante K ajustada: {K_fit:.8f}")

    # Calcular los valores de k predichos por el modelo ajustado
    k_pred = saturation_model(f_values, k_max_fit, K_fit)

    # --- 2. Calcular Métricas de Bondad de Ajuste (r y r²) ---
    # Inciso 5: Obtener el valor de r²
    # Fuentes: [source: 29, 65]
    # Fórmula: r² = 1 - (SS_res / SS_tot)
    residuals = k_values - k_pred
    ss_res = np.sum(residuals**2) # Suma de cuadrados de los residuales
    ss_tot = np.sum((k_values - np.mean(k_values))**2) # Suma total de cuadrados
    if ss_tot == 0:
        r2 = 1.0 # Caso perfecto o datos constantes
    else:
        r2 = 1 - (ss_res / ss_tot)
    print(f"[Inciso 5] Coeficiente de determinación r²: {r2:.8f}")

    # Inciso 4: Obtener el valor de r
    # Fuentes: [source: 28, 64]
    # r es el coeficiente de correlación. Se puede calcular como sqrt(r²)
    # o como la correlación entre los valores observados y predichos.
    # La segunda opción es generalmente preferible ya que preserva el signo (aunque aquí es positivo).
    r_corr = np.corrcoef(k_values, k_pred)[0, 1]
    # r_sqrt = math.sqrt(max(0, r2)) # Opción alternativa
    print(f"[Inciso 4] Coeficiente de correlación r (calculado con corrcoef): {r_corr:.8f}")
    # print(f"[Inciso 4] Coeficiente de correlación r (calculado como sqrt(r²)): {r_sqrt:.4f}")


    # --- 3. Graficar los Datos y el Modelo Ajustado ---
    plt.figure(figsize=(10, 6))
    plt.scatter(f_values, k_values, color='red', label='Datos Experimentales', zorder=5)
    # Generar puntos suaves para la curva del modelo
    f_plot = np.linspace(0, max(f_values) * 1.1, 200) # Empezar desde 0 para ver el origen
    k_plot = saturation_model(f_plot, k_max_fit, K_fit)
    plt.plot(f_plot, k_plot, color='blue', label=f'Modelo Ajustado\n$k = \\frac{{{k_max_fit:.3f} f}}{{{K_fit:.3f} + f}}$\n$r^2 = {r2:.4f}$')
    plt.xlabel("Concentración de sustrato, f (mg/L)")
    plt.ylabel("Tasa de crecimiento específico, k (1/día)")
    plt.title("Ajuste del Modelo de Crecimiento de Saturación Bacteriana")
    plt.legend()
    plt.grid(True)
    plt.ylim(bottom=0) # Asegurar que el eje y comience en 0
    plt.xlim(left=0)   # Asegurar que el eje x comience en 0
    plt.show()

    # --- 4. Integración Numérica ---
    # Usaremos la función k(f) con los parámetros ajustados k_max_fit y K_fit.

    def k_function_fit(f):
        """Función k(f) usando los parámetros ajustados."""
        # Evitar división por cero o valores no definidos si f=-K_fit
        # Dado que f (concentración) es >= 0 y K_fit > 0, no debería ocurrir.
        return k_max_fit * f / (K_fit + f)

    # Implementaciones revisadas de las reglas de integración

    def trapezoidal_rule(func, a, b, n):
        """Regla del Trapecio Compuesta."""
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = func(x)
        # Fórmula: (h/2) * [y₀ + 2(y₁ + ... + yₙ₋₁) + yₙ]
        integral = (h / 2) * (y[0] + 2 * np.sum(y[1:n]) + y[n])
        return integral

    def simpson_1_3_rule(func, a, b, n):
        """Regla de Simpson 1/3 Compuesta."""
        if n % 2 != 0:
            raise ValueError("n debe ser par para la regla de Simpson 1/3.")
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = func(x)
        # Fórmula: (h/3) * [y₀ + 4(y₁ + y₃ + ...) + 2(y₂ + y₄ + ...) + yₙ]
        integral = (h / 3) * (y[0] + 4 * np.sum(y[1:n:2]) + 2 * np.sum(y[2:n-1:2]) + y[n])
        return integral

    def simpson_3_8_rule(func, a, b, n):
        """Regla de Simpson 3/8 Compuesta."""
        if n % 3 != 0:
            raise ValueError("n debe ser múltiplo de 3 para la regla de Simpson 3/8.")
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = func(x)
        # Fórmula: (3h/8) * [y₀ + 3(y₁+y₂+y₄+y₅...) + 2(y₃+y₆+...) + yₙ]
        integral = y[0] + y[n] # Términos extremos
        for i in range(1, n):
            if i % 3 == 0: # Índices múltiplos de 3 (y₃, y₆, ...)
                integral += 2 * y[i]
            else: # Índices no múltiplos de 3 (y₁, y₂, y₄, y₅, ...)
                integral += 3 * y[i]
        integral *= (3 * h / 8)
        return integral

    print("\n--- Resultados de la Integración Numérica ---")
    n_integration = 6 # Número de subintervalos especificado en el problema

    # Inciso 6: Integral con método del trapecio [1, 40], n=6
    # Fuentes: [source: 30, 66]
    integral_trap = trapezoidal_rule(k_function_fit, 1, 40, n_integration)
    print(f"[Inciso 6] Integral Trapecio   [1, 40], n={n_integration}: {integral_trap:.8f}")

    # Inciso 7: Integral con método de Simpson 1/3 [1, 150], n=6
    # Fuentes: [source: 31, 67]
    # n=6 es par, válido para Simpson 1/3.
    integral_simpson_1_3 = simpson_1_3_rule(k_function_fit, 1, 150, n_integration)
    print(f"[Inciso 7] Integral Simpson 1/3 [1, 150], n={n_integration}: {integral_simpson_1_3:.8f}")

    # Inciso 8: Integral con método de Simpson 3/8 [1, 300], n=6
    # Fuentes: [source: 31, 68]
    # n=6 es múltiplo de 3, válido para Simpson 3/8.
    integral_simpson_3_8 = simpson_3_8_rule(k_function_fit, 1, 300, n_integration)
    print(f"[Inciso 8] Integral Simpson 3/8 [1, 300], n={n_integration}: {integral_simpson_3_8:.8f}")

except RuntimeError as e:
    print(f"\nError en el ajuste: {e}")
    print("El ajuste no convergió. Intenta ajustar las estimaciones iniciales (initial_guess) o los límites (bounds).")
except ValueError as e:
    print(f"\nError: {e}")
    print("Verifica los requisitos de 'n' para las reglas de Simpson.")
except Exception as e:
    print(f"\nOcurrió un error inesperado: {e}")