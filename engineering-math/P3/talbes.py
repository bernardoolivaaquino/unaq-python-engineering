import numpy as np
import matplotlib.pyplot as plt

def f(t, x, v):
    return -5 * v - 4 * x

def euler(h, t_max):
    t_values = np.arange(0, t_max + h, h)
    x_values = np.zeros_like(t_values)
    v_values = np.zeros_like(t_values)
    x_values[0], v_values[0] = 1, 1
    
    for i in range(len(t_values) - 1):
        v_values[i+1] = v_values[i] + h * f(t_values[i], x_values[i], v_values[i])
        x_values[i+1] = x_values[i] + h * v_values[i]
    
    return t_values, x_values

def heun(h, t_max):
    t_values = np.arange(0, t_max + h, h)
    x_values = np.zeros_like(t_values)
    v_values = np.zeros_like(t_values)
    x_values[0], v_values[0] = 1, 1
    
    for i in range(len(t_values) - 1):
        v_pred = v_values[i] + h * f(t_values[i], x_values[i], v_values[i])
        x_pred = x_values[i] + h * v_values[i]
        v_values[i+1] = v_values[i] + (h/2) * (f(t_values[i], x_values[i], v_values[i]) + f(t_values[i+1], x_pred, v_pred))
        x_values[i+1] = x_values[i] + (h/2) * (v_values[i] + v_pred)
    
    return t_values, x_values

def polygono_mejorado(h, t_max):
    return heun(h, t_max)

def ralston(h, t_max):
    t_values = np.arange(0, t_max + h, h)
    x_values = np.zeros_like(t_values)
    v_values = np.zeros_like(t_values)
    x_values[0], v_values[0] = 1, 1
    
    for i in range(len(t_values) - 1):
        k1_v = f(t_values[i], x_values[i], v_values[i])
        k1_x = v_values[i]
        k2_v = f(t_values[i] + (2/3) * h, x_values[i] + (2/3) * h * k1_x, v_values[i] + (2/3) * h * k1_v)
        k2_x = v_values[i] + (2/3) * h * k1_v
        v_values[i+1] = v_values[i] + (h / 4) * (k1_v + 3 * k2_v)
        x_values[i+1] = x_values[i] + (h / 4) * (k1_x + 3 * k2_x)
    
    return t_values, x_values

def rk3(h, t_max):
    t_values = np.arange(0, t_max + h, h)
    x_values = np.zeros_like(t_values)
    v_values = np.zeros_like(t_values)
    x_values[0], v_values[0] = 1, 1
    
    for i in range(len(t_values) - 1):
        k1_v = f(t_values[i], x_values[i], v_values[i])
        k1_x = v_values[i]
        k2_v = f(t_values[i] + h/2, x_values[i] + (h/2) * k1_x, v_values[i] + (h/2) * k1_v)
        k2_x = v_values[i] + (h/2) * k1_v
        k3_v = f(t_values[i] + h, x_values[i] - h * k1_x + 2 * h * k2_x, v_values[i] - h * k1_v + 2 * h * k2_v)
        k3_x = v_values[i] - h * k1_v + 2 * h * k2_v
        v_values[i+1] = v_values[i] + (h / 6) * (k1_v + 4 * k2_v + k3_v)
        x_values[i+1] = x_values[i] + (h / 6) * (k1_x + 4 * k2_x + k3_x)
    
    return t_values, x_values

def solucion_analitica(t):
    return (5/3)*np.exp(-t) - (2/3)*np.exp(-4*t)

h = 0.34
t_max = 4

metodos = {
    "Euler": euler(h, t_max),
    "Heun": heun(h, t_max),
    "Polígono Mejorado": polygono_mejorado(h, t_max),
    "Ralston": ralston(h, t_max),
    "RK3": rk3(h, t_max)
}

for nombre, (t, x) in metodos.items():
    print(f"\n{nombre}:")
    for i in range(len(t)):
        print(f"t = {t[i]:.2f}, x = {x[i]:.6f}")

# Imprimir solución analítica
t_analytic = np.linspace(0, t_max, int(t_max/h) + 1)
x_analytic = solucion_analitica(t_analytic)
print("\nSolución Analítica:")
for i in range(len(t_analytic)):
    print(f"t = {t_analytic[i]:.2f}, x = {x_analytic[i]:.6f}")

# Graficar resultados
t_analytic_plot = np.linspace(0, t_max, 1000)
x_analytic_plot = solucion_analitica(t_analytic_plot)

plt.figure(figsize=(10, 6))
plt.plot(t_analytic_plot, x_analytic_plot, label='Analítica', linewidth=2, color='black')
for nombre, (t, x) in metodos.items():
    plt.scatter(t, x, label=nombre)
plt.xlabel('Tiempo t')
plt.ylabel('x(t)')
plt.title('Comparación de Métodos Numéricos con la Solución Analítica')
plt.legend()
plt.grid()
plt.show()
