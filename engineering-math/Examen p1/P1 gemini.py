import math

def secant_method(f, a, b, E, imax, vis):
    """
    Finds a root of a function using the secant method (without using abs).

    Args:
        f: The function for which to find the root.
        a: The initial guess for the root (left endpoint).
        b: The initial guess for the root (right endpoint).
        E: The tolerance (error bound).
        imax: The maximum number of iterations.
        vis: A flag to control whether to print intermediate results (1 for print, 0 for no print).

    Returns:
        The approximate root of the function.
    """
    fa = f(a)
    fb = f(b)

    if fa > -E and fa < E:  # Replaces abs(fa) < E
        if vis == 1:
            print("a is a root")
        return a
    elif fb > -E and fb < E: # Replaces abs(fb) < E
        if vis == 1:
            print("b is a root")
        return b
    else:
        cont = 0
        while fa > E or fa < -E: # Replaces abs(fa) > E
            cont += 1
            if f(a) - f(b) == 0:
                if vis == 1:
                    print("Division by zero encountered. Choose different initial points.")
                return None  # Handle division by zero

            xr = a - (fa * (a - b)) / (f(a) - f(b))
            fr = f(xr)

            if vis == 1:
                print(cont, xr, fr)

            if fr > -E and fr < E: # Replaces abs(fr) < E
                if vis == 1:
                    print("xr is a root")
                return xr
            else:
                b = a
                a = xr
                fa = f(a)
                # fb = f(b)  # Not strictly necessary in the secant method

            if cont == imax:
                if vis == 1:
                    print("Reached maximum iterations")
                return xr


def find_roots_with_varying_parameters():
    """
    Finds the roots of the quadratic function m*r**2 + beta*r + k 
    for varying values of m, beta, and k using the secant method.
    """

    m_values = [0.1 + i * 0.2 for i in range(33)]
    beta_values = [0.4 + i * 0.2 for i in range(19)]
    k_values = [0.2 + i * 0.2 for i in range(25)]

    E = 1e-6  # Tolerance
    imax = 100  # Maximum iterations
    vis = 0  # Set to 1 to print intermediate steps

    results = []

    for m in m_values:
        for beta in beta_values:
            for k in k_values:
                f = lambda r: m * r**2 + beta * r + k

                # Initial guesses for the secant method
                a = -10
                b = 10

                root = secant_method(f, a, b, E, imax, vis)

                if root is not None:
                    results.append({'m': m, 'beta': beta, 'k': k, 'root': root})
    return results


# Example usage:
roots_data = find_roots_with_varying_parameters()

# Print or process the results
for data in roots_data:
    print(f"m={data['m']:.2f}, beta={data['beta']:.2f}, k={data['k']:.2f}, root={data['root']:.6f}")
