import math

def f_a(x):
    return x**3 - 8*x + 12

def f_b(x):
    return math.sin(math.log(x)) + math.exp(0.5*x)

def f_c(x):
    return math.sin(x**2 + 3*x) - math.cos(math.sin(x)/x**3)

def forward_derivative(f, x, h):
    return (f(x + h) - f(x)) /(h)

def centered_derivative(f, x, h):
    return (f(x + h) - f(x - h)) / (2*h)

def forward_high_precision(f, x, h):
    return (-3*f(x) + 4*f(x + h) - f(x + 2*h)) / (2*h)

def backward_second_high_precision(f, x, h):
    return (2*f(x) - 5*f(x-h) + 4*f(x-2*h) - f(x-3*h)) / (h**2)

def backward_second_derivative(f, x, h):
    return (f(x) - 2*f(x-h) + f(x-2*h)) / (h**2)

def centered_second_high_precision(f, x, h):
    return (-f(x + 2*h) + 16*f(x + h) - 30*f(x) + 16*f(x - h) - f(x - 2*h)) / (12*h**2)

def backward_third_high_precision(f, x, h):
    return (5*f(x) - 18*f(x - h) + 24*f(x - 2*h) - 14*f(x - 3*h) + 3*f(x - 4*h)) / (2*h**3)

x = 3
h = 0.1

functions = {'f_a': f_a, 'f_b': f_b, 'f_c': f_c}

derivatives = {
    "Primera derivada hacia adelante": forward_derivative,
    "Primera derivada centrada": centered_derivative,
    "Primera derivada hacia adelante de alta precisión": forward_high_precision,
    "Segunda derivada hacia atrás de alta precisión": backward_second_high_precision,
    "Segunda derivada hacia atrás": backward_second_derivative,
    "Segunda derivada centrada de alta precisión": centered_second_high_precision,
    "Tercera derivada hacia atrás de alta precisión": backward_third_high_precision
}

results = {}
for name, func in functions.items():
    results[name] = {}
    for dname, dfunc in derivatives.items():
        results[name][dname] = dfunc(func, x, h)

for fname, dvals in results.items():
    print(f"Resultados para {fname} en x={x} con h={h}:")
    for dname, value in dvals.items():
        print(f"  {dname}: {value:.6f}")
    print("\n")
