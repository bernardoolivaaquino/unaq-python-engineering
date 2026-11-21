import math

def golden_ratio_search(func, a, b, tolerance):
    """
    Finds the minimum of a unimodal function within a given interval using the Golden Ratio search method.

    Args:
        func: The function to minimize (must be callable).
        a: The left endpoint of the interval.
        b: The right endpoint of the interval.
        tolerance: The desired accuracy of the solution.

    Returns:
        A tuple containing:
            - The approximate x-value that minimizes the function.
            - The minimum function value.
            - The number of iterations performed.
    """

    # Golden ratio constant
    phi = (1 + math.sqrt(5)) / 2

    # Initial interval length
    interval_length = b - a

    # Initialize x1 and x2
    x1 = b - (b - a) / phi  # x1 is closer to 'a'
    x2 = a + (b - a) / phi  # x2 is closer to 'b'

    # Initialize function values at x1 and x2
    f1 = func(x1)
    f2 = func(x2)

    iterations = 0

    while interval_length > tolerance:
        iterations += 1
        if f1 < f2: # if f1 is better than f2
            b = x2 # Update the upper bound
            x2 = x1 # shift x1 to be the new x2
            f2 = f1 # shift f1 to be the new f2
            x1 = b - (b - a) / phi # compute the new x1
            f1 = func(x1) # compute the new f1
        else: # if f2 is better or equal than f1
            a = x1 # update the lower bound
            x1 = x2 # shift x2 to be the new x1
            f1 = f2 # shift f2 to be the new f1
            x2 = a + (b - a) / phi # compute the new x2
            f2 = func(x2) # compute the new f2
        interval_length = b - a  # Update interval length

    # Return the midpoint of the final interval as the approximate minimum
    xmin = (a + b) / 2
    fmin = func(xmin)  # Evaluate the function at the approximate minimum

    return xmin, fmin, iterations


# Get user input
try:
    func_str = input("Enter the function in terms of 'x' (e.g., x**2 - 2*x + 1): ")
    func = lambda x: eval(func_str)  # Define function from user input
    a = float(input("Enter the lower bound of the interval: "))
    b = float(input("Enter the upper bound of the interval: "))
    tolerance = float(input("Enter the desired tolerance: "))

    # Perform golden ratio search
    xmin, fmin, iterations = golden_ratio_search(func, a, b, tolerance)

    print(f"Approximate minimum x: {xmin}")
    print(f"Minimum function value: {fmin}")
    print(f"Number of iterations: {iterations}")

except (ValueError, SyntaxError, NameError, TypeError, ZeroDivisionError) as e:
    print(f"Invalid input. Please check your function definition and numerical values. Error details: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
