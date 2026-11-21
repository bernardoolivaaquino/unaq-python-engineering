import matplotlib.pyplot as plt

x=[]
y=[]
z=[]
for i in range(200):
    x.append(i)
    y.append(0.1*i*i)
    z.append(0.1*i*i-10*i)
plt.figure(10)
plt.plot(x,y,c="r",label="usuario 1")
plt.xlabel("eje x")
plt.ylabel("eje y")
plt.title("Gráfica 1")
plt.legend()
plt.figure(11)
plt.scatter(x,z,c="y",label="usuario 2")
plt.xlabel("eje x")
plt.ylabel("eje y")
plt.title("Gráfica 2")
plt.legend()
fig,ax=plt.subplots(2,2)
ax[0,0].plot(x,y)
ax[0,1].scatter(x,y)
ax[1,0].plot(x,z)
ax[1,1].scatter(x,z)
ax[0,0].set_xlabel("x")
ax[0,0].set_xlabel("y")
ax[0,0].set_title("titulo 1")


plt.show()
