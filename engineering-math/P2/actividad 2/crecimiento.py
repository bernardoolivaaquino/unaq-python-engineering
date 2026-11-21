import numpy as np
import matplotlib.pyplot as plt

def exponential_regression_with_offset(x, y):
    """
    Regresión de crecimiento exponencial con un desplazamiento: y = a * exp(b * x) + offset

    Args:
        x: Valores x.
        y: Valores y.

    Returns:
        Tupla: (a, b, offset, r_value, r_squared, y_predicted).
    """

    # 1. Calcular el desplazamiento (offset)
    offset = 0  # Inicializa el desplazamiento
    if np.min(y) <= 0:
        offset = -np.min(y) + 1e-6  # Agrega un pequeño valor para evitar log(0)

    y_shifted = y + offset   # Aplica el desplazamiento

    # 2. Transformación logarítmica
    log_y = np.log(y_shifted)

    # 3. Regresión lineal (igual que antes, pero con y_shifted)
    n = len(x)
    sum_x = np.sum(x)
    sum_log_y = np.sum(log_y)
    sum_x_squared = np.sum(x * x)
    sum_x_log_y = np.sum(x * log_y)

    b = (n * sum_x_log_y - sum_x * sum_log_y) / (n * sum_x_squared - sum_x * sum_x)
    ln_a = (sum_log_y - b * sum_x) / n
    a = np.exp(ln_a)

    # 4. Predicciones (con ajuste de desplazamiento)
    y_predicted = a * np.exp(b * x) + offset  # ¡IMPORTANTE: Suma el desplazamiento de nuevo!

    # 5. Métricas (R y R^2)
    # Calcular r usando los datos con desplazamiento. Es mejor usar los valores originales.
    mean_y = np.mean(y)
    mean_log_y_shifted = np.mean(log_y)

    numerator = np.sum((x - np.mean(x)) * (log_y - mean_log_y_shifted))
    denominator_x = np.sqrt(np.sum((x-np.mean(x))**2))
    denominator_log_y = np.sqrt(np.sum((log_y - mean_log_y_shifted)**2))

    r_value = numerator/(denominator_x * denominator_log_y)

    # R-cuadrado. Usamos los valores *originales* de y, y y_predicted *con* el desplazamiento.
    ss_res = np.sum((y - y_predicted)**2)
    ss_tot = np.sum((y - mean_y)**2)
    r_squared = 1 - (ss_res / ss_tot)

    return a, b, offset, r_value, r_squared, y_predicted



def plot_regression(x, y, y_predicted, title):
    # Igual que antes. No hay cambios aquí.
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='blue', label='Datos originales')
    plt.plot(x, y_predicted, color='red', label='Regresión exponencial')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# --- Datos de ejemplo y ejecución ---

# Conjunto de datos 1
x1 = np.array([-2.4, -1.5, -1, 0, 3, 3.5, 5, 5.5])
y1 = np.array([-27.3020, -6.5605, -1.2524, 0.3167, 54.9997, 86.5549, 250.4488, 333.2970])

# Conjunto de datos 2
x2 = np.array([-4, -3.4, -1, 0.5, 2, 2.8, 3.7, 6])
y2 = np.array([-15.6028, -8.1462, -0.4704, 0.8423, 1.7374, 1.7495, 2.2802, 2.6236])
# --- Usar la nueva función ---

a1, b1, offset1, r_value1, r_squared1, y_predicted1 = exponential_regression_with_offset(x1, y1)
print("Conjunto de datos 1:")
print(f"  a = {a1:.4f}")
print(f"  b = {b1:.4f}")
print(f"  Offset = {offset1:.4f}")  # Imprime el desplazamiento
print(f"  r = {r_value1:.4f}")
print(f"  R^2 = {r_squared1:.4f}")
plot_regression(x1, y1, y_predicted1, "Regresión Exponencial (con desplazamiento) - Conjunto de datos 1")

a2, b2, offset2, r_value2, r_squared2, y_predicted2 = exponential_regression_with_offset(x2, y2)
print("\nConjunto de datos 2:")
print(f"  a = {a2:.4f}")
print(f"  b = {b2:.4f}")
print(f"  Offset = {offset2:.4f}") # Imprime el desplazamiento
print(f"  r = {r_value2:.4f}")
print(f"  R^2 = {r_squared2:.4f}")
plot_regression(x2, y2, y_predicted2, "Regresión Exponencial (con desplazamiento) - Conjunto de datos 2")
