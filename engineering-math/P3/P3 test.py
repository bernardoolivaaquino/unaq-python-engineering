import matplotlib
import math
import numpy as np

# dX/dt = beta*C - alpha*(X*C / (N - I)) + epsilon*I
# dC/dt = -beta*C + alpha*(X*C / (N - I)) - gamma*C + delta*I
# dI/dt = gamma*C - I*(delta + epsilon)
# N = X + C + I (Constante)

def model(t, y, alpha, beta, delta, gamma, epsilon, N):

    X, C, I = y

    denominator = N - I
    if np.abs(denominator) < 1e-9: 
        print(f"Advertencia: Denominador (N-I) cercano a cero en t={t:.2f}. Usando 1e-9.")
        denominator = 1e-9 



    dxdt = beta * C - alpha * (X * C / denominator) + epsilon * I
    dcdt = -beta * C + alpha * (X * C / denominator) - gamma * C + delta * I
    didt = gamma * C - I * (delta + epsilon)

    return np.array([dxdt, dcdt, didt])

def euler_method(f, y0, t0, b, h, params):
    num_steps = int(np.ceil((b - t0) / h)) 
    t_values = np.linspace(t0, t0 + num_steps * h, num_steps + 1)
    if abs(t_values[-1] - b) > 1e-6 and t_values[-1] > b :
         t_values = t_values[:-1]
    elif abs(t_values[-1] - b) > 1e-6 and t_values[-1] < b :
        t_values = np.append(t_values, b)

    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i] 
        dydt = f(t_current, y_current, *params)
        y_values[i+1] = y_current + current_h * dydt
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

def heun_method(f, y0, t0, b, h, params):
    num_steps = int(np.ceil((b - t0) / h))
    t_values = np.linspace(t0, t0 + num_steps * h, num_steps + 1)
    if abs(t_values[-1] - b) > 1e-6 and t_values[-1] > b :
         t_values = t_values[:-1]
    elif abs(t_values[-1] - b) > 1e-6 and t_values[-1] < b :
        t_values = np.append(t_values, b)

    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        k1 = current_h * f(t_current, y_current, *params)
        y_predictor = y_current + k1
        k2 = current_h * f(t_values[i+1], y_predictor, *params)
        y_values[i+1] = y_current + 0.5 * (k1 + k2)
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

def improved_polygon_method(f, y0, t0, b, h, params):
    
    num_steps = int(np.ceil((b - t0) / h))
    t_values = np.linspace(t0, t0 + num_steps * h, num_steps + 1)
    if abs(t_values[-1] - b) > 1e-6 and t_values[-1] > b :
         t_values = t_values[:-1]
    elif abs(t_values[-1] - b) > 1e-6 and t_values[-1] < b :
        t_values = np.append(t_values, b)

    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        k1 = current_h * f(t_current, y_current, *params)
        y_mid = y_current + 0.5 * k1
        k2 = current_h * f(t_current + 0.5 * current_h, y_mid, *params)
        y_values[i+1] = y_current + k2
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]


def ralston_method(f, y0, t0, b, h, params):
    num_steps = int(np.ceil((b - t0) / h))
    t_values = np.linspace(t0, t0 + num_steps * h, num_steps + 1)
    if abs(t_values[-1] - b) > 1e-6 and t_values[-1] > b :
         t_values = t_values[:-1]
    elif abs(t_values[-1] - b) > 1e-6 and t_values[-1] < b :
        t_values = np.append(t_values, b)

    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        k1 = current_h * f(t_current, y_current, *params)
        y_3_4 = y_current + (3/4) * k1
        k2 = current_h * f(t_current + (3/4) * current_h, y_3_4, *params)
        y_values[i+1] = y_current + (1/3) * k1 + (2/3) * k2
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]


def rk3_method(f, y0, t0, b, h, params):
    num_steps = int(np.ceil((b - t0) / h))
    t_values = np.linspace(t0, t0 + num_steps * h, num_steps + 1)
    if abs(t_values[-1] - b) > 1e-6 and t_values[-1] > b :
         t_values = t_values[:-1]
    elif abs(t_values[-1] - b) > 1e-6 and t_values[-1] < b :
        t_values = np.append(t_values, b)

    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        current_h = t_values[i+1] - t_values[i]
        k1 = current_h * f(t_current, y_current, *params)
        k2 = current_h * f(t_current + 0.5 * current_h, y_current + 0.5 * k1, *params)
        k3 = current_h * f(t_values[i+1], y_current - k1 + 2 * k2, *params) 
        y_values[i+1] = y_current + (1/6) * (k1 + 4 * k2 + k3)
    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]


