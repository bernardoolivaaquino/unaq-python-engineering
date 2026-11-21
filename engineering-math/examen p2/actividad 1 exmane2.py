import math
import numpy as np
import matplotlib.pyplot as plt

# Datos de entrada
diametro = np.array([1, 2, 3, 1, 2, 3, 1, 2, 3])
pendiente = np.array([0.001, 0.001, 0.001, 0.01, 0.01, 0.01, 0.05, 0.05, 0.05])
flujo = np.array([1.4, 8.3, 24.2, 4.7, 28.9, 84.0, 11.1, 69.0, 200.0])

# Transformación logarítmica
log_diametro = np.log(diametro)
log_pendiente = np.log(pendiente)
log_flujo = np.log(flujo)

# Construir la matriz X (variables independientes)
X = np.vstack([np.ones(len(log_diametro)), log_diametro, log_pendiente]).T

# Calcular los coeficientes usando la fórmula de regresión lineal múltiple
XT = X.T
beta = np.linalg.inv(XT @ X) @ XT @ log_flujo

# Coeficientes del modelo
a = beta[0]  # ln(K)
b = beta[1]  # β₁
c = beta[2]  # β₂

print(f"Ecuación del modelo linealizado: ln(F) = {a:.3f} + {b:.3f} * ln(D) + {c:.3f} * ln(m)")

# Ecuación del modelo original
K = math.exp(a)
print(f"Ecuación del modelo original: F = {K:.3f} * D^({b:.3f}) * m^({c:.3f})")

# Función de predicción
def predecir_flujo(diametro, pendiente):
    log_diametro = math.log(diametro)
    log_pendiente = math.log(pendiente)
    log_flujo_predicho = a + b * log_diametro + c * log_pendiente
    flujo_predicho = math.exp(log_flujo_predicho)
    return flujo_predicho

# Predicciones
diametro_b = 2.5
pendiente_b = 0.025
flujo_predicho_b = predecir_flujo(diametro_b, pendiente_b)
print(f"Predicción para diámetro {diametro_b} ft y pendiente {pendiente_b} ft/ft: {flujo_predicho_b:.2f} ft³/s")

diametro_c = 1.6
pendiente_c = 0.035
flujo_predicho_c = predecir_flujo(diametro_c, pendiente_c)
print(f"Predicción para diámetro {diametro_c} ft y pendiente {pendiente_c} ft/ft: {flujo_predicho_c:.2f} ft³/s")

# Gráfica 1: Flujo vs. Diámetro (pendiente constante)
plt.figure()
for p in np.unique(pendiente):
    d_values = diametro[pendiente == p]
    f_values = flujo[pendiente == p]
    plt.plot(d_values, f_values, marker='o', label=f'Pendiente = {p}')
plt.xlabel('Diámetro (ft)')
plt.ylabel('Flujo (ft³/s)')
plt.title('Flujo vs. Diámetro (pendiente constante)')
plt.legend()
plt.grid(True)
plt.show()

# Gráfica 2: Flujo vs. Pendiente (diámetro constante)
plt.figure()
for d in np.unique(diametro):
    p_values = pendiente[diametro == d]
    f_values = flujo[diametro == d]
    plt.plot(p_values, f_values, marker='o', label=f'Diámetro = {d}')
plt.xlabel('Pendiente (ft/ft)')
plt.ylabel('Flujo (ft³/s)')
plt.title('Flujo vs. Pendiente (diámetro constante)')
plt.legend()
plt.grid(True)
plt.show()
