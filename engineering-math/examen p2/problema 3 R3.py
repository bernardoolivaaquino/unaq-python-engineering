import math
import random
import matplotlib.pyplot as plt
import numpy as np # Importar numpy para usar en gráficos

# --- Constantes del Problema 3 ---
# Dimensiones de la lámina de aluminio original [source: 32, 69]
SHEET_LENGTH = 0.7      # metros
SHEET_WIDTH = 0.35     # metros (35 cm)
# Espesor de la lámina [source: 32]
SHEET_THICKNESS = 3.5e-3 # metros (3.5 mm)
# Densidad de la aleación de aluminio 7075 [source: 33, 69] (Valor típico)
DENSITY_AL7075 = 2810    # kg/m³
# Parámetros para los métodos de optimización
RANDOM_SEARCH_SAMPLES = 100 # Número de muestras para búsqueda aleatoria [source: 35, 72]
GOLDEN_SEARCH_TOL = 1e-6   # Tolerancia para la sección dorada (más precisa que 1e-5)
# Cálculo del límite superior para la altura 'h' del corte
# h debe ser menor que la mitad del lado más corto para poder doblar
MAX_H = SHEET_WIDTH / 2.0 # Límite superior = 0.35 / 2 = 0.175 m

# --- Inciso I: Construir Función de Volumen ---
# Fuente: [source: 33, 70]
def volumen_caja(h):
    """
    Calcula el volumen de la caja sin tapa formada al cortar cuadrados
    de lado 'h' de las esquinas de la lámina SHEET_LENGTH x SHEET_WIDTH.
    V(h) = (L - 2h) * (W - 2h) * h
    Args:
        h (float): Altura de la caja (lado del cuadrado cortado).
    Returns:
        float: Volumen de la caja en m³. Devuelve 0 si h está fuera del rango válido.
    """
    if 0 < h < MAX_H:
        largo_base = SHEET_LENGTH - 2 * h
        ancho_base = SHEET_WIDTH - 2 * h
        return largo_base * ancho_base * h
    else:
        # Volumen es 0 o no físico si h <= 0 o h >= MAX_H
        return 0

# --- Funciones Auxiliares (Área y Masa) ---
def calcular_area_superficie(h):
    """
    Calcula el área de la superficie del material utilizado para la caja sin tapa.
    Area = Area Base + Area Lado Largo * 2 + Area Lado Ancho * 2
    Args:
        h (float): Altura de la caja.
    Returns:
        float: Área de la superficie en m².
    """
    if 0 <= h < MAX_H: # Permitir h=0 para cálculo de masa teórica
        largo_base = SHEET_LENGTH - 2 * h
        ancho_base = SHEET_WIDTH - 2 * h
        area_base = largo_base * ancho_base
        area_lados_largos = 2 * largo_base * h
        area_lados_anchos = 2 * ancho_base * h
        return area_base + area_lados_largos + area_lados_anchos
    else:
        # Si h no es válida, el área física sería la de la hoja original,
        # pero para la caja formada, sería 0 o inválido.
        # Devolver 0 si h es inválida para la formación de la caja.
        return 0


# --- Incisos IV y V: Calcular Masa ---
# Fuentes: [source: 36, 73]
def calcular_masa(h):
    """
    Calcula la masa de la caja formada con altura 'h'.
    Masa = Volumen del material * Densidad = Area Superficie * Espesor * Densidad
    Args:
        h (float): Altura de la caja.
    Returns:
        float: Masa de la caja en kg.
    """
    area_superficie = calcular_area_superficie(h)
    masa = area_superficie * SHEET_THICKNESS * DENSITY_AL7075
    return masa

