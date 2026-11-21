import math
import numpy as np
import matplotlib.pyplot as plt
import warnings

# --- Definición de las funciones originales ---
# Estas son las funciones matemáticas para las cuales calcularemos las derivadas.

def f_a(x):
    """Función polinómica: f(x) = x^3 - 8x + 12"""
    return x**3 - 8*x + 12

def f_b(x):
    """Función trigonométrica, logarítmica y exponencial: f(x) = sin(log(x)) + exp(0.5x)
       Nota: Esta función requiere x > 0 debido al logaritmo natural."""
    if x <= 0:
        # Manejo de error para dominio inválido
        # Devolver NaN (Not a Number) es útil para graficar, ya que matplotlib
        # generalmente ignora estos puntos o crea rupturas en la línea.
        warnings.warn(f"Dominio inválido para f_b: x={x} debe ser > 0.", RuntimeWarning)
        return np.nan
    return math.sin(math.log(x)) + math.exp(0.5*x)

def f_c(x):
    """Función trigonométrica compleja: f(x) = sin(x^2 + 3x) - cos(sin(x)/x^3)
       Nota: Esta función requiere x != 0 debido a la división por x^3."""
    if x == 0:
        warnings.warn(f"Dominio inválido para f_c: x={x} no puede ser 0.", RuntimeWarning)
        return np.nan
    # Manejo de posible división por cero si x es muy pequeño (aunque ya se filtró x=0)
    # y potencial inestabilidad numérica.
    try:
        term2 = math.cos(math.sin(x) / (x**3))
    except OverflowError:
        warnings.warn(f"OverflowError en f_c para x={x}. El término cos(sin(x)/x^3) es muy grande.", RuntimeWarning)
        return np.nan
    return math.sin(x**2 + 3*x) - term2


# --- Definición de las Fórmulas de Diferenciación Numérica ---
# Estas funciones implementan varias aproximaciones para calcular derivadas.
# Se basan en evaluar la función f en puntos cercanos a x, separados por una distancia h.

def forward_derivative(f, x, h):
    """
    Aproximación de la primera derivada usando diferencia hacia adelante.
    Fórmula: f'(x) ≈ [f(x + h) - f(x)] / h
    Orden de precisión: O(h)
    """
    try:
        return (f(x + h) - f(x)) / h
    except (ValueError, TypeError, ZeroDivisionError) as e:
        # Si f(x) o f(x+h) devuelven NaN o hay error, propagamos NaN
        # O si h fuera 0 (aunque no debería pasar con el valor fijo).
        # print(f"Error en forward_derivative en x={x}, h={h}: {e}") # Descomentar para depurar
        return np.nan

def centered_derivative(f, x, h):
    """
    Aproximación de la primera derivada usando diferencia centrada.
    Fórmula: f'(x) ≈ [f(x + h) - f(x - h)] / (2h)
    Orden de precisión: O(h^2) (generalmente más precisa que la hacia adelante)
    """
    try:
        return (f(x + h) - f(x - h)) / (2*h)
    except (ValueError, TypeError, ZeroDivisionError) as e:
        # print(f"Error en centered_derivative en x={x}, h={h}: {e}")
        return np.nan

def forward_high_precision(f, x, h):
    """
    Aproximación de la primera derivada hacia adelante con mayor precisión.
    Fórmula: f'(x) ≈ [-3f(x) + 4f(x + h) - f(x + 2h)] / (2h)
    Orden de precisión: O(h^2)
    """
    try:
        return (-3*f(x) + 4*f(x + h) - f(x + 2*h)) / (2*h)
    except (ValueError, TypeError, ZeroDivisionError) as e:
        # print(f"Error en forward_high_precision en x={x}, h={h}: {e}")
        return np.nan

def backward_second_high_precision(f, x, h):
    """
    Aproximación de la segunda derivada hacia atrás con alta precisión.
    Fórmula: f''(x) ≈ [2f(x) - 5f(x - h) + 4f(x - 2h) - f(x - 3h)] / h^2
    Orden de precisión: O(h^2)
    """
    try:
        return (2*f(x) - 5*f(x-h) + 4*f(x-2*h) - f(x-3*h)) / (h**2)
    except (ValueError, TypeError, ZeroDivisionError) as e:
        # print(f"Error en backward_second_high_precision en x={x}, h={h}: {e}")
        return np.nan

