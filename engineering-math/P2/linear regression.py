import math
x = [0.5, 1, 1.2, 1.8, 2.6, 3, 3.1, 3.4, 3.5, 4.9]
y = [1.250, 1.765, 1.895, 2.160, 2.364, 2.432, 2.447, 2.488, 2.500, 2.625]
def regresion_lineal(x, y):
    n = len(x)
    yt = []


    for i in range(n):
        yt.append(math.log(y[i]))

    sx = sum(x)
    syt = sum(yt) 
    sxyt = sum(x[i] * yt[i] for i in range(n)) 
    sx2 = sum(x[i] ** 2 for i in range(n))

    a1 = (n * sxyt - sx * syt) / (n * sx2 - sx ** 2)
    a0 = (syt - a1 * sx) / n

    print(f"Pendiente (a1): {a1}")
    print(f"Intercepto (a0): {a0}")
def regresion_lineal1(x,y):
    n=len(x)
    yt=[]
    for i in range (n):
        yt.append(math.log(y[i]))
    res=regresion_lineal(x,yt)
    alpha=math.e**(res[0])
    beta=res[1]
    r=res[2]
    r2=res[3]
    return alpha, beta, r, r2
    print (alpha,beta,r,r2)

regresion_lineal(x, y)
