import matplotlib.pyplot as plt
import numpy as np

# Datos del problema (SIN MODIFICAR EL ORDEN)
diametro_inicial = 0.503  # in
longitud_calibrada = 2.00  # in  (Aunque no se use directamente para la deformación)
area_inicial = np.pi * (diametro_inicial / 2)**2  # Area transversal inicial

data = np.array([
    [0, 0],
    [1.50, 0.0005],
    [4.60, 0.0015],
    [8.00, 0.0025],
    [11.00, 0.0035],
    [11.80, 0.0050],
    [11.80, 0.0080],
    [12.00, 0.0200],
    [16.60, 0.0400],
    [20.00, 0.1000],
    [21.50, 0.2800],
    [19.50, 0.4000],
    [18.50, 0.4600]
])

carga_kips = data[:, 0]  # Carga en kips
deformacion = data[:, 1]  # Deformación unitaria (in/in) - YA ES UNITARIA


# Calcular Esfuerzo en ksi (kips por pulgada cuadrada)
esfuerzo_ksi = carga_kips / area_inicial


# --- Gráfica Esfuerzo-Deformación (Completa) ---
plt.figure(figsize=(10, 6))
plt.plot(deformacion, esfuerzo_ksi, marker='o', linestyle='-', label="Datos Experimentales")
plt.title('Diagrama Esfuerzo-Deformación')
plt.xlabel('Deformación (in/in)')
plt.ylabel('Esfuerzo (ksi)')
plt.grid(True)

# Escalas para la gráfica completa
plt.xlim(0, 0.5)  # Ajustado para deformación
plt.ylim(0, 120)
plt.xticks(np.arange(0, 0.51, 0.05))
plt.yticks(np.arange(0, 121, 20))


# --- Región Elástica (Zoom) ---
plt.figure(figsize=(10, 6))
plt.plot(deformacion, esfuerzo_ksi, marker='o', linestyle='-', label="Datos Experimentales")
plt.title('Diagrama Esfuerzo-Deformación (Región Elástica)')
plt.xlabel('Deformación (in/in)')
plt.ylabel('Esfuerzo (ksi)')
plt.grid(True)

#  Escalas para la región elástica
plt.xlim(0, 0.005)
plt.ylim(0, 120)
plt.xticks(np.arange(0, 0.0051, 0.001))
plt.yticks(np.arange(0, 121, 20))



# --- Cálculo de Propiedades y Comparación de Módulos ---

# 1. Módulo de Young (E) y Comparación
print("--- Comparación de Módulos de Young ---")

# Lista para almacenar los módulos calculados
modulos = []

#  Iteramos sobre los puntos en la región elástica (hasta deformación ~0.004)
for i in range(1, len(deformacion)):
    if deformacion[i] > 0.004:
        break  # Salimos del bucle

    # Cálculo del módulo usando el punto actual y el origen (0,0)
    E_i = (esfuerzo_ksi[i] - esfuerzo_ksi[0]) / (deformacion[i] - deformacion[0])
    modulos.append(E_i)
    print(f"Módulo de Young (E) entre puntos 0 y {i}: {E_i:.2f} ksi")

# Calculamos un módulo promedio
E_promedio = np.mean(modulos)
print(f"\nMódulo de Young Promedio (hasta deformación 0.004): {E_promedio:.2f} ksi")

# Módulo de referencia (puntos 1 y 3)
p1_ind = 1
p2_ind = 3
E = (esfuerzo_ksi[p2_ind] - esfuerzo_ksi[p1_ind]) / (deformacion[p2_ind] - deformacion[p1_ind])
print(f"\nMódulo de Young (E) - Referencia (puntos {p1_ind} y {p2_ind}): {E:.2f} ksi")


# Ecuación de la recta (usando E de referencia)
b = esfuerzo_ksi[p1_ind] - E * deformacion[p1_ind]
print(f"Ecuación de la recta en la región elástica: Esfuerzo = {E:.2f} * Deformación + {b:.2f}")

# Dibujamos la línea
x_elastica = np.linspace(0, 0.005, 100)
y_elastica = E * x_elastica + b
plt.figure(2)
plt.plot(x_elastica, y_elastica, linestyle='--', color='purple', label=f"Recta Elástica (E={E:.2f} ksi)")


# 2. Esfuerzo de Cedencia (Sy)
deformacion_offset = 0.002
esfuerzo_cedencia = np.interp(deformacion_offset, deformacion, esfuerzo_ksi)
print(f"\nEsfuerzo de Cedencia (Sy): {esfuerzo_cedencia:.2f} ksi")

# Dibujamos la línea de offset
plt.figure(2)
plt.plot([0, deformacion_offset + (esfuerzo_ksi[p2_ind]-esfuerzo_ksi[p1_ind])/(E)], [0, esfuerzo_ksi[p2_ind]-esfuerzo_ksi[p1_ind]+ E * deformacion_offset], linestyle='--', color='red', label='Offset 0.2%')
plt.plot(deformacion_offset, esfuerzo_cedencia, marker='o', color='red')


# 3. Esfuerzo Último (Su)
esfuerzo_ultimo = np.max(esfuerzo_ksi)
print(f"Esfuerzo Último (Su): {esfuerzo_ultimo:.2f} ksi")
deformacion_en_su = deformacion[np.argmax(esfuerzo_ksi)]
plt.figure(1)
plt.plot(deformacion_en_su, esfuerzo_ultimo, marker = 'o', color = 'green')
plt.figure(2)
plt.plot(deformacion_en_su, esfuerzo_ultimo, marker = 'o', color = 'green')


# 4. Esfuerzo de Fractura (Sf)
esfuerzo_fractura = esfuerzo_ksi[-1]
print(f"Esfuerzo de Fractura (Sf): {esfuerzo_fractura:.2f} ksi")

plt.figure(1)
plt.plot(deformacion[-1], esfuerzo_fractura, marker='o', color='magenta')
plt.figure(2)
plt.plot(deformacion[-1], esfuerzo_fractura, marker='o', color='magenta')

plt.figure(1).legend()
plt.figure(2).legend()
plt.show()