def backward_second_derivative(f, x, h):
    """
    Aproximación de la segunda derivada usando diferencia hacia atrás.
    Fórmula: f''(x) ≈ [f(x) - 2f(x - h) + f(x - 2h)] / h^2
    Orden de precisión: O(h)
    """
    try:
        return (f(x) - 2*f(x-h) + f(x-2*h)) / (h**2)
    except (ValueError, TypeError, ZeroDivisionError) as e:
        # print(f"Error en backward_second_derivative en x={x}, h={h}: {e}")
        return np.nan

def centered_second_high_precision(f, x, h):
    """
    Aproximación de la segunda derivada centrada con alta precisión.
    Fórmula: f''(x) ≈ [-f(x + 2h) + 16f(x + h) - 30f(x) + 16f(x - h) - f(x - 2h)] / (12h^2)
    Orden de precisión: O(h^4) (muy precisa para h pequeño si la función es suave)
    """
    try:
        return (-f(x + 2*h) + 16*f(x + h) - 30*f(x) + 16*f(x - h) - f(x - 2*h)) / (12*h**2)
    except (ValueError, TypeError, ZeroDivisionError) as e:
        # print(f"Error en centered_second_high_precision en x={x}, h={h}: {e}")
        return np.nan

def backward_third_high_precision(f, x, h):
    """
    Aproximación de la tercera derivada hacia atrás con alta precisión.
    Fórmula: f'''(x) ≈ [5f(x) - 18f(x - h) + 24f(x - 2h) - 14f(x - 3h) + 3f(x - 4h)] / (2h^3)
    Orden de precisión: O(h^2)
    """
    try:
        return (5*f(x) - 18*f(x - h) + 24*f(x - 2*h) - 14*f(x - 3*h) + 3*f(x - 4*h)) / (2*h**3)
    except (ValueError, TypeError, ZeroDivisionError) as e:
        # print(f"Error en backward_third_high_precision en x={x}, h={h}: {e}")
        return np.nan


# --- Parámetros de Cálculo y Graficación ---
x_point = 3   # Punto específico donde queremos el valor numérico de la derivada
h = 0.01      # Tamaño del paso. Un h más pequeño suele dar mejor precisión,
              # pero puede causar errores de redondeo si es demasiado pequeño.
              # Cambiado a 0.01 para mejorar precisión vs 0.1 original.

plot_range_radius = 2 # Radio alrededor de x_point para graficar (x_point ± plot_range_radius)
num_points_plot = 200 # Número de puntos para generar las gráficas (más puntos = curva más suave)

# Generar un array de valores de x para usar en las gráficas
# np.linspace crea un array de 'num_points_plot' números espaciados uniformemente
# entre x_point - plot_range_radius y x_point + plot_range_radius
x_values_for_plot = np.linspace(x_point - plot_range_radius, x_point + plot_range_radius, num_points_plot)

# --- Diccionarios para organizar funciones y métodos de derivada ---
functions_to_analyze = {'f_a': f_a, 'f_b': f_b, 'f_c': f_c}

derivative_methods = {
    "Primera derivada hacia adelante O(h)": forward_derivative,
    "Primera derivada centrada O(h^2)": centered_derivative,
    "Primera derivada adelante alta precisión O(h^2)": forward_high_precision,
    "Segunda derivada atrás O(h)": backward_second_derivative,
    "Segunda derivada atrás alta precisión O(h^2)": backward_second_high_precision,
    "Segunda derivada centrada alta precisión O(h^4)": centered_second_high_precision,
    "Tercera derivada atrás alta precisión O(h^2)": backward_third_high_precision
}

# Diccionario para guardar los resultados numéricos en el punto x_point
results_at_x_point = {}

# --- Bucle Principal: Calcular y Graficar Derivadas para cada Función ---
print(f"Iniciando cálculos y graficación para x={x_point} con h={h}")
print("="*60)

