def corrector(f,x0,y0,b,h,n):
    y1=y0+f(x0,y0)*h
    for i in range(n):
        ym=y0+(f(x0,y0)+f(x0+h,y1))*h/2
        y1=ym
    return ym
def heunC(f,x0,y0,b,h,m):
    n=math.ceil((b-x0)/h)
    x=[x0]
    y=[y0]
    for i in range(n):
        x.append(x0+(i+1)*h)
        y1=corrector(f,x[i],y[i],b,h,m)
        y.append(y1)
    return n,x,y