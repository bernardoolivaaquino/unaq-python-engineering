import numpy as np
import matplotlib.pyplot as plt

# --- 1. Definir el sistema de EDOs de primer orden ---
# dY/dt = F(t, Y) donde Y = [y1, y2] = [x, x']
# La ecuación original es: d²x/dt² + 5 dx/dt + 4x = 0
# dy1/dt = y2
# dy2/dt = -4*y1 - 5*y2
def F(t, Y):
    """
    Define el sistema de ecuaciones diferenciales de primer orden.
    Args:
        t (float): Tiempo actual (aunque no se usa explícitamente aquí porque la EDO es autónoma).
        Y (np.array): Vector de estado [y1, y2] = [x, dx/dt].
    Returns:
        np.array: Vector de derivadas [dy1/dt, dy2/dt].
    """
    y1, y2 = Y
    dy1_dt = y2
    dy2_dt = -4.0 * y1 - 5.0 * y2
    return np.array([dy1_dt, dy2_dt])

# --- 2. Implementación de los pasos de los métodos numéricos ---

def euler_step(f, t, y, h):
    """Realiza un paso del método de Euler."""
    return y + h * f(t, y)

def heun_step(f, t, y, h):
    """Realiza un paso del método de Heun (RK2 - Trapecio)."""
    k1 = f(t, y)
    y_predict = y + h * k1
    k2 = f(t + h, y_predict)
    return y + (h / 2.0) * (k1 + k2)

def ralston_step(f, t, y, h):
    """Realiza un paso del método de Ralston (RK2)."""
    k1 = f(t, y)
    k2 = f(t + (2.0/3.0)*h, y + (2.0/3.0)*h*k1)
    return y + h * (0.25*k1 + 0.75*k2)

def rk3_step(f, t, y, h):
    """Realiza un paso del método RK3 (Kutta clásico)."""
    k1 = f(t, y)
    k2 = f(t + 0.5*h, y + 0.5*h*k1)
    k3 = f(t + h, y - h*k1 + 2.0*h*k2)
    return y + (h / 6.0) * (k1 + 4.0*k2 + k3)

# --- 3. Solucionador genérico de EDO ---
def solve_ode(method_step_func, f, y0, t_span, h):
    """
    Resuelve un sistema de EDOs usando un método de un solo paso.
    Args:
        method_step_func: La función que implementa el paso del método (ej. euler_step).
        f: La función que define el sistema de EDOs F(t, Y).
        y0 (np.array): Vector de condiciones iniciales.
        t_span (list or tuple): Intervalo de tiempo [t_start, t_end].
        h (float): Tamaño del paso.
    Returns:
        tuple: (t_values, y_values) donde t_values es un array de tiempos
               y y_values es un array 2D con las soluciones [y1(t), y2(t)] en cada fila.
    """
    t_start, t_end = t_span
    # Calcula el número de pasos (asegura incluir t_end)
    n_steps = int(np.ceil((t_end - t_start) / h))
    # Ajusta h para que el último punto coincida exactamente con t_end si es necesario
    # h = (t_end - t_start) / n_steps # Descomentar si se prefiere ajustar h

    t_values = np.linspace(t_start, t_start + n_steps * h, n_steps + 1)
    # Asegura que t_values no exceda t_end (por errores de punto flotante)
    t_values = t_values[t_values <= t_end]
    if t_values[-1] < t_end and not np.isclose(t_values[-1], t_end):
         t_values = np.append(t_values, t_end) # Añade t_end si falta
         n_steps = len(t_values) - 1
         # Reajusta h si t_end fue añadido (o maneja el último paso de forma especial)
         # Para simplicidad, no reajustaremos h aquí, el último paso puede ser más corto

    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0, :] = y0
    y_current = y0.copy()
    t_current = t_start

    for i in range(n_steps):
        current_h = t_values[i+1] - t_values[i] # Usa la diferencia real de tiempo
        y_current = method_step_func(f, t_current, y_current, current_h)
        y_values[i+1, :] = y_current
        t_current = t_values[i+1] # Actualiza al siguiente tiempo exacto

    return t_values, y_values

