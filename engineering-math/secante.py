f= lambda x: (0.1*x**2)+0.4*x+0.2
g= lambda x: 2*x-9
def sec(f, a, b,  E, imax, vis):
    fa=f(a)
    fb=f(b)
    if fa>(0-E) and fa<(0+E):
        print("a es raiz")
        return a
    elif fb>(0-E) and fb<(0+E):
        print("b es raiz")
        return b
    else:
        cont=0
        while fa<(0-E) or fa>(0+E):
            cont+=1
            xr=((a)-((fa*(a-b))/(f(a)-f(b))))
            fr=f(xr)
            if vis==1:
                print(cont, xr, fr)
            if fr>(0-E) and fr<(0+E):
                print("xr es raiz")
                return xr
            else:
                b=a
                a=xr
                fa=f(a)
                fb=f(b)
            if cont==imax:
                print("Alcanzaste iteraciones maximas")
            return xr
