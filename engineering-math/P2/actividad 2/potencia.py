import numpy as np
import matplotlib.pyplot as plt

# Datos de entrada (los mismos que proporciona la imagen)
x1 = np.array([-2.4, -1.5, -1, 0, 3, 3.5, 5, 5.5])
y1 = np.array([-27.3020, -6.5605, -1.2524, 0.3167, 54.9997, 86.5549, 250.4488, 333.2970])

x2 = np.array([-4, -3.4, -1, 0.5, 2, 2.8, 3.7, 6])
y2 = np.array([-15.6028, -8.1462, -0.4704, 0.8423, 1.7374, 1.7495, 2.2802, 2.6236])

def power_regression(x, y):
    """
    Calcula la regresión de potencia para los datos dados.

    Args:
        x: Matriz NumPy de valores x.
        y: Matriz NumPy de valores y.

    Returns:
        Una tupla que contiene:
            - a: Coeficiente 'a' en y = a * x^b
            - b: Coeficiente 'b' (exponente) en y = a * x^b
            - r_value: Coeficiente de correlación de Pearson.
            - r_squared: Coeficiente de determinación (R cuadrado).
            - y_pred: Matriz NumPy de valores y predichos usando el modelo de regresión de potencia.
    """

    # 1. Transformación logarítmica: el truco de la regresión de potencia
    #    Ajustar y = a * x^b  es equivalente a ajustar log(y) = log(a) + b * log(x)
    #    Si hacemos Y = log(y), A = log(a), y X = log(x), entonces tenemos una ecuación lineal: Y = A + b * X
    log_x = np.log(x)
    log_y = np.log(y)

    # 2. Regresión lineal en los datos transformados.
    # Usamos polyfit para la regresión lineal (polinomio de grado 1).
    b, A = np.polyfit(log_x, log_y, 1)  # b es la pendiente, A es la intersección en y
    a = np.exp(A)  # Recuerda que A = log(a), entonces a = e^A

    # 3. Hacer predicciones
    y_pred = a * (x ** b)

    # 4. Calcular el coeficiente de correlación (r) y R cuadrado
    n = len(x)
    sum_xy = np.sum(log_x * log_y)
    sum_x = np.sum(log_x)
    sum_y = np.sum(log_y)
    sum_x2 = np.sum(log_x**2)
    sum_y2 = np.sum(log_y**2)

    numerator = n * sum_xy - sum_x * sum_y
    denominator = np.sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))
    
    #Manejar el caso donde el denominador es cero
    if denominator == 0:
        r_value = 0  # o algún valor predeterminado que tenga sentido en tu contexto
    else:
        r_value = numerator / denominator

    r_squared = r_value**2

    return a, b, r_value, r_squared, y_pred



def plot_regression(x, y, y_pred, title, a, b, r_value, r_squared):
    """
    Traza los datos, la línea de regresión y muestra las estadísticas.
    """
    plt.figure(figsize=(10, 6))  # Crea una nueva figura.  Hazla un poco más grande.
    plt.scatter(x, y, color='blue', label='Datos reales')  # Puntos azules para los datos reales
    plt.plot(x, y_pred, color='red', label=f'Regresión de potencia: y = {a:.3f} * x^{b:.3f}') # Línea roja

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.legend()
    plt.grid(True)  # Añade una cuadrícula para facilitar la lectura.

    # Añade texto con las estadísticas en el gráfico
    plt.text(0.1, 0.9, f'r = {r_value:.3f}\nR^2 = {r_squared:.3f}',
             transform=plt.gca().transAxes,  # Esto coloca el texto en relación con los ejes
             bbox=dict(facecolor='white', alpha=0.8)) # Un cuadro blanco alrededor del texto

    plt.show()


# --- Ejecuta la regresión y traza los resultados para ambos conjuntos de datos ---

# MUY IMPORTANTE: Lidiar con valores de x <= 0.
# La regresión de potencia *requiere* valores de x estrictamente positivos
# porque estamos tomando logaritmos.  Debemos filtrar los puntos no positivos.

x1_pos = x1[x1 > 0]  # Conservar solo los valores positivos de x
y1_pos = y1[x1 > 0]  # Conservar los valores de y correspondientes.  Índice usando el MISMO filtro.

x2_pos = x2[x2 > 0]
y2_pos = y2[x2 > 0]


# Conjunto de datos 1
a1, b1, r_value1, r_squared1, y_pred1 = power_regression(x1_pos, y1_pos)
plot_regression(x1_pos, y1_pos, y_pred1, "Regresión de potencia - Conjunto de datos 1", a1, b1, r_value1, r_squared1)

# Conjunto de datos 2
a2, b2, r_value2, r_squared2, y_pred2 = power_regression(x2_pos, y2_pos)
plot_regression(x2_pos, y2_pos, y_pred2, "Regresión de potencia - Conjunto de datos 2", a2, b2, r_value2, r_squared2)

print(f"Conjunto de datos 1: a={a1:.4f}, b={b1:.4f}, r={r_value1:.4f}, R^2={r_squared1:.4f}")
print(f"Conjunto de datos 2: a={a2:.4f}, b={b2:.4f}, r={r_value2:.4f}, R^2={r_squared2:.4f}")
