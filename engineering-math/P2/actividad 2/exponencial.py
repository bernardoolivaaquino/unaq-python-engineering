import numpy as np
import matplotlib.pyplot as plt

# Datos de entrada
x1 = np.array([-2.4, -1.5, -1, 0, 3, 3.5, 5, 5.5])
y1 = np.array([-27.3020, -6.5605, -1.2524, 0.3167, 54.9997, 86.5549, 250.4488, 333.2970])
x2 = np.array([-4, -3.4, -1, 0.5, 2, 2.8, 3.7, 6])
y2 = np.array([-15.6028, -8.1462, -0.4704, 0.8423, 1.7374, 1.7495, 2.2802, 2.6236])

def regresion_exponencial(x, y):
    """
    Realiza una regresión exponencial y calcula los coeficientes.

    Args:
        x (np.array): Datos de la variable independiente.
        y (np.array): Datos de la variable dependiente.

    Returns:
        tuple: (a, b) coeficientes de la regresión exponencial (y = a * exp(b*x)).
    """
    # El error estaba aquí:  np.log() no puede manejar valores negativos o cero.
    # Solución: Filtramos los valores donde y <= 0
    mask = y > 0
    x_filtered = x[mask]
    y_filtered = y[mask]
    log_y = np.log(y_filtered)
    b = (len(x_filtered) * np.sum(x_filtered * log_y) - np.sum(x_filtered) * np.sum(log_y)) / (len(x_filtered) * np.sum(x_filtered**2) - np.sum(x_filtered)**2)
    a = np.exp(np.mean(log_y) - b * np.mean(x_filtered))
    return a, b

def calcular_coeficientes(x, y, a, b):
    """
    Calcula el coeficiente de correlación y el coeficiente de determinación.

    Args:
        x (np.array): Datos de la variable independiente.
        y (np.array): Datos de la variable dependiente.
        a (float): Coeficiente a de la regresión exponencial.
        b (float): Coeficiente b de la regresión exponencial.

    Returns:
        tuple: (r, r2) coeficiente de correlación y coeficiente de determinación.
    """
    y_pred = a * np.exp(b * x)
    # Correlación solo entre valores donde la predicción es válida (y original > 0)
    mask = y > 0
    r = np.corrcoef(y[mask], y_pred[mask])[0, 1]
    r2 = r**2
    return r, r2

def graficar_regresion(x, y, a, b, titulo):
    """
    Grafica los datos y la regresión exponencial.

    Args:
        x (np.array): Datos de la variable independiente.
        y (np.array): Datos de la variable dependiente.
        a (float): Coeficiente a de la regresión exponencial.
        b (float): Coeficiente b de la regresión exponencial.
        titulo (str): Título del gráfico.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, label='Datos')
    x_range = np.linspace(min(x), max(x), 100)
    y_pred = a * np.exp(b * x_range)
    plt.plot(x_range, y_pred, color='red', label='Regresión Exponencial')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.show()

# Regresión exponencial para el primer conjunto de datos
a1, b1 = regresion_exponencial(x1, y1)
r1, r2_1 = calcular_coeficientes(x1, y1, a1, b1)
print("Conjunto de datos 1:")
print(f"y = {a1:.4f} * exp({b1:.4f} * x)")
print(f"Coeficiente de correlación (r): {r1:.4f}")
print(f"Coeficiente de determinación (r^2): {r2_1:.4f}")
graficar_regresion(x1, y1, a1, b1, 'Regresión Exponencial (Conjunto 1)')

# Regresión exponencial para el segundo conjunto de datos
a2, b2 = regresion_exponencial(x2, y2)
r2, r2_2 = calcular_coeficientes(x2, y2, a2, b2)
print("\nConjunto de datos 2:")
print(f"y = {a2:.4f} * exp({b2:.4f} * x)")
print(f"Coeficiente de correlación (r): {r2:.4f}")
print(f"Coeficiente de determinación (r^2): {r2_2:.4f}")
graficar_regresion(x2, y2, a2, b2, 'Regresión Exponencial (Conjunto 2)')
