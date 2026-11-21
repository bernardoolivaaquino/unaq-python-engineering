import math
import matplotlib.pyplot as plt

def solve_quadratic(m, beta, k):
    """Solves the quadratic equation m*r**2 + beta*r + k = 0."""
    discriminant = beta**2 - 4 * m * k
    roots = []

    if discriminant > 0:
        r1 = (-beta + math.sqrt(discriminant)) / (2 * m)
        r2 = (-beta - math.sqrt(discriminant)) / (2 * m)
        roots = [r1, r2]
        root_type = "real y diferente"
    elif discriminant == 0:
        r1 = -beta / (2 * m)
        roots = [r1]
        root_type = "real e igual"
    else:
        root_type = "complejo"

    return roots, root_type

def plot_roots(x_values, y_values, root_type_filter, x_label, y_label, title):
    """Plots the roots based on the specified criteria."""
    roots_data = []
    for m in m_values:
        for beta in beta_values:
            for k in k_values:
                roots, root_type = solve_quadratic(m, beta, k)
                if root_type == root_type_filter:
                   for root in roots:
                       if x_label == 'k':
                           x_val = k
                       elif x_label == 'm':
                           x_val = m
                       elif x_label == 'beta':
                           x_val = beta
                       roots_data.append((x_val, root))

    x_vals, y_vals = zip(*roots_data) if roots_data else ([], []) #unpacking for plotting, handles empty lists

    plt.figure()
    plt.scatter(x_vals, y_vals, s=1)  # Use scatter plot for individual points
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout() # Adjust layout to prevent labels from overlapping
    plt.show()


# Define ranges for m, beta, and k
m_values = [0.1 + i * 0.2 for i in range(33)]
beta_values = [0.4 + i * 0.2 for i in range(19)]
k_values = [0.2 + i * 0.2 for i in range(25)]


# Generate plots for each question
for x_label, root_type, question_num in [
    ('k', 'real y diferente', 14),
    ('m', 'real y diferente', 15),
    ('beta', 'real y diferente', 16),
    ('k', 'real e igual', 17),
    ('m', 'real e igual', 18),
    ('beta', 'real e igual', 19),
]:
    plot_roots(m_values, [], root_type, x_label, "Valor Raíz", f"Pregunta {question_num}: Raíces vs. {x_label}")

# Question 20: Roots vs. Mass (showing both real and complex)
roots_data = []

for m in m_values:
    for beta in beta_values:
        for k in k_values:
            roots, root_type = solve_quadratic(m, beta, k)
            for root in roots:
                roots_data.append((m, root, root_type))  # Include root type for coloring

m_vals, root_vals, root_types = zip(*roots_data) if roots_data else ([], [], [])

plt.figure()
# Separate real and complex roots for plotting
real_roots_x = [m for m, root, rt in zip(m_vals, root_vals, root_types) if rt != "complejo"]
real_roots_y = [root for m, root, rt in zip(m_vals, root_vals, root_types) if rt != "complejo"]

complex_roots_x = [m for m, root, rt in zip(m_vals, root_vals, root_types) if rt == "complejo"]
complex_roots_y = [root for m, root, rt in zip(m_vals, root_vals, root_types) if rt == "complejo"]

plt.scatter(real_roots_x, real_roots_y, label="Raíces reales", s=1)
# Complex roots would require special handling to plot on a 2D plane as they have imaginary components
# For visualization purposes, you might want to plot the magnitude or real part of the complex root.
# If you have complex roots, uncomment the line below (after appropriate complex number handling)
#plt.scatter(complex_roots_x, complex_roots_y, label="Complex Roots", s=1, color='red')

plt.xlabel("Masa (m)")
plt.ylabel("Valor Raíz")
plt.title("Pregunta 20: Raíces vs Masa")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
