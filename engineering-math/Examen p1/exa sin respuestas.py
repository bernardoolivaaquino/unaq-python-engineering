import math

def secante(f, a, b, E, imax, vis):
    fa = f(a)
    fb = f(b)
    if abs(fa) < E: return a
    if abs(fb) < E: return b
    for _ in range(imax):
        xr = a - fa * (a - b) / (fa - fb)
        fr = f(xr)
        if vis == 1: print(cont, xr, fr)
        if abs(fr) < E: return xr
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
            raiz = secante(f, 4, 4.2, 1e-5, 100, 0)
            if raiz is None: continue

            discriminante = beta**2 - 4*m*k
            tipo_raiz = "real_diferente" if discriminante > 0 else \
                        "real_igual" if discriminante == 0 else "compleja"
            resultados.append([k, beta, m, raiz, tipo_raiz])

print(resultados)
