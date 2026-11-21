import matplotlib.pyplot as plt
import math
import numpy as np
import time

# --- Definición del Modelo de Ecuaciones Diferenciales ---
# (Sin cambios)
def model(t, y, alpha, beta, delta, gamma, epsilon, N):
    X, C, I = y
    denominator = N - I
    if np.abs(denominator) < 1e-10:
        denominator = np.sign(denominator) * 1e-10 if denominator != 0 else 1e-10

    interaction_term = alpha * (X * C / denominator) if denominator != 0 else 0
    dxdt = beta * C - interaction_term + epsilon * I
    dcdt = -beta * C + interaction_term - gamma * C + delta * I
    didt = gamma * C - I * (delta + epsilon)
    return np.array([dxdt, dcdt, didt])

# --- Implementaciones de Métodos Numéricos ---
def _prepare_time_steps(t0, b, h):
    """Helper para crear el array de tiempos asegurando que b esté incluido."""
    num_steps = int(np.ceil((b - t0) / h))
    t_values = np.linspace(t0, t0 + num_steps * h, num_steps + 1)
    if abs(t_values[-1] - b) > 1e-9 and t_values[-1] > b:
        t_values = t_values[t_values <= b]
        if abs(t_values[-1] - b) > 1e-9 :
             t_values = np.append(t_values, b)
    elif abs(t_values[-1] - b) > 1e-9 and t_values[-1] < b:
        t_values = np.append(t_values, b)
    t_values = np.unique(t_values)
    return t_values

# (Funciones euler_method, heun_method, improved_polygon_method,
#  ralston_method, rk3_method, rk4_method sin cambios aquí)
# Asegúrate de tener las definiciones completas aquí
def euler_method(f, y0, t0, b, h, params):
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0
    for i in range(len(t_values) - 1):
        t_current = t_values[i]; y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        dydt = f(t_current, y_current, *params)
        y_values[i+1] = y_current + current_h * dydt
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

def heun_method(f, y0, t0, b, h, params):
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0
    for i in range(len(t_values) - 1):
        t_current = t_values[i]; y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        k1 = f(t_current, y_current, *params)
        y_predictor = y_current + current_h * k1
        k2 = f(t_values[i+1], y_predictor, *params)
        y_values[i+1] = y_current + current_h * 0.5 * (k1 + k2)
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

def improved_polygon_method(f, y0, t0, b, h, params):
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0
    for i in range(len(t_values) - 1):
        t_current = t_values[i]; y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        k1 = f(t_current, y_current, *params)
        y_mid = y_current + 0.5 * current_h * k1
        k2 = f(t_current + 0.5 * current_h, y_mid, *params)
        y_values[i+1] = y_current + current_h * k2
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

def ralston_method(f, y0, t0, b, h, params):
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0
    for i in range(len(t_values) - 1):
        t_current = t_values[i]; y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        k1 = f(t_current, y_current, *params)
        y_3_4 = y_current + (3.0/4.0) * current_h * k1
        k2 = f(t_current + (3.0/4.0) * current_h, y_3_4, *params)
        y_values[i+1] = y_current + current_h * ((1.0/3.0) * k1 + (2.0/3.0) * k2)
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

def rk3_method(f, y0, t0, b, h, params):
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0
    for i in range(len(t_values) - 1):
        t_current = t_values[i]; y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        k1 = f(t_current, y_current, *params)
        k2 = f(t_current + 0.5 * current_h, y_current + 0.5 * current_h * k1, *params)
        k3 = f(t_values[i+1], y_current - current_h * k1 + 2 * current_h * k2, *params)
        y_values[i+1] = y_current + (current_h / 6.0) * (k1 + 4 * k2 + k3)
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

