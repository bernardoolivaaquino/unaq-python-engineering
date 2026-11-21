import matplotlib.pyplot as plt
import numpy as np

# --- Datos del Ensayo (Comunes a Prob. 3-2 y 3-3) ---
# Esfuerzo (sigma) en ksi (kilopounds per square inch)
esfuerzo_ksi = np.array([0, 33.2, 45.5, 49.4, 51.5, 53.4])
# Deformación unitaria (epsilon) en in/in (adimensional)
deformacion_in_in = np.array([0, 0.0006, 0.0010, 0.0014, 0.0018, 0.0022])

# --- Graficación del Diagrama Esfuerzo-Deformación (Común a ambos problemas) ---
plt.figure(figsize=(8, 6))
plt.plot(deformacion_in_in, esfuerzo_ksi, marker='o', linestyle='-', color='b') # Graficar puntos y líneas
plt.title('Diagrama Esfuerzo-Deformación para Material Cerámico')
plt.xlabel('Deformación Unitaria ($\epsilon$) [in/in]')
plt.ylabel('Esfuerzo ($\sigma$) [ksi]')
plt.grid(True)
plt.xlim(left=0)
plt.ylim(bottom=0)

# Resaltar la región elástica lineal y el límite proporcional
plt.plot([0, deformacion_in_in[1]], [0, esfuerzo_ksi[1]], color='red', linestyle='--', linewidth=2, label=f'Región Lineal (hasta $\sigma_{{pl}}={esfuerzo_ksi[1]}$ ksi)')
plt.scatter([deformacion_in_in[1]], [esfuerzo_ksi[1]], color='red', zorder=5) # Marca el punto pl
plt.legend()

print("Generando la gráfica del diagrama esfuerzo-deformación...")
plt.show()

# --- Cálculos para Prob. 3-2 ---

# 1. Módulo de Elasticidad (E)
# La curva es lineal entre el origen (0,0) y el primer punto (e1, s1)
sigma_1 = esfuerzo_ksi[1]  # 33.2 ksi (Este es el límite proporcional, sigma_pl)
epsilon_1 = deformacion_in_in[1] # 0.0006 in/in (Esta es la deformación en el límite prop., epsilon_pl)

# E es la pendiente en la región lineal: E = sigma_1 / epsilon_1
modulo_elasticidad_E_ksi = sigma_1 / epsilon_1

# Asignar límite proporcional para claridad
sigma_pl = sigma_1
epsilon_pl = epsilon_1

# 2. Módulo de Resiliencia (Ur)
# Es el área bajo la curva hasta el límite proporcional (área del triángulo)
# Ur = 0.5 * sigma_pl * epsilon_pl
modulo_resiliencia_Ur_ksi = 0.5 * sigma_pl * epsilon_pl
# Verificación alternativa: Ur = sigma_pl^2 / (2*E)
# modulo_resiliencia_Ur_alt = (sigma_pl**2) / (2 * modulo_elasticidad_E_ksi)

# --- Cálculos para Prob. 3-3 ---

# 3. Módulo de Tenacidad (Ut) Aproximado
# Es el área total bajo la curva hasta la fractura (usando regla del trapecio)
# El último punto (e_f, s_f) es (0.0022, 53.4)
modulo_tenacidad_Ut_ksi = np.trapz(esfuerzo_ksi, deformacion_in_in)

# --- Resultados ---
print("\n--- Resultados del Análisis ---")
# Usamos list() para una impresión más limpia de los arrays
print(f"Datos de Esfuerzo (σ) [ksi]: {list(esfuerzo_ksi)}")
print(f"Datos de Deformación (ε) [in/in]: {list(deformacion_in_in)}")

print("\n--- Resultados para Problema 3-2 ---")
print("1. Módulo de Elasticidad (E):")
print(f"   Se calcula usando la pendiente de la región lineal inicial (hasta el punto 1).")
print(f"   Punto 1: ε₁ = {epsilon_1} in/in, σ₁ = {sigma_1} ksi")
print(f"   Fórmula: E = σ₁ / ε₁")
print(f"   E = {sigma_1} ksi / {epsilon_1} in/in")
# Muestra el resultado en ksi y en psi (ksi * 1000)
print(f"   E ≈ {modulo_elasticidad_E_ksi:.1f} ksi")
print(f"   E ≈ {modulo_elasticidad_E_ksi * 1000:.1f} psi")

print("\n2. Módulo de Resiliencia (U_r):")
print(f"   Representa la energía absorbida por unidad de volumen hasta el límite proporcional.")
print(f"   Límite Proporcional: σ_pl = {sigma_pl} ksi, ε_pl = {epsilon_pl} in/in")
print(f"   Fórmula: U_r = 0.5 * σ_pl * ε_pl")
print(f"   U_r = 0.5 * {sigma_pl} ksi * {epsilon_pl} in/in")
# Muestra el resultado en ksi y en psi (lb*in/in^3)
print(f"   U_r ≈ {modulo_resiliencia_Ur_ksi:.6f} ksi")
print(f"   U_r ≈ {modulo_resiliencia_Ur_ksi * 1000:.4f} psi  (o lb·in/in³)")
# print(f"   (Verificación con U_r = σ_pl² / (2E): {modulo_resiliencia_Ur_alt:.6f} ksi)") # Descomentar para ver verificación

print("\n--- Resultado para Problema 3-3 ---")
print("3. Módulo de Tenacidad (U_t) Aproximado:")
print(f"   Representa la energía total absorbida por unidad de volumen hasta la fractura.")
print(f"   Se calcula como el área total bajo la curva (integral aproximada con regla del trapecio).")
print(f"   Fractura en: ε_f = {deformacion_in_in[-1]} in/in, σ_f = {esfuerzo_ksi[-1]} ksi")
# Muestra el resultado en ksi y en psi (lb*in/in^3)
print(f"   U_t ≈ {modulo_tenacidad_Ut_ksi:.4f} ksi")
print(f"   U_t ≈ {modulo_tenacidad_Ut_ksi * 1000:.2f} psi  (o lb·in/in³)")