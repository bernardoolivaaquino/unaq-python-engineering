import math

f= lambda x: x**2+2*x-24
def bis(f, a, b,E, vis):
    a=-1
    b=7
    fa=f(a)
    fb=f(b)
    if fa*fb<(0+E) and fa*fb>(0-E):
        print("Raiz a o b")
    elif fa*fb>0+E:
         print("No hay raiz")
    else:
        h=0
        cont=0
        while h==0:
          xr=((a+b)/2)
          fr=f(xr)
          if vis==1:
              print(cont, xr, f(xr))
          if fr<(0+E) and fr>(0-E):
              print(xr)
              h=1
              return xr
          else:
              if fa*fr>0+E:
                 a=xr
                 b=b
              else:
                  a=a
                  b=xr
          cont=cont+1
          print(cont, xr)
          if cont==1e8:
              return xr
#print(xr)