def rk4_method(f, y0, t0, b, h, params):
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0
    for i in range(len(t_values) - 1):
        t_current = t_values[i]; y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i] # Paso actual
        k1 = f(t_current, y_current, *params)
        k2 = f(t_current + 0.5 * current_h, y_current + 0.5 * current_h * k1, *params)
        k3 = f(t_current + 0.5 * current_h, y_current + 0.5 * current_h * k2, *params)
        k4 = f(t_values[i+1], y_current + current_h * k3, *params)
        y_values[i+1] = y_current + (current_h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

# --- Parámetros del Modelo y Condiciones Iniciales ---
alpha = 0.2
beta = 0.3
delta = 0.1
gamma = 0.6
epsilon = 0.35

t0 = 0.0
x0 = 1.0
c0 = 2.0
i0 = 1.0
y0 = np.array([x0, c0, i0])

b = 7.0

N = x0 + c0 + i0

params = (alpha, beta, delta, gamma, epsilon, N)

# --- Configuración de la Simulación ---
h_elegido = 0.5 # Paso de tiempo para todos los métodos
print(f"Ejecutando todos los métodos con h = {h_elegido}")

# --- Lista de Métodos a Ejecutar ---
metodos = [
    ("Euler", euler_method),
    ("Heun", heun_method),
    ("Polígono Mejorado", improved_polygon_method),
    ("Ralston", ralston_method),
    ("RK3", rk3_method),
    ("RK4", rk4_method)
]

# --- Diccionario para Almacenar Resultados ---
resultados = {}

# --- Ejecutar Todos los Métodos ---
print("Calculando soluciones para cada método...")
for nombre, funcion_metodo in metodos:
    print(f"  Ejecutando: {nombre}")
    t, X, C, I = funcion_metodo(model, y0, t0, b, h_elegido, params)
    resultados[nombre] = {'t': t.copy(), 'X': X.copy(), 'C': C.copy(), 'I': I.copy()}
print("Cálculos completados.")

# --- SECCIÓN DE GRAFICACIÓN ÚNICA (ESTILO POR MÉTODO) ---

print(f"\nGenerando gráfica única para X, C, I (estilo por método)...")
print("ADVERTENCIA: Esta gráfica puede ser difícil de interpretar.")

# Crear figura y UN solo eje
fig, ax = plt.subplots(1, 1, figsize=(14, 9))

# Definir estilos:
# Color: Se asignará uno por método usando un ciclo de color.
# Marcador: Se asignará uno por método.
# Estilo de línea: Se asignará uno por variable.
estilos_variable_linea = {
    'X': {'linestyle': '-'},  # Sólido para X
    'C': {'linestyle': '--'}, # Discontinuo para C
    'I': {'linestyle': ':'}   # Punteado para I
}
marcadores_metodo = {
    "Euler":             {'marker': 'o', 'markersize': 5},
    "Heun":              {'marker': 'v', 'markersize': 5},
    "Polígono Mejorado": {'marker': '^', 'markersize': 5},
    "Ralston":           {'marker': 's', 'markersize': 5},
    "RK3":               {'marker': 'd', 'markersize': 5},
    "RK4":               {'marker': None} # Sin marcador para RK4 (usualmente el más preciso)
}
variables_a_graficar = ['X', 'C', 'I']

# Obtener un ciclo de colores de matplotlib (usaremos tab10 que tiene 10 colores distintos)
colores = plt.cm.tab10(np.linspace(0, 1, len(metodos)))

# Iterar sobre cada método CON SU ÍNDICE para asignar color
for i, (nombre_metodo, res) in enumerate(resultados.items()):
    t_vals = res['t']
    color_metodo = colores[i] # Color asignado a este método
    marker_info = marcadores_metodo.get(nombre_metodo, {'marker': None}) # Marcador para este método

    # Iterar sobre cada variable (X, C, I) para este método
    for var_nombre in variables_a_graficar:
        y_vals = res[var_nombre]
        estilo_var = estilos_variable_linea[var_nombre] # Estilo de línea para esta variable

        # Crear etiqueta combinada
        etiqueta_combinada = f"{nombre_metodo} - {var_nombre}"

        # Graficar la línea para esta combinación
        ax.plot(t_vals, y_vals,
                label=etiqueta_combinada,
                linestyle=estilo_var['linestyle'], # Estilo de línea por VARIABLE
                marker=marker_info['marker'],      # Marcador por MÉTODO
                markersize=marker_info.get('markersize', None),
                color=color_metodo)                # Color por MÉTODO

# --- Configurar la Gráfica Única ---
ax.set_title(f"Comparación Múltiple (Color/Marcador por Método, Línea por Variable, h={h_elegido})")
ax.set_xlabel("Tiempo (t)")
ax.set_ylabel("Valor de las Variables")

# Añadir Leyenda y Rejilla (externa)
ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fontsize='small')
ax.grid(True)

# Ajustar el layout para dejar espacio a la leyenda externa
plt.tight_layout(rect=[0, 0, 0.80, 1]) # Ajustar 0.80 si es necesario

# Mostrar la gráfica
plt.show()

print("Gráfica mostrada.")