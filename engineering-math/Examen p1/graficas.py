import math
import matplotlib.pyplot as plt

def secante(f, a, b, E, imax, vis):
    """
    Calcula la raíz de una función utilizando el método de la secante.

    Args:
        f: La función a la que se le busca la raíz.
        a: El primer punto inicial.
        b: El segundo punto inicial.
        E: La tolerancia de error.
        imax: El número máximo de iteraciones.
        vis: Un parámetro para visualizar las iteraciones (1 para mostrar, 0 para ocultar).

    Returns:
        La raíz aproximada de la función, o None si no se encuentra dentro de las iteraciones máximas.
    """
    fa = f(a)
    fb = f(b)
    
    # if abs(fa) < E: return a  # Esto usaba abs, lo cambiamos
    if fa**2 < E**2: return a
    # if abs(fb) < E: return b # Esto usaba abs, lo cambiamos
    if fb**2 < E**2: return b

    cont = 0
    for _ in range(imax):
        cont += 1
        xr = a - fa * (a - b) / (fa - fb)
        fr = f(xr)
        if vis == 1: print(cont, xr, fr)
        # if abs(fr) < E: return xr # Esto usaba abs, lo cambiamos
        if fr**2 < E**2: return xr
        if fa * fr < 0:
            b = xr
            fb = fr
        else:
            a = xr
            fa = fr
    return None

k_vals = [0.2 + 0.2 * i for i in range(25)]
beta_vals = [0.4 + 0.4 * i for i in range(10)]
m_vals = [0.1 + 0.2 * i for i in range(33)]

resultados = []

for k in k_vals:
    for beta in beta_vals:
        for m in m_vals:
            f = lambda r: m*r**2 + beta*r + k
            raiz = secante(f, -4, 4.2, 1e-5, 100, 0) # Se modifico el intervalo inicial de [-4, 4.2] para incluir raices negativas
            if raiz is None: continue

            discriminante = beta**2 - 4*m*k
            tipo_raiz = "real_diferente" if discriminante > 0 else \
                        "real_igual" if discriminante == 0 else "compleja"
            resultados.append([k, beta, m, raiz, tipo_raiz])

# --- Código para graficar ---

# 14. Raíces reales vs k
plt.figure(figsize=(8, 6))
for k, _, _, raiz, tipo_raiz in resultados:
    if tipo_raiz == "real_diferente":
        plt.scatter(k, raiz)
plt.xlabel("k (Constante del resorte)")
plt.ylabel("Raíces reales diferentes")
plt.title("Raíces reales vs k")
plt.grid(True)
plt.show()

# 15. Raíces reales vs m
plt.figure(figsize=(8, 6))
for _, _, m, raiz, tipo_raiz in resultados:
    if tipo_raiz == "real_diferente":
        plt.scatter(m, raiz)
plt.xlabel("m (Masa)")
plt.ylabel("Raíces reales diferentes")
plt.title("Raíces reales vs m")
plt.grid(True)
plt.show()

# 16. Raíces reales vs beta
plt.figure(figsize=(8, 6))
for _, beta, _, raiz, tipo_raiz in resultados:
    if tipo_raiz == "real_diferente":
        plt.scatter(beta, raiz)
plt.xlabel("β (Amortiguamiento)")
plt.ylabel("Raíces reales diferentes")
plt.title("Raíces reales vs β")
plt.grid(True)
plt.show()

# 17. Raíces reales iguales vs k
plt.figure(figsize=(8, 6))
for k, _, _, raiz, tipo_raiz in resultados:
    if tipo_raiz == "real_igual":
        plt.scatter(k, raiz)
plt.xlabel("k (Constante del resorte)")
plt.ylabel("Raíces reales iguales")
plt.title("Raíces reales iguales vs k")
plt.grid(True)
plt.show()

# 18. Raíces reales iguales vs m
plt.figure(figsize=(8, 6))
for _, _, m, raiz, tipo_raiz in resultados:
    if tipo_raiz == "real_igual":
        plt.scatter(m, raiz)
plt.xlabel("m (Masa)")
plt.ylabel("Raíces reales iguales")
plt.title("Raíces reales iguales vs m")
plt.grid(True)
plt.show()

# 19. Raíces reales iguales vs beta
plt.figure(figsize=(8, 6))
for _, beta, _, raiz, tipo_raiz in resultados:
    if tipo_raiz == "real_igual":
        plt.scatter(beta, raiz)
plt.xlabel("β (Amortiguamiento)")
plt.ylabel("Raíces reales iguales")
plt.title("Raíces reales iguales vs β")
plt.grid(True)
plt.show()

# 20. Raíces reales vs complejas en función de la masa
plt.figure(figsize=(8, 6))
for _, _, m, raiz, tipo_raiz in resultados:
    if tipo_raiz == "real_diferente":
        plt.scatter(m, raiz, label="Real diferente", color = "blue")
    elif tipo_raiz == "compleja":
        plt.scatter(m, raiz, label="Compleja", color = "orange")
plt.xlabel("m (Masa)")
plt.ylabel("Raíces")
plt.title("Raíces reales vs complejas en función de la masa")
plt.legend()
plt.grid(True)
plt.show()
