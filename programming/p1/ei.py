import numpy as np
import pandas as pd

# EJERCICIO 1: Datos y proyección [cite: 1045-1047]
nombre = input("Ex 1 - Nombre: ")
edad = int(input("Edad: "))
print(f"Hola {nombre}, en 10 años tendrás {edad + 10} años.\n")

# EJERCICIO 2: Paridad [cite: 1048]
n2 = int(input("Ex 2 - Número entero: "))
print(f"Es {'par' if n2 % 2 == 0 else 'impar'}.\n")

# EJERCICIO 3: Ciclo y potencias [cite: 1049-1053]
print("Ex 3 - Números 1-10 y sus cuadrados:")
for i in range(1, 11):
    print(f"{i} = {i**2}")

# EJERCICIO 4: Función Primo [cite: 1054-1055]
def es_primo(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True
n4 = int(input("\nEx 4 - Número para probar primo: "))
print(f"¿Es primo?: {es_primo(n4)}\n")

# EJERCICIO 5: Promedio de calificaciones [cite: 1056-1059]
def calcular_promedio(lista):
    return sum(lista) / len(lista)

cals = [float(input(f"Ex 5 - Nota {i+1}: ")) for i in range(5)]
p5 = calcular_promedio(cals)
print(f"Promedio: {p5} - {'Aprobado' if p5 >= 70 else 'Reprobado'}\n")

# ... (Los ejercicios 6 al 15 se omiten aquí por brevedad, pero se mantienen igual en tu archivo final)

# =============================================================================
# BLOQUE 2: ACTIVIDAD 6 - PRODUCCIÓN Y COSTOS [cite: 174-185]
# =============================================================================

# EJERCICIO 16 (Actividad 6.1): Registro de producción [cite: 175-180]
# Concepto: argmax() devuelve el índice del valor más alto.
v_prod = np.array([20, 50, 34, 92, 105, 16, 34, 54])
total_p = np.sum(v_prod)
prom_p = np.mean(v_prod)
hora_m = np.argmax(v_prod) # Índice del máximo

print("--- ACTIVIDAD 6 ---")
print(f"Total producido: {total_p}")
print(f"Promedio por hora: {prom_p}")
print(f"Hora con mayor producción: {hora_m + 1}\n") # +1 porque los índices inician en 0

# EJERCICIO 17 (Actividad 6.2): Costos de materiales (Pandas) [cite: 181-185]
# Concepto: DataFrame organiza datos en tablas con etiquetas.
# axis=0: Suma por columnas (materiales).
# axis=1: Suma por filas (proveedores).
matriz_c = np.array([[32, 54], [15, 43]])
proveedores = ["Ferretería", "HomeDepot"]
materiales = ["Acero", "Cemento"]

df = pd.DataFrame(data=matriz_c, index=proveedores, columns=materiales)
print("Tabla de Costos:\n", df)

costo_mat = np.sum(matriz_c, axis=0)
costo_prov = np.sum(matriz_c, axis=1)
print(f"Costo total por materiales (Acero, Cemento): {costo_mat}")
print(f"Costo total por proveedores (Ferretería, HomeDepot): {costo_prov}\n")

# =============================================================================
# BLOQUE 3: ACTIVIDAD 7 - ÁLGEBRA LINEAL [cite: 191-198]
# =============================================================================

# EJERCICIO 18 (Actividad 7.1): Vector de 10 números [cite: 195]
v10 = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
print("--- ACTIVIDAD 7 ---")
print(f"Vector: {v10}")
print(f"Suma: {np.sum(v10)}, Promedio: {np.mean(v10)}\n")

# EJERCICIO 19 (Actividad 7.2): Operaciones 3x3 [cite: 196]
# Concepto: @ realiza multiplicación de matrices (punto), no elemento a elemento.
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
B = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])

print("Suma A+B:\n", A + B)
print("Resta A-B:\n", A - B)
print("Multiplicación Matricial (A @ B):\n", A @ B, "\n")

# EJERCICIO 20 (Actividad 7.3): Transpuesta e Inversa [cite: 197]
# Concepto: La inversa requiere que el determinante sea distinto de 0.
C = np.array([[1, 0, 5], [2, 1, 6], [3, 4, 0]])
trans = np.transpose(C) 
inv = np.linalg.inv(C) 

print("Transpuesta de C:\n", trans)
print("Inversa de C:\n", inv, "\n")

# EJERCICIO 21 (Actividad 7.4): Determinante 
# Fórmula: det(C) indica si la matriz tiene inversa.
det_c = np.linalg.det(C)
print(f"Determinante de C: {det_c:.2f}")