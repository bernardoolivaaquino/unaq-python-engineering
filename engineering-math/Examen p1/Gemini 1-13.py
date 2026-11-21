import math

def solve_quadratic(m, beta, k):
    """
    Solves the quadratic equation m*r**2 + beta*r + k = 0 using the quadratic formula.

    Args:
        m: The coefficient of r**2 (mass).
        beta: The coefficient of r (damping constant).
        k: The constant term (spring constant).

    Returns:
        A tuple containing:
        - A list of the roots (empty if no real roots).
        - A string indicating the type of roots: "real and different", "real and equal", or "complex".
    """
    discriminant = beta**2 - 4 * m * k
    roots = []

    if discriminant > 0:
        r1 = (-beta + math.sqrt(discriminant)) / (2 * m)
        r2 = (-beta - math.sqrt(discriminant)) / (2 * m)
        roots = [r1, r2]
        root_type = "real and different"
    elif discriminant == 0:
        r1 = -beta / (2 * m)
        roots = [r1]
        root_type = "real and equal"
    else:
        root_type = "complex"

    return roots, root_type


def analyze_roots():
    """
    Analyzes the roots of the quadratic equation for varying values of m, beta, and k.
    """
    m_values = [0.1 + i * 0.2 for i in range(33)]
    beta_values = [0.4 + i * 0.2 for i in range(19)]
    k_values = [0.2 + i * 0.2 for i in range(25)]

    results = []
    
    different_real_roots_count = 0
    equal_real_roots_count = 0
    complex_roots_count = 0
    
    different_real_roots_by_m = {}
    equal_real_roots_by_m = {}
    complex_roots_by_m = {}


    for m in m_values:
        for beta in beta_values:
            for k in k_values:
                roots, root_type = solve_quadratic(m, beta, k)

                if root_type == "real and different":
                    different_real_roots_count +=1
                    different_real_roots_by_m[m] = different_real_roots_by_m.get(m, 0) + 1
                elif root_type == "real and equal":
                    equal_real_roots_count +=1
                    equal_real_roots_by_m[m] = equal_real_roots_by_m.get(m, 0) + 1
                else:
                    complex_roots_count +=1
                    complex_roots_by_m[m] = complex_roots_by_m.get(m, 0) + 1

                if roots:  # If there are roots
                    results.append({'m': m, 'beta': beta, 'k': k, 'roots': roots, 'root_type': root_type})
    
    # Find smallest and largest roots
    smallest_root = float('inf')
    largest_root = float('-inf')
    smallest_root_data = None
    largest_root_data = None
    
    for data in results:
      for root in data['roots']:
        if root < smallest_root:
            smallest_root = root
            smallest_root_data = data
        if root > largest_root:
            largest_root = root
            largest_root_data = data
            
    # Find m with most similar count of different real and complex roots
    closest_m = None
    min_diff = float('inf')

    for m in m_values:
      diff_real_count = different_real_roots_by_m.get(m, 0)
      complex_count = complex_roots_by_m.get(m, 0)
      diff = abs(diff_real_count - complex_count)
    
      if diff < min_diff:
          min_diff = diff
          closest_m = m
          
    # Find m with the highest number of equal real roots
    max_equal_roots = 0
    m_with_max_equal_roots = None

    for m, count in equal_real_roots_by_m.items():
        if count > max_equal_roots:
            max_equal_roots = count
            m_with_max_equal_roots = m
    
    

    # Print the results

    print(f"1. The smallest root is: {smallest_root:.6f}")
    print(f"2. The mass (m) with the smallest root is: {smallest_root_data['m']:.2f}")
    print(f"3. The spring constant (k) with the smallest root is: {smallest_root_data['k']:.2f}")
    print(f"4. The damping constant (beta) with the smallest root is: {smallest_root_data['beta']:.2f}")

    print(f"5. The largest root is: {largest_root:.6f}")
    print(f"6. The mass (m) with the largest root is: {largest_root_data['m']:.2f}")
    print(f"7. The spring constant (k) with the largest root is: {largest_root_data['k']:.2f}")
    print(f"8. The damping constant (beta) with the largest root is: {largest_root_data['beta']:.2f}")

    print(f"9. Number of equations with different real roots: {different_real_roots_count}")
    print(f"10. Number of equations with equal real roots: {equal_real_roots_count}")
    print(f"11. Number of equations with complex roots: {complex_roots_count}")
    print(f"12. The value of mass (m) for which the number of different real roots and complex roots is most similar is: {closest_m:.2f}")
    print(f"13. The value of mass (m) with the highest number of equal real roots: {m_with_max_equal_roots:.2f}")



analyze_roots()