# --- 4. Solución Analítica (para comparación) ---
# Ecuación característica: r^2 + 5r + 4 = 0 => (r+1)(r+4)=0 => r1=-1, r2=-4
# Solución general: x(t) = c1*exp(-t) + c2*exp(-4t)
# x'(t) = -c1*exp(-t) - 4*c2*exp(-4t)
# x(0)=1 => c1 + c2 = 1
# x'(0)=1 => -c1 - 4*c2 = 1
# Resolviendo: c2 = -2/3, c1 = 5/3
# Solución analítica: x(t) = (5/3)*exp(-t) - (2/3)*exp(-4t)
def analytical_solution(t):
    """Calcula la solución analítica x(t)."""
    return (5.0/3.0) * np.exp(-t) - (2.0/3.0) * np.exp(-4.0*t)

# --- 5. Parámetros del Problema y Ejecución ---
y0 = np.array([1.0, 1.0]) # Condiciones iniciales: Y(0) = [x(0), x'(0)] = [1, 1]
t_span = [0.0, 4.0]      # Intervalo de tiempo [t_start, t_end]

# ==========================================================
# === ¡MODIFICA AQUÍ EL TAMAÑO DE PASO (h) DESEADO! ===
h = 0.35  # Ejemplo: tamaño de paso
# ==========================================================

print(f"Resolviendo con tamaño de paso h = {h}")

# Calcular soluciones numéricas
t_euler, y_euler = solve_ode(euler_step, F, y0, t_span, h)
t_heun, y_heun = solve_ode(heun_step, F, y0, t_span, h)
t_ralston, y_ralston = solve_ode(ralston_step, F, y0, t_span, h)
t_rk3, y_rk3 = solve_ode(rk3_step, F, y0, t_span, h)

# Extraer la componente x(t) (que es y1) de las soluciones
x_euler = y_euler[:, 0]
x_heun = y_heun[:, 0]
x_ralston = y_ralston[:, 0]
x_rk3 = y_rk3[:, 0]

# Calcular solución analítica para graficar en más puntos (para una curva suave)
t_analytical_smooth = np.linspace(t_span[0], t_span[1], 200)
x_analytical_smooth = analytical_solution(t_analytical_smooth)

# Calcular la solución analítica en los mismos puntos que los métodos numéricos (para errores)
# Usaremos los puntos de RK3 como referencia, ya que todos deberían ser iguales si h no se ajusta
t_ref = t_rk3
x_analytical_at_steps = analytical_solution(t_ref)

# --- 6. Graficar los resultados ---
plt.figure(figsize=(12, 8))

plt.plot(t_analytical_smooth, x_analytical_smooth, 'k-', linewidth=2, label='Solución Analítica')
plt.plot(t_euler, x_euler, 'o--', markersize=5, label=f'Euler (h={h})')
plt.plot(t_heun, x_heun, 's--', markersize=5, label=f'Heun (RK2) (h={h})')
plt.plot(t_ralston, x_ralston, '^--', markersize=5, label=f'Ralston (RK2) (h={h})')
plt.plot(t_rk3, x_rk3, 'd--', markersize=5, label=f'RK3 (h={h})')

plt.title('Comparación de Métodos Numéricos vs. Solución Analítica\nd²x/dt² + 5dx/dt + 4x = 0, x(0)=1, x\'(0)=1')
plt.xlabel('Tiempo t')
plt.ylabel('Posición x(t)')
plt.legend()
plt.grid(True)
plt.ylim(bottom=0) # Ajustar si es necesario para ver mejor cerca de cero
plt.axhline(0, color='grey', linewidth=0.5) # Eje x=0

plt.show()