# --- Inciso II: Optimizar Volumen Máximo (Razón Dorada) ---
# Fuente: [source: 34, 71]
def razon_dorada_max(func, a, b, tol=GOLDEN_SEARCH_TOL):
    """
    Encuentra el valor de 'h' que maximiza la función 'func' (volumen_caja)
    en el intervalo [a, b] usando el método de la sección dorada.
    Args:
        func (callable): La función a maximizar (ej. volumen_caja).
        a (float): Límite inferior del intervalo de búsqueda para h.
        b (float): Límite superior del intervalo de búsqueda para h.
        tol (float): Tolerancia para la convergencia.
    Returns:
        tuple: (h_optimo, historial_h) donde h_optimo es la altura que maximiza
               el volumen y historial_h es una lista de las estimaciones de h
               en cada iteración.
    """
    gr = (math.sqrt(5) - 1) / 2  # Constante de la razón dorada (aprox 0.618)
    # Puntos interiores iniciales
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    historial_h = [] # Guardar historial para posible visualización

    while abs(c - d) > tol:
        historial_h.append((b + a) / 2) # Guardar punto medio como estimación actual
        # Comparar valores de la función en los puntos interiores
        if func(c) > func(d):
            # El máximo está en [a, d], descartar [d, b]
            b = d
            d = c # El nuevo d es el antiguo c
            c = b - gr * (b - a) # Calcular nuevo c
        else:
            # El máximo está en [c, b], descartar [a, c]
            a = c
            c = d # El nuevo c es el antiguo d
            d = a + gr * (b - a) # Calcular nuevo d

    # El óptimo está en el centro del intervalo final [a, b]
    h_optimo = (b + a) / 2
    historial_h.append(h_optimo)
    return h_optimo, historial_h

# --- Inciso III: Optimizar Volumen Mínimo (Búsqueda Aleatoria) ---
# Fuente: [source: 35, 72]
def optimizacion_aleatoria_min(func, low, high, n=RANDOM_SEARCH_SAMPLES):
    """
    Encuentra el valor de 'h' que minimiza la función 'func' (volumen_caja)
    en el intervalo (low, high) usando búsqueda aleatoria.
    Args:
        func (callable): La función a minimizar (ej. volumen_caja).
        low (float): Límite inferior (exclusivo) del intervalo para h.
        high (float): Límite superior (exclusivo) del intervalo para h.
        n (int): Número de muestras aleatorias a tomar.
    Returns:
        tuple: (h_optimo, historial_h) donde h_optimo es la altura que dio el
               mínimo volumen encontrado y historial_h es la lista de todas
               las alturas muestreadas.
    """
    mejor_h = None
    mejor_valor = math.inf  # Inicializar con infinito para encontrar el mínimo
    historial_h = [] # Guardar todas las h muestreadas

    for _ in range(n):
        # Generar h aleatoria en el intervalo abierto (low, high)
        # Usamos un pequeño épsilon para evitar exactamente 0 y MAX_H si es necesario,
        # pero random.uniform ya genera en [low, high), lo cual es bueno aquí.
        # Asegurémonos que h no sea exactamente 0 o MAX_H si func(0) o func(MAX_H) es problemático,
        # aunque nuestra función volumen_caja devuelve 0 para esos casos.
        # El intervalo estricto es (0, MAX_H) para un volumen > 0.
        h_actual = random.uniform(low, high)
        # Para asegurar estrictamente > low y < high:
        # epsilon = 1e-9 # Un valor pequeño
        # h_actual = random.uniform(low + epsilon, high - epsilon)

        historial_h.append(h_actual)
        valor_actual = func(h_actual)

        # Actualizar si encontramos un valor menor
        if valor_actual < mejor_valor:
            mejor_valor = valor_actual
            mejor_h = h_actual

    # Nota: El mínimo volumen teórico > 0 ocurre cuando h tiende a 0 o a MAX_H.
    # La búsqueda aleatoria encontrará el h muestreado que produce el menor volumen,
    # que probablemente será muy cercano a 0 o a MAX_H.
    return mejor_h, historial_h

# --- Ejecución Principal y Resultados ---

print("Resolviendo Problema 3...")
print("---------------------------------------")
print(f"Dimensiones lámina: L={SHEET_LENGTH} m, W={SHEET_WIDTH} m")
print(f"Intervalo válido para altura h: (0, {MAX_H}) m")
print("---------------------------------------")

# II. Optimizar para Máximo Volumen
h_max, historial_max = razon_dorada_max(volumen_caja, 0, MAX_H)
volumen_max = volumen_caja(h_max)
# IV. Calcular Masa para Máximo Volumen
m_max = calcular_masa(h_max)

