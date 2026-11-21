# --- EJERCICIO 1: Inventario de almacén (Mutabilidad) ---
# Objetivo: Demostrar que las listas en Python se pasan por referencia.
def agregar_pieza(lista_inventario, pieza):
    """Agrega una pieza directamente a la lista original."""
    lista_inventario.append(pieza)
    print(f"[Dentro de función] Lista modificada: {lista_inventario}")
# Programa Principal
mi_almacen = ["Tornillo", "Tuerca"]
print(f"Inventario inicial: {mi_almacen}")
nueva_pieza = "Arandela"
agregar_pieza(mi_almacen, nueva_pieza)
print(f"Inventario final (fuera): {mi_almacen}\n")

# --- EJERCICIO 2: Simulation sin modificar datos (Copia de listas) ---
def simular_incremento(mediciones):
    #Retorna una nueva lista con valores +10% sin tocar la original.
    nueva_lista = [(valor * 1.10, 2) for valor in mediciones]
    return nueva_lista

# Programa Principal
datos_originales = [100.0, 150.5, 200.0]
print(f"Mediciones originales: {datos_originales}")
datos_simulados = simular_incremento(datos_originales)
print(f"Simulación (+10%): {datos_simulados}")
print(f"Verificación (Original sigue igual): {datos_originales}\n")


# --- EJERCICIO 3: Registro de vuelo (Tipos de argumentos) ---
def registrar_vuelo(numero_vuelo, destino, origen="CDMX", aerolinea="Aeroméxico"):
    print(f"Vuelo {numero_vuelo} de {aerolinea}: {origen} -> {destino}")

# Programa Principal Ejercicio 3
print("Registros de vuelo:")
registrar_vuelo("AM123", "Madrid")
registrar_vuelo(destino="París", numero_vuelo="AF456", aerolinea="Air France", origen="Cancún")