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

# Análisis de resultados
min_raiz = min(r[3] for r in resultados if r[3] is not None)
max_raiz = max(r[3] for r in resultados if r[3] is not None)

min_params = next(
    {'k': r[0], 'beta': r[1], 'm': r[2]}
    for r in resultados
    if r[3] == min_raiz
)
max_params = next(
    {'k': r[0], 'beta': r[1], 'm': r[2]}
    for r in resultados
    if r[3] == max_raiz
)

print(f"1. Raíz mínima: {min_raiz}")
print(f"2. Masa con raíz mínima: {min_params['m']}")
print(f"3. Constante del resorte con raíz mínima: {min_params['k']}")
print(f"4. Constante de amortiguamiento con raíz mínima: {min_params['beta']}")
print(f"5. Raíz máxima: {max_raiz}")
print(f"6. Masa con raíz máxima: {max_params['m']}")
print(f"7. Constante del resorte con raíz máxima: {max_params['k']}")
print(f"8. Constante de amortiguamiento con raíz máxima: {max_params['beta']}")

conteo_raices = {}
for _, _, _, _, tr in resultados:
    conteo_raices[tr] = conteo_raices.get(tr, 0) + 1
print(f"9. Ecuaciones con raíces reales diferentes: {conteo_raices.get('real_diferente', 0)}")
print(f"10. Ecuaciones con raíces reales iguales: {conteo_raices.get('real_igual', 0)}")
print(f"11. Ecuaciones con raíces complejas: {conteo_raices.get('compleja', 0)}")

conteo_real_dif = {}
conteo_complejas = {}
conteo_iguales = {}

for k, beta, m, raiz, tr in resultados:
    if tr == 'real_diferente':
        conteo_real_dif[m] = conteo_real_dif.get(m, 0) + 1
    elif tr == 'compleja':
        conteo_complejas[m] = conteo_complejas.get(m, 0) + 1
    elif tr == 'real_igual':
        conteo_iguales[m] = conteo_iguales.get(m, 0) + 1

masa_dif_complejas = min(conteo_real_dif, key=lambda k: abs(conteo_real_dif[k] - conteo_complejas.get(k, 0) if k in conteo_complejas else conteo_real_dif[k]))
masa_max_iguales = max(conteo_iguales, key=conteo_iguales.get) if conteo_iguales else 'N/A'

print(f"12. Masa con número similar de raíces reales diferentes y complejas: {masa_dif_complejas}")
print(f"13. Masa con más raíces reales iguales: {masa_max_iguales}")
