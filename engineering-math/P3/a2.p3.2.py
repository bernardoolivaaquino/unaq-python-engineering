import numpy as np
import matplotlib.pyplot as plt
import math # Importar math para usar ceil

# --- 1. Definir el sistema de EDOs de primer orden ---
# (Sin cambios)
def F(t, Y):
    y1, y2 = Y
    dy1_dt = y2
    dy2_dt = -4.0 * y1 - 5.0 * y2
    return np.array([dy1_dt, dy2_dt])

# --- 2. Implementación de los pasos de los métodos numéricos ---
# (Sin cambios: euler_step, heun_step, ralston_step, rk3_step)
def euler_step(f, t, y, h):
    return y + h * f(t, y)

def heun_step(f, t, y, h):
    k1 = f(t, y)
    y_predict = y + h * k1
    k2 = f(t + h, y_predict)
    return y + (h / 2.0) * (k1 + k2)

def ralston_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + (2.0/3.0)*h, y + (2.0/3.0)*h*k1)
    return y + h * (0.25*k1 + 0.75*k2)

def rk3_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + 0.5*h, y + 0.5*h*k1)
    k3 = f(t + h, y - h*k1 + 2.0*h*k2)
    return y + (h / 6.0) * (k1 + 4.0*k2 + k3)


# --- 3. Solucionador genérico - MODIFICADO PARA USAR h EXACTO ---
def solve_ode(method_step_func, f, y0, t_span, h):
    """
    Resuelve un sistema de EDOs usando un método de un solo paso
    con un tamaño de paso h *exacto*.
    Los puntos de tiempo se generan sumando h hasta alcanzar o superar t_end.
    """
    t_start, t_end = t_span
    
    # Estimar número de pasos necesarios (para pre-alocar arrays si se quisiera)
    # Se suma una pequeña cantidad a t_end para asegurar que se incluya si es múltiplo de h
    n_steps = math.ceil((t_end - t_start + h * 1e-9) / h) 
    
    # Generar puntos de tiempo usando el h exacto
    # Similar a np.arange(t_start, t_end + h, h) pero asegurando incluir t_start
    t_values = np.array([t_start + i * h for i in range(n_steps + 1)])
    # Recortar si el último punto excede t_end innecesariamente lejos (opcional)
    # t_values = t_values[t_values <= t_end + h*1e-9] 
    
    # Recalcular n_steps basado en los t_values generados
    n_steps = len(t_values) - 1 

    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0, :] = y0

    for i in range(n_steps):
        # Usa el h especificado directamente
        y_values[i+1, :] = method_step_func(f, t_values[i], y_values[i, :], h)

    return t_values, y_values

# --- 4. Solución Analítica (para comparación) ---
# (Sin cambios)
def analytical_solution(t):
    return (5.0/3.0) * np.exp(-t) - (2.0/3.0) * np.exp(-4.0*t)

# --- 5. Parámetros del Problema y Ejecución ---
y0 = np.array([1.0, 1.0]) # Condiciones iniciales: Y(0) = [x(0), x'(0)] = [1, 1]
t_span = [0.0, 4.0]      # Intervalo de tiempo [t_start, t_end]
t_max = t_span[1]

# ==========================================================
# === ¡MODIFICA AQUÍ EL TAMAÑO DE PASO (h) DESEADO! ===
h = 0.35 # Ahora este valor de h será usado directamente
# ==========================================================

print(f"Resolviendo con tamaño de paso h = {h} (exacto)")

# Diccionario para almacenar resultados (t_values, x_values)
results = {}

# Calcular soluciones numéricas y almacenar x(t)
t_euler, y_euler = solve_ode(euler_step, F, y0, t_span, h)
results['Euler'] = (t_euler, y_euler[:, 0])

t_heun, y_heun = solve_ode(heun_step, F, y0, t_span, h)
results['Heun / Polígono Mejorado'] = (t_heun, y_heun[:, 0])

t_ralston, y_ralston = solve_ode(ralston_step, F, y0, t_span, h)
results['Ralston'] = (t_ralston, y_ralston[:, 0])

t_rk3, y_rk3 = solve_ode(rk3_step, F, y0, t_span, h)
results['RK3'] = (t_rk3, y_rk3[:, 0])

# Usar los tiempos de una de las soluciones como referencia
t_ref = results['Euler'][0]

# Calcular solución analítica en los mismos puntos de tiempo
x_analytical_at_steps = analytical_solution(t_ref)

# --- 6. Imprimir los Valores Calculados ---
print("\n--- Valores Calculados por Método ---")
for nombre, (t, x) in results.items():
    print(f"\n === {nombre} (h={h}) ===") # Usar el h especificado
    print("-----------------------------")
    print("  t      |    x(t)")
    print("---------|-------------")
    for i in range(len(t)):
        # Formato: t con 3 decimales, x con 6 decimales
        print(f" {t[i]:<7.3f} | {x[i]:>11.6f}")
    print("-----------------------------")

print("\n === Solución Analítica (en los mismos t numéricos) ===")
print("-----------------------------")
print("  t      |    x(t)")
print("---------|-------------")
for i in range(len(t_ref)):
     # Formato: t con 3 decimales, x con 6 decimales
     print(f" {t_ref[i]:<7.3f} | {x_analytical_at_steps[i]:>11.6f}")
print("-----------------------------")


# --- 7. Graficar los resultados ---
plt.figure(figsize=(12, 8))

# Solución analítica más suave para la línea
t_analytical_smooth = np.linspace(t_span[0], t_span[1], 200)
x_analytical_smooth = analytical_solution(t_analytical_smooth)
plt.plot(t_analytical_smooth, x_analytical_smooth, 'k-', linewidth=2, label='Solución Analítica')

# Graficar resultados numéricos
for nombre, (t, x) in results.items():
     plt.plot(t, x, 'o--', markersize=5, alpha=0.8, label=f'{nombre}')

plt.title(f'Comparación de Métodos Numéricos vs. Solución Analítica (h={h})') # Usar h exacto
plt.xlabel('Tiempo t')
plt.ylabel('Posición x(t)')
plt.legend()
plt.grid(True)
plt.ylim(bottom=-0.1)
plt.axhline(0, color='grey', linewidth=0.5)
# Asegurar que el eje x muestre hasta el último punto calculado si excede t_end
plt.xlim(left=t_span[0], right=max(t_span[1], t_ref[-1])) 

plt.show()