# Ignorar advertencias de RuntimeWarning (como las de dominio inválido) temporalmente
# para no llenar la consola, pero tenerlas en cuenta si las gráficas se ven raras.
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)

    for func_name, func_object in functions_to_analyze.items():
        print(f"\nProcesando función: {func_name}")
        results_at_x_point[func_name] = {}

        # Crear una nueva figura de Matplotlib para cada función original
        plt.figure(figsize=(14, 9)) # Tamaño de la figura (ancho, alto) en pulgadas

        # 1. Graficar la función original como referencia
        y_original = np.array([func_object(xv) for xv in x_values_for_plot])
        # Solo graficar si hay valores válidos (no todos NaN)
        if not np.all(np.isnan(y_original)):
             plt.plot(x_values_for_plot, y_original, label=f'{func_name}(x) Original', linestyle=':', linewidth=2.5, color='black', zorder=5)
        else:
            print(f"  Advertencia: No se pudo graficar la función original {func_name} en el rango [{x_values_for_plot[0]:.2f}, {x_values_for_plot[-1]:.2f}].")


        # Límites iniciales para el eje Y (se ajustarán dinámicamente)
        min_y, max_y = np.inf, -np.inf

        # 2. Calcular y graficar cada tipo de derivada
        for deriv_name, deriv_func in derivative_methods.items():

            # a) Calcular el valor de la derivada en el punto específico x_point
            value_at_x = deriv_func(func_object, x_point, h)
            results_at_x_point[func_name][deriv_name] = value_at_x
            # Imprimir inmediatamente el resultado numérico si es válido
            if not np.isnan(value_at_x):
                 print(f"  {deriv_name}: {value_at_x:.6f} (en x={x_point})")
            else:
                 print(f"  {deriv_name}: No se pudo calcular en x={x_point} (dominio inválido o error)")


            # b) Calcular los valores de la derivada en todo el rango para la gráfica
            # Usamos un list comprehension para aplicar la función derivada a cada x en el rango
            y_values_derivative = np.array([deriv_func(func_object, xv, h) for xv in x_values_for_plot])

            # c) Graficar la derivada si tiene puntos válidos
            # Comprobamos que no todos los valores calculados sean NaN
            if not np.all(np.isnan(y_values_derivative)):
                # Graficamos usando los valores x del plot y los valores y de la derivada calculada
                plt.plot(x_values_for_plot, y_values_derivative, label=deriv_name, linewidth=1.5)

                # Actualizar límites Y para ajustar la vista (ignorando NaN y Inf)
                valid_y = y_values_derivative[np.isfinite(y_values_derivative)]
                if len(valid_y) > 0:
                    min_y = min(min_y, np.min(valid_y))
                    max_y = max(max_y, np.max(valid_y))
            else:
                 print(f"  Advertencia: No se pudieron calcular puntos válidos para graficar '{deriv_name}' de {func_name}.")


        # 3. Configurar y mostrar la gráfica para la función actual
        plt.title(f"Función {func_name}(x) y sus Derivadas Numéricas (h={h})")
        plt.xlabel("x")
        plt.ylabel("Valor de la función / derivada")
        plt.grid(True, which='both', linestyle='--', linewidth=0.5) # Rejilla más detallada

        # Añadir una línea vertical en x_point para marcar el punto de interés
        plt.axvline(x=x_point, color='red', linestyle='-.', linewidth=1.5, label=f'x = {x_point}')

        # Ajustar límites del eje Y para mejorar visualización, añadiendo un margen
        if np.isfinite(min_y) and np.isfinite(max_y) and max_y > min_y :
             margin = (max_y - min_y) * 0.1 # 10% de margen
             plt.ylim(min_y - margin, max_y + margin)
        # Caso especial si todas las derivadas son constantes o rango muy pequeño
        elif np.isfinite(min_y):
             plt.ylim(min_y - 1, min_y + 1) # Rango pequeño alrededor del valor constante


        # Mostrar leyenda (lista de qué línea corresponde a qué derivada)
        # 'loc='best'' intenta encontrar la mejor ubicación para no tapar las líneas
        # 'fontsize='small'' reduce el tamaño de la fuente si hay muchas leyendas
        plt.legend(loc='best', fontsize='small')

        # Guardar la gráfica en un archivo (opcional)
        # plt.savefig(f"derivadas_{func_name}_h{h}.png", dpi=300)

        # Mostrar la gráfica en una ventana
        plt.show()


# --- Imprimir Resumen Final de Resultados Numéricos ---
print("\n" + "="*60)
print(f"Resumen de los valores numéricos calculados en x = {x_point} con h = {h}:")
print("="*60)

for func_name, deriv_values in results_at_x_point.items():
    print(f"\nResultados para {func_name}:")
    for deriv_name, value in deriv_values.items():
        if isinstance(value, (int, float)) and not np.isnan(value):
            # Usamos f-string formateado para mostrar 6 decimales
            print(f"  {deriv_name}: {value:.6f}")
        else:
            # Si el valor no es un número (es NaN o None), indicamos que no se calculó
            print(f"  {deriv_name}: No calculado/Inválido")
    print("-" * 30)

print("\nProceso completado.")