def rk4_method(f, y0, t0, b, h, params):
    num_steps = int(np.ceil((b - t0) / h)) 
    t_values = np.linspace(t0, t0 + num_steps * h, num_steps + 1)
    
    if abs(t_values[-1] - b) > 1e-6 and t_values[-1] > b :
         t_values = t_values[:-1] 
    elif abs(t_values[-1] - b) > 1e-6 and t_values[-1] < b :
         t_values = np.append(t_values, b)


    y_values = np.zeros((len(t_values), len(y0)))
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        t_current = t_values[i]
        y_current = y_values[i]
        
        current_h = t_values[i+1] - t_values[i]

        k1 = current_h * f(t_current, y_current, *params)
        k2 = current_h * f(t_current + 0.5 * current_h, y_current + 0.5 * k1, *params)
        k3 = current_h * f(t_current + 0.5 * current_h, y_current + 0.5 * k2, *params)
        k4 = current_h * f(t_values[i+1], y_current + k3, *params)
        y_values[i+1] = y_current + (1/6) * (k1 + 2*k2 + 2*k3 + k4)

    return t_values, y_values[:, 0], y_values[:, 1], y_values[:, 2]

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




h_elegido = 1.5

print(f"Ejecutando con h = {h_elegido}")

#print("\n--- Método de Euler ---")
#t, X, C, I = euler_method(model, y0, t0, b, h_elegido, params)
#nombre_metodo = "Euler"

#print("\n--- Método de Heun ---")
#t, X, C, I = heun_method(model, y0, t0, b, h_elegido, params)
#nombre_metodo = "Heun"

#print("\n--- Método del Polígono Mejorado (Punto Medio) ---")
#t, X, C, I = improved_polygon_method(model, y0, t0, b, h_elegido, params)
#nombre_metodo = "Polígono Mejorado"

#print("\n--- Método de Ralston ---")
#t, X, C, I = ralston_method(model, y0, t0, b, h_elegido, params)
#nombre_metodo = "Ralston"

#print("\n--- Método RK3 ---") #<-- Ejecutando RK3 por defecto
#t, X, C, I = rk3_method(model, y0, t0, b, h_elegido, params)
#nombre_metodo = "RK3"


print("\n--- Método RK4 ---")
t, X, C, I = rk4_method(model, y0, t0, b, h_elegido, params)
nombre_metodo = "RK4"


print(f"\nTabla de Valores para X, C, I, T usando el método {nombre_metodo} con h = {h_elegido}")
print("-" * 60) 

print(f"{'Tiempo (T)':<12} {'X':<15} {'C':<15} {'I':<15}")
print("-" * 60)


for i in range(len(t)):
    print(f"{t[i]:<12.4f} {X[i]:<15.6f} {C[i]:<15.6f} {I[i]:<15.6f}")

print("-" * 60)


# --- NOTA ADICIONAL ---
# Este código ejecuta UN método con UN valor de h a la vez.
# Para responder todas las preguntas del documento, necesitarás:
# 1. Ejecutar este código varias veces, cambiando 'h_elegido' y el método descomentado.
# 2. Almacenar o anotar los resultados específicos que piden las preguntas (e.g., X en t=5 con RK4 y h=0.5).
# 3. Para las preguntas de error relativo (7, 8, 9), necesitarás ejecutar dos métodos con el mismo h
#    (por ejemplo, RK4 y Euler con h=0.5) y luego calcular el error:
#    Error Relativo = |(Valor_Aproximado - Valor_Real) / Valor_Real| * 100%
#    Donde el "Valor_Real" se toma del método más preciso (RK4 en este caso).
# 4. Para las preguntas 10-14 (modificar coeficientes), requerirás un enfoque de prueba y error
#    o un método de optimización, ajustando alpha, beta, etc., y volviendo a ejecutar la simulación
#    hasta alcanzar el objetivo deseado.
# 5. Para las gráficas (15-18), puedes usar librerías como Matplotlib para visualizar los datos
#    generados (los arrays t, X, C, I).