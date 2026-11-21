def forward_derivative(f, xi, h):
  """
  Calculates the first numeric derivative of a function using the forward difference scheme.

  Args:
    f: The function to differentiate (a callable object).
    xi: The point at which to calculate the derivative.
    h: The step size (error).

  Returns:
    The approximate derivative at xi.
  """
  return (f(xi + h) - f(xi)) / h

# Example Usage:
def my_function(x):
  return 3*x**3+27*x**2-30*x+5  # Example function: f(x) = x^2

xi_value = 30
step_size = 0.01

derivative_approximation = forward_derivative(my_function, xi_value, step_size)
print(f"Approximate derivative of f(x) at x = {xi_value}: {derivative_approximation}")

# Demonstrating the error being proportional to h

def forward_derivative_with_error(f, xi, h):
    """
    Calculates the first numeric derivative of a function using the forward difference scheme,
    and returns the result.
    """
    return (f(xi + h) - f(xi)) / h

def actual_derivative(xi):
    """
    The actual derivative of my_function(x) = x^2, which is 2x.
    """
    return 2 * xi

xi_value = 2.0
step_sizes = [0.1, 0.05, 0.01, 0.001, 0.0001] # varying step sizes

print("\nDemonstrating error proportional to h:")
print("h\tApproximate Derivative\tActual Derivative\tError")

for h in step_sizes:
    approx_deriv = forward_derivative_with_error(my_function, xi_value, h)
    actual_deriv = actual_derivative(xi_value)
    error = abs(approx_deriv - actual_deriv) #absolute value of error
    print(f"{h}\t{approx_deriv:.6f}\t\t{actual_deriv:.6f}\t\t{error:.6f}")
