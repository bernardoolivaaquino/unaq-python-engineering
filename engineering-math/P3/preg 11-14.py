import matplotlib # Dejado por si se usa en el futuro
import math
import numpy as np
import time
from scipy.optimize import minimize # <--- Importante para la optimización
from scipy.interpolate import interp1d # Para obtener valor en t_target exacto

# --- Definición del Modelo de Ecuaciones Diferenciales ---
# (Sin cambios respecto a tu versión anterior)
def model(t, y, alpha, beta, delta, gamma, epsilon, N):
    X, C, I = y
    denominator = N - I
    if np.abs(denominator) < 1e-10: # Usar un umbral más pequeño es a veces mejor
        denominator = np.sign(denominator) * 1e-10 if denominator != 0 else 1e-10

    interaction_term = alpha * (X * C / denominator) if denominator != 0 else 0
    dxdt = beta * C - interaction_term + epsilon * I
    dcdt = -beta * C + interaction_term - gamma * C + delta * I
    didt = gamma * C - I * (delta + epsilon)
    return np.array([dxdt, dcdt, didt])

# --- Implementación de Métodos Numéricos ---
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

# (Se omite Euler, Heun, etc. para brevedad, pero se deja RK4 que es el que usaremos)
def rk4_method(f, y0, t0, b, h, params):
    """Método de Runge-Kutta de Orden 4 (clásico)."""
    t_values = _prepare_time_steps(t0, b, h)
    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]

        # Extraer parámetros para pasarlos a 'f'
        current_params = params # alpha, beta, delta, gamma, epsilon, N

        k1 = f(t_current, y_current, *current_params)
        k2 = f(t_current + 0.5 * current_h, y_current + 0.5 * current_h * k1, *current_params)
        k3 = f(t_current + 0.5 * current_h, y_current + 0.5 * current_h * k2, *current_params)
        k4 = f(t_values[i+1], y_current + current_h * k3, *current_params)
        y_values[i+1] = y_current + (current_h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

# --- Función Objetivo para la Optimización ---
def objective_function(current_params_array, target_var, t_target, value_target, y0, t0, b, h_sim, N_const, min_param_value):
    """
    Calcula el error cuadrático entre el valor simulado y el objetivo
    para un conjunto de parámetros dados.
    """
    alpha, beta, delta, gamma, epsilon = current_params_array

    # --- Restricción de Parámetros Mínimos ---
    if any(p < min_param_value for p in current_params_array):
        # Penalización alta si algún parámetro es demasiado bajo
        # Esto guía al optimizador a evitar estas regiones.
        return 1e18 # Un número muy grande

    # Reconstruir la tupla de parámetros para la simulación
    params_for_sim = (alpha, beta, delta, gamma, epsilon, N_const)

    try:
        # Ejecutar la simulación con los parámetros actuales
        t_sim, X_sim, C_sim, I_sim = rk4_method(model, y0, t0, b, h_sim, params_for_sim)

        # --- Obtener el valor simulado en t_target ---
        # Usamos interpolación para obtener el valor exacto en t_target,
        # ya que t_target podría no coincidir con un punto de t_sim.
        if target_var == 'X':
            f_interp = interp1d(t_sim, X_sim, kind='linear', fill_value="extrapolate")
        elif target_var == 'C':
            f_interp = interp1d(t_sim, C_sim, kind='linear', fill_value="extrapolate")
        else: # target_var == 'I'
            f_interp = interp1d(t_sim, I_sim, kind='linear', fill_value="extrapolate")

        simulated_value_at_target = f_interp(t_target)

        # Calcular el error cuadrático (lo que queremos minimizar)
        error = (simulated_value_at_target - value_target)**2
        # print(f"Params: {current_params_array}, Error: {error:.4e}") # Descomentar para depurar

    except Exception as e:
        # Si la simulación falla (p.ej., por valores inestables), penalizar
        print(f"  Advertencia: Simulación falló con params {np.round(current_params_array, 4)}. Error: {e}")
        error = 1e18 # Penalización alta

    return error

# --- Parámetros Iniciales y Configuración ---
alpha_init = 0.2
beta_init = 0.3
delta_init = 0.1 # Modificado de tu ejemplo para empezar > 0.05
gamma_init = 1.0 # Modificado de tu ejemplo para empezar en un rango más típico
epsilon_init = 0.35

t0 = 0.0
x0 = 1.0
c0 = 2.0
i0 = 1.0
y0 = np.array([x0, c0, i0])

b = 7.0 # Tiempo final de simulación

N = x0 + c0 + i0

# Paso de tiempo para las simulaciones DENTRO del optimizador y la final
# Un h más pequeño da más precisión pero hace la optimización más lenta
h_elegido = 0.5 # Ajustado para un mejor balance en optimización

min_param_val = 0.05 # RestricIción mínima para los parámetros

# --- Interacción con el Usuario ---
while True:
    target_variable = input("¿Qué variable quieres ajustar (X, C, o I)? ").upper()
    if target_variable in ['X', 'C', 'I']:
        break
    else:
        print("Entrada inválida. Por favor, introduce X, C, o I.")

while True:
    try:
        target_time = float(input(f"¿En qué tiempo (entre {t0} y {b}) quieres ajustar {target_variable}? "))
        if t0 <= target_time <= b:
            break
        else:
            print(f"El tiempo debe estar entre {t0} y {b}.")
    except ValueError:
        print("Entrada inválida. Introduce un número.")

while True:
    try:
        target_value = float(input(f"¿Qué valor objetivo quieres para {target_variable} en t={target_time}? "))
        break
    except ValueError:
        print("Entrada inválida. Introduce un número.")

print("\nIniciando optimización para encontrar los parámetros...")
print(f"Objetivo: {target_variable}(t={target_time}) ≈ {target_value}")
print(f"Restricción: alpha, beta, delta, gamma, epsilon >= {min_param_val}")

# --- Configuración de la Optimización ---
initial_guess = np.array([alpha_init, beta_init, delta_init, gamma_init, epsilon_init])

# Límites para los parámetros: [min_param_val, infinity] o un límite superior razonable
# Usar un límite superior (ej. 20) puede ayudar a estabilizar la optimización
bounds = [(min_param_val, 20.0)] * 5 # Límite inferior 0.05, superior 20.0 para todos

# Argumentos adicionales para pasar a objective_function
args_for_obj = (target_variable, target_time, target_value, y0, t0, b, h_elegido, N, min_param_val)

start_time_opt = time.time()

# Llama al optimizador. Métodos comunes que soportan bounds:
# 'L-BFGS-B', 'TNC', 'SLSQP'
# 'Nelder-Mead' es más simple pero no usa bounds directamente (los verificamos en la función)
result = minimize(objective_function,
                  initial_guess,
                  args=args_for_obj,
                  method='L-BFGS-B', # Método que maneja bien las restricciones de caja
                  bounds=bounds,
                  options={'disp': True, 'maxiter': 200, 'ftol': 1e-8}) # Mostrar progreso, limitar iteraciones

end_time_opt = time.time()
print(f"\nOptimización completada en {end_time_opt - start_time_opt:.2f} segundos.")

# --- Resultados de la Optimización ---
if result.success:
    optimized_params_array = result.x
    print("\nOptimización exitosa.")
    print("Parámetros encontrados:")
    print(f"  alpha   = {optimized_params_array[0]:.6f}")
    print(f"  beta    = {optimized_params_array[1]:.6f}")
    print(f"  delta   = {optimized_params_array[2]:.6f}")
    print(f"  gamma   = {optimized_params_array[3]:.6f}")
    print(f"  epsilon = {optimized_params_array[4]:.6f}")
else:
    print("\nLa optimización no convergió exitosamente.")
    print(f"Mensaje: {result.message}")
    print("Usando los últimos parámetros intentados (pueden no ser óptimos):")
    optimized_params_array = result.x # Usar los últimos parámetros de todas formas
    print(f"  alpha   = {optimized_params_array[0]:.6f}")
    print(f"  beta    = {optimized_params_array[1]:.6f}")
    print(f"  delta   = {optimized_params_array[2]:.6f}")
    print(f"  gamma   = {optimized_params_array[3]:.6f}")
    print(f"  epsilon = {optimized_params_array[4]:.6f}")

# --- Ejecutar Simulación Final con Parámetros Optimizados ---
print(f"\nEjecutando simulación final con h = {h_elegido} usando los parámetros encontrados...")
final_params_tuple = (optimized_params_array[0], optimized_params_array[1], optimized_params_array[2],
                      optimized_params_array[3], optimized_params_array[4], N)

t, X, C, I = rk4_method(model, y0, t0, b, h_elegido, final_params_tuple)
nombre_metodo = "RK4 (con params optimizados)"

# --- Verificar Valor Alcanzado ---
f_interp_final_X = interp1d(t, X, kind='linear', fill_value="extrapolate")
f_interp_final_C = interp1d(t, C, kind='linear', fill_value="extrapolate")
f_interp_final_I = interp1d(t, I, kind='linear', fill_value="extrapolate")

achieved_value = 0.0
if target_variable == 'X':
    achieved_value = f_interp_final_X(target_time)
elif target_variable == 'C':
    achieved_value = f_interp_final_C(target_time)
else: # target_var == 'I'
    achieved_value = f_interp_final_I(target_time)

print("\n--- Comparación Objetivo vs. Alcanzado ---")
print(f"Variable objetivo: {target_variable}")
print(f"Tiempo objetivo:   {target_time:.4f}")
print(f"Valor deseado:     {target_value:.6f}")
print(f"Valor alcanzado:   {achieved_value:.6f}")
print(f"Diferencia:        {abs(achieved_value - target_value):.6e}")


# --- Mostrar Tabla de Resultados Finales ---
print(f"\nTabla de Valores para X, C, I, T usando el método {nombre_metodo} con h = {h_elegido}")
print("-" * 60)
print(f"{'Tiempo (T)':<12} {'X':<15} {'C':<15} {'I':<15}")
print("-" * 60)

for i in range(len(t)):
    print(f"{t[i]:<12.4f} {X[i]:<15.6f} {C[i]:<15.6f} {I[i]:<15.6f}")

print("-" * 60)