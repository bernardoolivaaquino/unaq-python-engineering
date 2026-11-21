import math


x = [0.5, 1, 1.2, 1.8, 2.6, 3, 3.1, 3.4, 3.5, 4.9]
y = [1.588, 1.939, 2.101, 2.671, 3.678, 4.316, 4.492, 5.065, 5.272, 9.229]

n = len(x)  
sx = sum(x)
sy = sum(y)
sxy = sum(x[i] * y[i] for i in range(n))
sx2 = sum(x[i] ** 2 for i in range(n))


a1 = (n * sxy - sx * sy) / (n * sx2 - sx ** 2)
a0 = (sy - a1 * sx) / n
for i in range(n):
        y.append(math.log(y[i]))
print(f"Pendiente (a1): {a1}")
print(f"Intercepto (a0): {a0}")
