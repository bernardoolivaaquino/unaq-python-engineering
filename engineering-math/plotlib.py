import matplotlib.pyplot as plt

x=[]
y=[]
z=[]
for i in range(200):
    x.append(i)
    y.append(0.1*i*i)
    z.append(0.1*i*i-10*i)
plt.plot(x,y,c="r",label="usuario 1")
plt.scatter(x,z,c="y",label="usuario 2")
plt.xlabel("eje x")
plt.ylabel("eje y")
plt.title("Gráfica 1")
plt.legend()
plt.show()
