import matplotlib # Aunque no se use para graficar aquí, lo dejamos por si acaso
import math
import numpy as np
import time # Para medir el tiempo de cálculo de la referencia

# --- Definición del Modelo de Ecuaciones Diferenciales ---
# dX/dt = beta*C - alpha*(X*C / (N - I)) + epsilon*I
# dC/dt = -beta*C + alpha*(X*C / (N - I)) - gamma*C + delta*I
# dI/dt = gamma*C - I*(delta + epsilon)
# N = X + C + I (Constante)

def model(t, y, alpha, beta, delta, gamma, epsilon, N):
    """
    Define el sistema de EDOs.
    t: tiempo actual
    y: array [X, C, I]
    alpha, beta, delta, gamma, epsilon, N: parámetros del modelo
    """
    X, C, I = y

    denominator = N - I
    # Pequeña salvaguarda para evitar división por cero o valores muy pequeños
    if np.abs(denominator) < 1e-10:
        # print(f"Advertencia: Denominador (N-I)={denominator:.2e} cercano a cero en t={t:.4f}. Usando +/-1e-10.")
        denominator = np.sign(denominator) * 1e-10 if denominator != 0 else 1e-10

    # Asegurarse de que X, C, I no sean negativos si el modelo lo requiere físicamente
    # X = max(0, X)
    # C = max(0, C)
    # I = max(0, I)
    # y = np.array([X, C, I]) # Actualizar y si se modificaron los valores

    # Cálculo de las derivadas
    interaction_term = alpha * (X * C / denominator) if denominator != 0 else 0 # Evitar NaN si X o C son 0

    dxdt = beta * C - interaction_term + epsilon * I
    dcdt = -beta * C + interaction_term - gamma * C + delta * I
    didt = gamma * C - I * (delta + epsilon)

    return np.array([dxdt, dcdt, didt])

# --- Implementaciones de Métodos Numéricos ---

def _prepare_time_steps(t0, b, h):
    """Helper para crear el array de tiempos asegurando que b esté incluido."""
    num_steps = int(np.ceil((b - t0) / h)) # Usar ceil para asegurar que cubrimos hasta b
    t_values = np.linspace(t0, t0 + num_steps * h, num_steps + 1)

    # Asegurar que el último punto no exceda b significativamente y que b esté presente si es necesario
    if abs(t_values[-1] - b) > 1e-9 and t_values[-1] > b:
        # Si el último punto excede b, lo reemplazamos por b
        t_values = t_values[t_values <= b]
        if abs(t_values[-1] - b) > 1e-9 : # Si b no quedó exacto, lo añadimos
             t_values = np.append(t_values, b)
    elif abs(t_values[-1] - b) > 1e-9 and t_values[-1] < b:
         # Si el último punto es menor que b, añadimos b
        t_values = np.append(t_values, b)
    # Eliminar duplicados si b coincidió con un paso anterior
    t_values = np.unique(t_values)
    return t_values

def euler_method(f, y0, t0, b, h, params):
    """Método de Euler Explícito."""
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i] # Paso actual, puede variar al final
        dydt = f(t_current, y_current, *params)
        y_values[i+1] = y_current + current_h * dydt
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

def heun_method(f, y0, t0, b, h, params):
    """Método de Heun (RK2, Predictor-Corrector)."""
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        # Predictor (Euler step)
        k1 = f(t_current, y_current, *params)
        y_predictor = y_current + current_h * k1
        # Corrector
        k2 = f(t_values[i+1], y_predictor, *params)
        y_values[i+1] = y_current + current_h * 0.5 * (k1 + k2)
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

def improved_polygon_method(f, y0, t0, b, h, params):
    """Método del Polígono Mejorado (Punto Medio, RK2)."""
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        # Pendiente en el punto inicial
        k1 = f(t_current, y_current, *params)
        # Estimar valor en el punto medio del intervalo
        y_mid = y_current + 0.5 * current_h * k1
        # Pendiente en el punto medio estimado
        k2 = f(t_current + 0.5 * current_h, y_mid, *params)
        # Usar la pendiente del punto medio para avanzar
        y_values[i+1] = y_current + current_h * k2
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

