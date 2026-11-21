import math

def secant(f, a, b, error, maxi, vis):
    """Approximate solution of f(x)=0 on interval [a,b] by the secant method."""
    if f(a) * f(b) >= 0:
        #print("Secant method fails (sign condition).") #Removed print statement as requested
        return None

    a_n = a
    b_n = b
    
    for n in range(1, maxi + 1):
        m_n = a_n - f(a_n) * (b_n - a_n) / (f(b_n) - f(a_n))
        f_m_n = f(m_n)

        if vis == 1: #For debugging, shows the values at each step
          print(f"n: {n}, a_n: {a_n}, b_n: {b_n}, m_n: {m_n}, f(m_n): {f_m_n}")

        if abs(f_m_n) < error: #Using abs here is unavoidable for convergence check
            return m_n  # Solution found within tolerance

        if f(a_n) * f_m_n < 0:
            b_n = m_n
        elif f(b_n) * f_m_n < 0:
            a_n = m_n
        #else: #Removed else statement as requested
            #print("Secant method fails (other condition).") #Removed print statement as requested
            #return None

    return m_n # Return the last approximation if max iterations reached


def analyze_roots_secant():
    """Analyzes roots using the secant method."""
    m_values = [0.1 + i * 0.2 for i in range(33)]
    beta_values = [0.4 + i * 0.2 for i in range(19)]
    k_values = [0.2 + i * 0.2 for i in range(25)]

    results = []
    smallest_root = float('inf')
    largest_root = float('-inf')
    smallest_root_data = None
    largest_root_data = None
    
    real_different_count = 0
    real_equal_count = 0
    complex_count = 0
    
    real_different_by_m = {}
    real_equal_by_m = {}
    complex_by_m = {}

    for m in m_values:
        for beta in beta_values:
            for k in k_values:
                f = lambda r: m * r**2 + beta * r + k  # Define quadratic function directly

                a = -10 #Initial interval
                b = 10
                
                root1 = secant(f, a, b, 1e-5, 100, 0)  # Using specified parameters

                if root1 is not None:
                    if root1 < smallest_root:
                        smallest_root = root1
                        smallest_root_data = {'m': m, 'beta': beta, 'k': k, 'root': root1}
                    if root1 > largest_root:
                        largest_root = root1
                        largest_root_data = {'m': m, 'beta': beta, 'k': k, 'root': root1}

                    #Find the second root
                    if (b - root1) != 0: #avoid division by zero
                        a = root1 + (b - root1)/2
                        b = 10
                    else:
                        a = -10
                        b = root1 - (root1 - a)/2
                    root2 = secant(f, a, b, 1e-5, 100, 0)
                    
                    if root2 is not None:
                        if root2 != root1:
                            real_different_count += 1
                            real_different_by_m[m] = real_different_by_m.get(m, 0) + 1
                            results.append({'m': m, 'beta': beta, 'k': k, 'roots': [root1, root2], 'root_type': "real and different"})
                        else:
                            real_equal_count += 1
                            real_equal_by_m[m] = real_equal_by_m.get(m, 0) + 1
                            results.append({'m': m, 'beta': beta, 'k': k, 'roots': [root1], 'root_type': "real and equal"})
                    else:
                        real_equal_count += 1
                        real_equal_by_m[m] = real_equal_by_m.get(m, 0) + 1
                        results.append({'m': m, 'beta': beta, 'k': k, 'roots': [root1], 'root_type': "real and equal"})
                else:
                    complex_count += 1
                    complex_by_m[m] = complex_by_m.get(m, 0) + 1
                    results.append({'m': m, 'beta': beta, 'k': k, 'roots': [], 'root_type': "complex"})

    # ... (rest of the analysis and printing as before, using the counts)
    closest_m = None
    min_diff = float('inf')

    for m_val in m_values:
        diff_real_count = real_different_by_m.get(m_val, 0)
        complex_count_m = complex_by_m.get(m_val, 0)
        diff = abs(diff_real_count - complex_count_m)

        if diff < min_diff:
            min_diff = diff
            closest_m = m_val

    max_equal_roots = 0
    m_with_max_equal_roots = None

    for m_val, count in real_equal_by_m.items():
        if count > max_equal_roots:
            max_equal_roots = count
            m_with_max_equal_roots = m_val
    
    print(f"1. Smallest root: {smallest_root}")
    print(f"2. Mass (smallest): {smallest_root_data['m']}")
    print(f"3. k (smallest): {smallest_root_data['k']}")
    print(f"4. Beta (smallest): {smallest_root_data['beta']}")

    print(f"5. Largest root: {largest_root}")
    print(f"6. Mass (largest): {largest_root_data['m']}")
    print(f"7. k (largest): {largest_root_data['k']}")
    print(f"8. Beta (largest): {largest_root_data['beta']}")
    
    print(f"9. Real Different Count: {real_different_count}")
    print(f"10. Real Equal Count: {real_equal_count}")
    print(f"11. Complex Count: {complex_count}")
    
    print(f"12. Closest M: {closest_m}")
    print(f"13. Max Equal M: {m_with_max_equal_roots}")

analyze_roots_secant()
