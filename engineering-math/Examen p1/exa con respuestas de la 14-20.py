import math
import matplotlib.pyplot as plt

def secante(f, a, b, E, imax, vis):
    fa = f(a)
    fb = f(b)
    
    # Verificar si los signos de fa y fb son iguales
    if fa * fb >= 0:
        print("La función no cumple con el requisito de signos opuestos en los extremos del intervalo.")
        return None, None, None  # Devuelve None para indicar que no se encontró una raíz
    
    for cont in range(imax):
        xr = b - fb * (b - a) / (fb - fa)
        fr = f(xr)
        if vis == 1:
            print(cont, xr, fr)
        
        # Usar una tolerancia relativa para la condición de parada
        if abs(fr) < E or abs((xr-b)/xr if xr !=0 else (xr-b)) < E :
            return xr, cont, xr  # Devolver la raíz, iteraciones y la ultima aproximación

        if fa * fr < 0:
            b = xr
            fb = fr
        else:
            a = xr
            fa = fr
    return None, cont, None # Devolver la raíz, iteraciones y la ultima aproximación

k_vals = [0.2 + 0.2 * i for i in range(25)]
beta_vals = [0.4 + 0.4 * i for i in range(10)]
m_vals = [0.1 + 0.2 * i for i in range(33)]

resultados = []

for k in k_vals:
    for beta in beta_vals:
        for m in m_vals:
            f = lambda r: m * r**2 + beta * r + k
            
            # Inicializar a y b con valores que aseguren signos opuestos
            a = -10  
            b = 10  
            
            raiz, iteraciones, ultima_aproximacion = secante(f, a, b, 1e-5, 100, 0)
            
            if raiz is None:
                continue
            
            discriminante = beta**2 - 4 * m * k
            tipo_raiz = "real_diferente" if discriminante > 0 else \
                        "real_igual" if discriminante == 0 else "compleja"
            resultados.append([k, beta, m, raiz, tipo_raiz, iteraciones, ultima_aproximacion])