def ralston_method(f, y0, t0, b, h, params):
    """Método de Ralston (RK2)."""
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        k1 = f(t_current, y_current, *params)
        # Estimar valor a 3/4 del intervalo usando k1
        y_3_4 = y_current + (3.0/4.0) * current_h * k1
        # Pendiente en t + 3/4 h
        k2 = f(t_current + (3.0/4.0) * current_h, y_3_4, *params)
        # Combinación ponderada de pendientes
        y_values[i+1] = y_current + current_h * ((1.0/3.0) * k1 + (2.0/3.0) * k2)
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

def rk3_method(f, y0, t0, b, h, params):
    """Método de Runge-Kutta de Orden 3 (clásico)."""
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        k1 = f(t_current, y_current, *params)
        k2 = f(t_current + 0.5 * current_h, y_current + 0.5 * current_h * k1, *params)
        # Nota: El argumento del tiempo para k3 es t_{i+1} = t_current + current_h
        k3 = f(t_values[i+1], y_current - current_h * k1 + 2 * current_h * k2, *params)
        y_values[i+1] = y_current + (current_h / 6.0) * (k1 + 4 * k2 + k3)
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

def rk4_method(f, y0, t0, b, h, params):
    """Método de Runge-Kutta de Orden 4 (clásico)."""
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i] # Paso actual

        k1 = f(t_current, y_current, *params)
        k2 = f(t_current + 0.5 * current_h, y_current + 0.5 * current_h * k1, *params)
        k3 = f(t_current + 0.5 * current_h, y_current + 0.5 * current_h * k2, *params)
        # Nota: El argumento del tiempo para k4 es t_{i+1} = t_current + current_h
        k4 = f(t_values[i+1], y_current + current_h * k3, *params)
        # Combinación de las pendientes
        y_values[i+1] = y_current + (current_h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]


def get_reference_solution(f, y0, t0, b, params, h_ref_factor=100):
    """
    Calcula una solución de alta precisión usando RK4 con un paso muy pequeño.
    h_ref_factor: El paso de referencia será h_elegido / h_ref_factor.
    """
    # Usar un paso significativamente más pequeño que el h_elegido típico
    # Estimamos un h_elegido común (ej. 0.5) para calcular h_ref si no se proporciona h_elegido
    h_typical = 0.5
    h_ref = h_typical / h_ref_factor
    print(f"\nCalculando solución de referencia usando RK4 con h = {h_ref:.5f}...")
    start_time = time.time()
    # Usamos rk4_method directamente
    t_ref, X_ref, C_ref, I_ref = rk4_method(f, y0, t0, b, h_ref, params)
    end_time = time.time()
    print(f"Solución de referencia calculada en {end_time - start_time:.2f} segundos.")
    return t_ref, X_ref, C_ref, I_ref

# --- Parámetros del Modelo y Condiciones Iniciales ---
alpha = 0.2
beta = 0.3
delta = 0.1
gamma = 0.6
epsilon = 0.35

t0 = 0.0  # Tiempo inicial
x0 = 1.0  # Valor inicial de X
c0 = 2.0  # Valor inicial de C
i0 = 1.0  # Valor inicial de I
y0 = np.array([x0, c0, i0]) # Vector de condiciones iniciales

b = 7.0   # Tiempo final

N = x0 + c0 + i0 # Población total (constante)

params = (alpha, beta, delta, gamma, epsilon, N) # Tupla de parámetros

# --- Ejecución y Selección del Método ---

# ¡¡¡ Descomenta SOLO UN método a la vez para ejecutarlo !!!
h_elegido = 0.2 # El paso de tiempo para el método seleccionado