print(f"[II] Altura óptima para MÁXIMO volumen (Razón Dorada): h = {h_max:.6f} m")
print(f"     Volumen máximo correspondiente: V_max = {volumen_max:.6f} m³")
print(f"[IV] Masa de la caja con volumen máximo: m_max = {m_max:.4f} kg")
print("---------------------------------------")

# III. Optimizar para Mínimo Volumen
# Buscamos en (0, MAX_H) porque en h=0 y h=MAX_H el volumen es exactamente 0.
# Si buscamos el mínimo > 0, el intervalo debería ser (epsilon, MAX_H - epsilon).
# Pero como el método es numérico y se pide búsqueda aleatoria,
# buscar en [0, MAX_H] con uniform() está bien, encontrará h cerca de los bordes.
h_min, historial_min_h = optimizacion_aleatoria_min(volumen_caja, 0, MAX_H)
volumen_min = volumen_caja(h_min)
# V. Calcular Masa para Mínimo Volumen
m_min = calcular_masa(h_min)

print(f"[III] Altura encontrada para MÍNIMO volumen (Búsqueda Aleatoria, n={RANDOM_SEARCH_SAMPLES}): h = {h_min:.6f} m")
print(f"      Volumen mínimo encontrado: V_min = {volumen_min:.6f} m³")
print(f"      (Nota: El V_min encontrado será cercano a 0, ya que V tiende a 0 en h=0 y h={MAX_H})")
print(f"[V]  Masa de la caja con volumen mínimo encontrado: m_min = {m_min:.4f} kg")
print("---------------------------------------")


# --- Visualizaciones ---

# 1. Gráfica de la función Volumen vs Altura
h_vals = np.linspace(0, MAX_H, 200) # Generar valores de h en el intervalo [0, MAX_H]
v_vals = [volumen_caja(h) for h in h_vals] # Calcular volumen para cada h

plt.figure(figsize=(8, 6))
plt.plot(h_vals, v_vals, label='V(h) = (L-2h)(W-2h)h')
plt.scatter([h_max], [volumen_max], color='red', zorder=5, label=f'Máximo V={volumen_max:.4f} en h={h_max:.4f}')
plt.xlabel('Altura del corte, h (m)')
plt.ylabel('Volumen de la caja, V (m³)')
plt.title('Volumen de la Caja vs. Altura del Corte')
plt.grid(True)
plt.legend()
plt.ylim(bottom=0) # Asegurar que el eje y empiece en 0
plt.xlim(left=0, right=MAX_H)
plt.show()

# 2. Gráfica de Convergencia de la Razón Dorada (Opcional)
# Se grafica el volumen en las estimaciones de h (puntos medios) de cada iteración
volumenes_hist_max = [volumen_caja(h) for h in historial_max]
plt.figure(figsize=(8, 6))
plt.plot(range(len(historial_max)), volumenes_hist_max, marker='o', linestyle='-')
plt.xlabel('Iteración de la Razón Dorada')
plt.ylabel('Volumen estimado V(h) (m³)')
plt.title('Convergencia del Método de la Razón Dorada para Máximo Volumen')
plt.grid(True)
# plt.yscale('log') # Puede ser útil si converge muy rápido
plt.show()

# 3. Gráfica de la Búsqueda Aleatoria (Opcional)
# Muestra los puntos (h, V(h)) evaluados durante la búsqueda aleatoria
volumenes_hist_min = [volumen_caja(h) for h in historial_min_h]
plt.figure(figsize=(8, 6))
plt.scatter(historial_min_h, volumenes_hist_min, s=10, alpha=0.6, label=f'{RANDOM_SEARCH_SAMPLES} muestras')
plt.scatter([h_min], [volumen_min], color='red', zorder=5, s=50, label=f'Mínimo encontrado V={volumen_min:.4f} en h={h_min:.4f}')
plt.xlabel('Altura del corte, h (m)')
plt.ylabel('Volumen de la caja, V (m³)')
plt.title(f'Muestras de la Búsqueda Aleatoria (n={RANDOM_SEARCH_SAMPLES}) para Mínimo Volumen')
plt.grid(True)
plt.legend()
plt.ylim(bottom=0)
plt.xlim(left=0, right=MAX_H)
plt.show()