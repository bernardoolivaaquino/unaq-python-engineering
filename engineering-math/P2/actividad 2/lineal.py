import numpy as np
import matplotlib.pyplot as plt

# Datos de entrada
data = {
    'X1': [-2.4, -1.5, -1, 0, 3, 3.5, 5, 5.5],
    'Y1': [-27.3020, -6.5605, -1.2524, 0.3167, 54.9997, 86.5549, 250.4488, 333.2970],
    'X2': [-4, -3.4, -1, 0.5, 2, 2.8, 3.7, 6],
    'Y2': [-15.6028, -8.1462, -0.4704, 0.8423, 1.7374, 1.7495, 2.2802, 2.6236]
}

def regression(x, y):
    """Realiza la regresión lineal y calcula métricas."""
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi**2 for xi in x)

    # Cálculo de la pendiente (m) y la intersección (b)
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    b = (sum_y - m * sum_x) / n

    # Cálculo de la línea de regresión
    y_pred = [m * xi + b for xi in x]

    # Cálculo del coeficiente de correlación (r)
    numerator = sum((xi - np.mean(x)) * (yi - np.mean(y)) for xi, yi in zip(x, y))
    denominator = np.sqrt(sum((xi - np.mean(x))**2 for xi in x) * sum((yi - np.mean(y))**2 for yi in y))
    r = numerator / denominator

    # Cálculo del coeficiente de determinación (r^2)
    r_squared = r**2

    return m, b, r, r_squared, y_pred

def plot_regression(x, y, y_pred, title):
    """Grafica los datos y la línea de regresión."""
    plt.scatter(x, y, label='Datos')
    plt.plot(x, y_pred, color='red', label='Regresión lineal')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.legend()
    plt.show()

# Regresión para el primer conjunto de datos (X1, Y1)
m1, b1, r1, r_squared1, y_pred1 = regression(data['X1'], data['Y1'])
print(f"Regresión para X1, Y1:\nPendiente (m): {m1}\nIntersección (b): {b1}\nCoeficiente de correlación (r): {r1}\nCoeficiente de determinación (r^2): {r_squared1}")
plot_regression(data['X1'], data['Y1'], y_pred1, 'Regresión lineal de X1 vs Y1')

# Regresión para el segundo conjunto de datos (X2, Y2)
m2, b2, r2, r_squared2, y_pred2 = regression(data['X2'], data['Y2'])
print(f"\nRegresión para X2, Y2:\nPendiente (m): {m2}\nIntersección (b): {b2}\nCoeficiente de correlación (r): {r2}\nCoeficiente de determinación (r^2): {r_squared2}")
plot_regression(data['X2'], data['Y2'], y_pred2, 'Regresión lineal de X2 vs Y2')