# print(f"Ejecutando MÉTODO DE EULER con h = {h_elegido}")
# t, X, C, I = euler_method(model, y0, t0, b, h_elegido, params)
# nombre_metodo = "Euler"

# print(f"Ejecutando MÉTODO DE HEUN con h = {h_elegido}")
# t, X, C, I = heun_method(model, y0, t0, b, h_elegido, params)
# nombre_metodo = "Heun"

# print(f"Ejecutando MÉTODO DEL POLÍGONO MEJORADO (P. MEDIO) con h = {h_elegido}")
# t, X, C, I = improved_polygon_method(model, y0, t0, b, h_elegido, params)
# nombre_metodo = "Polígono Mejorado"

# print(f"Ejecutando MÉTODO DE RALSTON con h = {h_elegido}")
# t, X, C, I = ralston_method(model, y0, t0, b, h_elegido, params)
# nombre_metodo = "Ralston"

# print(f"Ejecutando MÉTODO RK3 con h = {h_elegido}")
# t, X, C, I = rk3_method(model, y0, t0, b, h_elegido, params)
# nombre_metodo = "RK3"

print(f"Ejecutando MÉTODO RK4 con h = {h_elegido}") # <-- Ejecutando RK4 por defecto
t, X, C, I = rk4_method(model, y0, t0, b, h_elegido, params)
nombre_metodo = "RK4"

# --- Obtener la Solución de Referencia (Pseudo-Analítica) ---
# Usamos un factor para que h_ref sea más pequeño que h_elegido
t_ref, X_ref_full, C_ref_full, I_ref_full = get_reference_solution(model, y0, t0, b, params, h_ref_factor=200)

# --- Interpolar la Solución de Referencia en los Puntos de Tiempo del Método Elegido ---
# Esto es necesario porque los puntos de tiempo t y t_ref pueden no coincidir exactamente.
# np.interp(x_nuevo, x_original, y_original) -> evalúa la función definida por (x_original, y_original) en los puntos x_nuevo
print("Interpolando la solución de referencia para la comparación...")
X_ref_interp = np.interp(t, t_ref, X_ref_full)
C_ref_interp = np.interp(t, t_ref, C_ref_full)
I_ref_interp = np.interp(t, t_ref, I_ref_full)
print("Interpolación completa.")

# --- Presentación de Resultados Comparativos ---
print(f"\nTabla Comparativa: {nombre_metodo} (h={h_elegido}) vs. Solución de Referencia (RK4 muy preciso)")
# Ajusta el ancho de la línea según sea necesario
print("-" * 100)
print(f"{'Tiempo (T)':<12} {'X (Num)':<15} {'C (Num)':<15} {'I (Num)':<15} | {'X (Ref)':<15} {'C (Ref)':<15} {'I (Ref)':<15}")
print("-" * 100)

# Iterar sobre los resultados del método elegido (t, X, C, I)
for i in range(len(t)):
    # Imprimir los valores del método numérico y los valores interpolados de la referencia
    print(f"{t[i]:<12.4f} {X[i]:<15.6f} {C[i]:<15.6f} {I[i]:<15.6f} | {X_ref_interp[i]:<15.6f} {C_ref_interp[i]:<15.6f} {I_ref_interp[i]:<15.6f}")

print("-" * 100)


# --- NOTA ADICIONAL ---
# Este código ejecuta UN método numérico (el que descomentes) con UN valor de h a la vez
# y lo compara con una solución de referencia de alta precisión calculada con RK4.
# Para calcular errores relativos, puedes usar los valores de la tabla:
#   Error Relativo X = |(X (Num) - X (Ref)) / X (Ref)| * 100% (si X (Ref) no es cero)
#   Y similarmente para C e I.
# Recuerda que la "Solución de Referencia" aquí NO es una solución analítica exacta,
# sino una aproximación numérica muy buena.