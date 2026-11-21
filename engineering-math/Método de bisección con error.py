import math
f= lambda x: (x**3)-9*x**2+6*x+16
def bis(f,a,b,e):
    a=-4
    b=-0.5
    fa=f(a)
    fb=f(b)
    if fa*fb>(0-e) and fa*fb<(0+e):
        print ("raiz a o b")
    elif fa*fb>(0+e):
        print ("no raiz")
    else :
        h=0
        cont=0
        while h==0:
            r=((a+b)/2)
            fr=f(r)
            if fr>(0-e) and fr<(0+e):
                #print(r)
                h=1
                return r
            else:
                 if fa*fr>(0+e):
                     a=r
                     b=b
                 else:
                    a=a
                    b=r
            cont=cont+1
            print(cont,r)
            if cont==1e8:
                return r
            
#print(r)
            
