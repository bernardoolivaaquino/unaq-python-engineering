import numpy as n

#Ejercicio 1
vector = n.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
suma=n.sum(vector)
promedio= n.mean(vector)

print("Vector:", vector)
print("Suma:", suma, "Promedio:",promedio)


#Ejercicio 2
A = n.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
B = n.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])

suma=A+B
resta=A-B
multiplicacion= A@B 

print("\nMatrices:")
print("Suma:\n",suma)
print("Resta:\n",resta)
print("Multiplicación:\n", multiplicacion)


#Ejercicio 3
C = n.array([[1, 0, 5], [2, 1, 6], [3, 4, 0]])
transpuesta=n.transpose(C) 
inversa=n.linalg.inv(C) 
print("Transpuesta:\n", transpuesta)
print("Inversa:\n", inversa)


#Ejercicio 4
determinante = n.linalg.det(C)
print("\nDeterminante de C:", determinante)