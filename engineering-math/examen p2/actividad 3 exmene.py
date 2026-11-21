import math
import random
import matplotlib.pyplot as plt

def volumen_caja(h):
    """Calcula el volumen de la caja sin tapa."""
    L = 0.7  
    W = 0.35  
    return (L - 2 * h) * (W - 2 * h) * h

def calcular_area_superficie(h):
    """Calcula el área de la superficie de la caja sin tapa."""
    largo = 0.7 - 2 * h
    ancho = 0.35 - 2 * h
    return (largo * ancho) + (2 * largo * h) + (2 * ancho * h)

def razon_dorada(a, b, tol=1e-5):
    """Encuentra la altura óptima para el máximo volumen usando la razón dorada."""
    gr = (math.sqrt(5) - 1) / 2  # Razón dorada
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    alturas = []
    while abs(c - d) > tol:
        alturas.append((b + a) / 2)
        if volumen_caja(c) > volumen_caja(d):
            b = d
        else:
            a = c
        c = b - gr * (b - a)
        d = a + gr * (b - a)

    return (b + a) / 2, alturas  

def optimizacion_aleatoria(n=100):
    """Encuentra la altura óptima para el mínimo volumen usando búsqueda aleatoria."""
    mejor_h = None
    mejor_volumen = math.inf  
    alturas = []
    for _ in range(n):
        h = random.uniform(0, 0.175)  
        v = volumen_caja(h)
        alturas.append(h)
        if v < mejor_volumen or mejor_h is None:
            mejor_h = h
            mejor_volumen = v

    return mejor_h, alturas  

def calcular_masa(h):
    """Calcula la masa de la caja."""
    densidad_aluminio_7075 = 2810  
    espesor = 3.5e-3  
    area_superficie = calcular_area_superficie(h)
    return area_superficie * espesor * densidad_aluminio_7075


h_max, alturas_max = razon_dorada(0, 0.175)  
h_min, alturas_min = optimizacion_aleatoria()
volumen_max = volumen_caja(h_max)
volumen_min = volumen_caja(h_min)
m_max = calcular_masa(h_max)
m_min = calcular_masa(h_min)

print(f"Altura óptima (máximo volumen): {h_max:.4f} m")
print(f"Volumen máximo: {volumen_max:.4f} m³")
print(f"Masa para volumen máximo: {m_max:.4f} kg")
print(f"Altura óptima (mínimo volumen): {h_min:.4f} m")
print(f"Volumen mínimo: {volumen_min:.4f} m³")
print(f"Masa para volumen mínimo: {m_min:.4f} kg")


alturas = [0.175 * i / 99 for i in range(100)] 
volumenes = [volumen_caja(h) for h in alturas]
plt.figure(figsize=(8, 6))
plt.plot(alturas, volumenes)
plt.xlabel('Altura (m)')
plt.ylabel('Volumen (m³)')
plt.title('Volumen de la caja vs. Altura')
plt.grid(True)
plt.show()


volumenes_max = [volumen_caja(h) for h in alturas_max]
plt.figure(figsize=(8, 6))
plt.plot(alturas_max, volumenes_max, marker='o')
plt.xlabel('Altura (m)')
plt.ylabel('Volumen (m³)')
plt.title('Convergencia de la Razón Dorada (Máximo Volumen)')
plt.grid(True)
plt.show()


volumenes_min = [volumen_caja(h) for h in alturas_min]
plt.figure(figsize=(8, 6))
plt.scatter(alturas_min, volumenes_min, s=10)
plt.xlabel('Altura (m)')
plt.ylabel('Volumen (m³)')
plt.title('Búsqueda Aleatoria (Mínimo Volumen)')
plt.grid(True)
plt.show()
