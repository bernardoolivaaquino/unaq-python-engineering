import numpy as np

# Crear una matriz de 2x2 [cite: 111, 161]
A = np.array([[1, 2], [3, 4]])

# Transpuesta e Inversa [cite: 164, 167]
A_transpuesta = A.T
A_inversa = np.linalg.inv(A)

# Propiedades de la matriz [cite: 140-143]
print("Forma:", A.shape)     # (filas, columnas)
print("Elementos:", A.size)  # Total de datos
print("Dimensiones:", A.ndim) # 2 para matrices
print(A.T)