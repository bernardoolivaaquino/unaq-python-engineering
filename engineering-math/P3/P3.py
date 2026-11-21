import numpy as np
import matplotlib.pyplot as plt

alpha = 0.2
beta = 0.3
delta = 0.1
gamma = 0.6
epsilon = 0.35


X0 = 1.0
C0 = 2.0
I0 = 1.0
N = X0 + C0 + I0  


if not np.isclose(X0 + C0 + I0, N):
    raise ValueError(f"Las condiciones iniciales (X0={X0}, C0={C0}, I0={I0}) no suman la población total N={N}. Ajústalos.")


t0 = 0.0       
t_final = 7.0  

h = 0.5        



def modelo_crimen(t, y, N_pop, alpha_p, beta_p, delta_p, gamma_p, epsilon_p):
    """
    Define el sistema de EDOs para el modelo de crimen.
    y: vector de estado [X, C, I]
    t: tiempo actual
    N_pop, alpha_p, beta_p, delta_p, gamma_p, epsilon_p: parámetros del modelo
    Retorna: array numpy [dX/dt, dC/dt, dI/dt]
    """
    X, C, I = y[0], y[1], y[2]

    
    denominador = N_pop - I
    if np.abs(denominador) < 1e-9: # Tolerancia pequeña
        termino_interaccion = 0.0 # Asumimos 0 si I es casi N
        print(f"Advertencia: Denominador (N-I) cercano a cero en t={t:.2f}. Interacción ajustada a 0.")
    else:
        termino_interaccion = alpha_p * (X * C) / denominador

  
    dXdt = beta_p * C - termino_interaccion + epsilon_p * I


    dCdt = -beta_p * C + termino_interaccion - gamma_p * C + delta_p * I


    dIdt = gamma_p * C - I * (delta_p + epsilon_p)

    return np.array([dXdt, dCdt, dIdt])


def paso_rk4(funcion_modelo, t, y, h, N_pop, alpha_p, beta_p, delta_p, gamma_p, epsilon_p):
    """
    Realiza un paso de integración usando el método RK4.
    funcion_modelo: la función que define las EDOs (modelo_crimen).
    t: tiempo actual.
    y: vector de estado actual [X, C, I].
    h: tamaño del paso.
    N_pop, ... epsilon_p: parámetros a pasar a funcion_modelo.
    Retorna: vector de estado y en el tiempo t+h.
    """

    k1 = h * funcion_modelo(t, y, N_pop, alpha_p, beta_p, delta_p, gamma_p, epsilon_p)
    k2 = h * funcion_modelo(t + 0.5*h, y + 0.5*k1, N_pop, alpha_p, beta_p, delta_p, gamma_p, epsilon_p)
    k3 = h * funcion_modelo(t + 0.5*h, y + 0.5*k2, N_pop, alpha_p, beta_p, delta_p, gamma_p, epsilon_p)
    k4 = h * funcion_modelo(t + h, y + k3, N_pop, alpha_p, beta_p, delta_p, gamma_p, epsilon_p)


    y_siguiente = y + (k1 + 2*k2 + 2*k3 + k4) / 6.0
    return y_siguiente


tiempos = [t0]
resultados = [np.array([X0, C0, I0])] 


tiempo_actual = t0
estado_actual = np.array([X0, C0, I0])
paso_actual = h 

print(f"Iniciando simulación con N={N}, X0={X0}, C0={C0}, I0={I0}, h={h}")

while tiempo_actual < t_final:
    if tiempo_actual + paso_actual > t_final:
        paso_actual = t_final - tiempo_actual

    estado_siguiente = paso_rk4(modelo_crimen, tiempo_actual, estado_actual, paso_actual,
                                N, alpha, beta, delta, gamma, epsilon)

    tiempo_actual += paso_actual
    estado_actual = estado_siguiente

    if tiempo_actual <= t_final:
      tiempos.append(tiempo_actual)
      resultados.append(estado_actual)

    paso_actual = h


resultados_np = np.array(resultados)
X_valores = resultados_np[:, 0]
C_valores = resultados_np[:, 1]
I_valores = resultados_np[:, 2]
Suma_valores = X_valores + C_valores + I_valores 
print(f"\nSimulación completada hasta t = {tiempos[-1]:.2f}")
print(f"Valores finales (millones):")
print(f"  X(t={tiempos[-1]:.2f}) = {X_valores[-1]:.4f}")
print(f"  C(t={tiempos[-1]:.2f}) = {C_valores[-1]:.4f}")
print(f"  I(t={tiempos[-1]:.2f}) = {I_valores[-1]:.4f}")
print(f"Suma final X+C+I = {Suma_valores[-1]:.4f} (Debería ser muy cercano a N={N})")


plt.figure(figsize=(12, 7))

plt.plot(tiempos, X_valores, label='X (No Criminales)', marker='o', linestyle='-')
plt.plot(tiempos, C_valores, label='C (Criminales)', marker='s', linestyle='--')
plt.plot(tiempos, I_valores, label='I (Encarcelados)', marker='^', linestyle=':')


plt.title(f'Simulación del Modelo de Crimen (RK4, h={h})')
plt.xlabel('Tiempo (años)')
plt.ylabel('Población (millones)')
plt.legend() 
plt.grid(True) 
plt.ylim(bottom=0)
plt.xlim(t0, t_final)

# Mostrar la gráfica
plt.show()



print("\n--- Tabla de Resultados ---")
print("Tiempo (t) | X          | C          | I          | Suma X+C+I")
print("-----------|------------|------------|------------|-----------")
for i in range(len(tiempos)):
    print(f"{tiempos[i]:<11.4f}| {X_valores[i]:<11.4f}| {C_valores[i]:<11.4f}| {I_valores[i]:<11.4f}| {Suma_valores[i]:<11.4f}")