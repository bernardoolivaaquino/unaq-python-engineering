import random
import os

# 1. FUNCIONES DE UTILIDAD E INTERFAZ

def limpiar_pantalla():
    """Limpia la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_bienvenida():
    print("==================================================")
    print("     ESCAPE ROOM UNAQ: MISIÓN CÓDIGO SECRETO      ")
    print("==================================================")

def solicitar_datos_jugador():
    #DIFICULTAD
    nombre = input("Ingresa tu nombre de agente: ")
    while True:
        print("\nSelecciona tu nivel de dificultad:")
        print("1. Fácil (15 intentos)")
        print("2. Medio (10 intentos)")
        print("3. Difícil (5 intentos)")
        dif = input("> ")
        if dif in ['1', '2', '3']:
            return nombre, int(dif)
        print("Error: Ingresa 1, 2 o 3.")

def mostrar_mision():
    # El lore
    print("\n--- MISIÓN INICIAL ---")
    print("Estás atrapado en el laboratorio de aerodinámica de la UNAQ.")
    print("El sistema ha iniciado una secuencia de bloqueo. Debes explorar")
    print("la habitación (matriz 3x3), encontrar pistas, resolver acertijos")
    print("y deducir el código de 4 dígitos para abrir la puerta principal.")
    print("Si te quedas sin intentos, quedarás encerrado para siempre.")
    pausar()

def mostrar_menu_principal():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Explorar habitación")
    print("2. Revisar inventario")
    print("3. Resolver acertijo")
    print("4. Intentar abrir puerta")
    print("5. Ver pistas disponibles")
    print("6. Salir del juego")

def pausar():
    #Detiene la ejecución hasta que el usuario decida continuar.
    input("\nPresiona Enter para continuar...")

def validar_coordenada(entrada):
    #Valida que la entrada del usuario sea un número entre 0 y 2.
    try:
        val = int(entrada)
        if 0 <= val <= 2:
            return True, val
        return False, -1
    except ValueError:
        return False, -1


# 2. FUNCIONES DE LÓGICA Y RECURSIVIDAD

def generar_acertijo_matematico():
    #Genera un acertijo usando aleatoriedad (Requisito Obligatorio)
    a = random.randint(10, 50)
    b = random.randint(1, 10)
    operaciones = [('+', a + b), ('-', a - b), ('*', a * b)]
    op, respuesta = random.choice(operaciones)
    pregunta = f"¿Cuánto es {a} {op} {b}?"
    return pregunta, respuesta

def verificar_acertijo(respuesta_usuario, respuesta_correcta):
    #Verifica si la respuesta al acertijo es correcta validando el tipo de dato.
    try:
        return int(respuesta_usuario) == respuesta_correcta
    except ValueError:
        return False

def verificar_codigo_recursivo(codigo_real, intento, indice=0):
    #FUNCIÓN RECURSIVA 
    # Caso base 1: Hemos revisado todos los caracteres con éxito
    if indice == len(codigo_real):
        return True
    
    # Caso base 2: Encontramos una discrepancia
    if codigo_real[indice] != intento[indice]:
        return False
        
    # Paso recursivo: Llamada a la misma función evaluando el siguiente índice
    return verificar_codigo_recursivo(codigo_real, intento, indice + 1)

# 3. PROGRAMACIÓN ORIENTADA A OBJETOS
#Primera Clase
class Jugador:

    def __init__(self, nombre, dificultad):
        self.nombre = nombre
        self.inventario = [] # LISTA
        self.pistas_restantes = 2
        
        if dificultad == 1: self.intentos = 15
        elif dificultad == 2: self.intentos = 10
        else: self.intentos = 5

    def mostrar_estado(self):
        print(f"\nAgente: {self.nombre} | Intentos restantes: {self.intentos} | Pistas: {self.pistas_restantes}")

    def agregar_al_inventario(self, objeto):
        if objeto not in self.inventario:
            self.inventario.append(objeto)
            print(f"¡Has añadido '{objeto}' a tu inventario!")
        else:
            print("Ya tienes este objeto.")

    def mostrar_inventario(self):
        print("\n--- INVENTARIO ---")
        if not self.inventario:
            print("Tu mochila está vacía.")
        else:
            for i, item in enumerate(self.inventario):
                print(f"{i+1}. {item}")
#Clase 2
class Habitacion:
    def __init__(self):
        # MATRIZ 
        self.mapa = [
            ["[?]", "[?]", "[?]"],
            ["[?]", "[?]", "[?]"],
            ["[?]", "[?]", "[?]"]
        ]
        # Aleatoriedad en la generación del código y ubicación de la llave
        self.codigo_secreto = str(random.randint(1000, 9999))
        self.fila_llave = random.randint(0, 2)
        self.col_llave = random.randint(0, 2)

    def imprimir_mapa(self):
        print("\n--- MAPA DE LA HABITACIÓN ---")
        for fila in self.mapa:
            print(" ".join(fila))
        print("Coordenadas: 0 a 2 para filas y columnas.")

    def explorar(self, fila, col, jugador):
        """Lógica de exploración de la matriz."""
        if self.mapa[fila][col] != "[?]":
            print("Ya exploraste esta zona. No hay nada nuevo.")
            return

        print(f"Buscando en las coordenadas ({fila}, {col})...")
        if fila == self.fila_llave and col == self.col_llave:
            print("¡Bingo! Encontraste un fragmento de papel rasgado.")
            jugador.agregar_al_inventario(f"Papel con los primeros 2 dígitos: {self.codigo_secreto[:2]}")
            self.mapa[fila][col] = "[P]" # P de Pista
        else:
            print("Solo encuentras polvo y cables viejos.")
            self.mapa[fila][col] = "[X]" # X de Vacío

# 4. CONTROLADORES DE MENÚ Y EJECUCIÓN

def opcion_explorar(jugador, habitacion):
    habitacion.imprimir_mapa()
    f_str = input("Ingresa la fila a explorar (0-2): ")
    c_str = input("Ingresa la columna a explorar (0-2): ")
    
    valida_f, f = validar_coordenada(f_str)
    valida_c, c = validar_coordenada(c_str)
    
    if valida_f and valida_c:
        habitacion.explorar(f, c, jugador)
        jugador.intentos -= 1
    else:
        print("Coordenadas inválidas. Has perdido tiempo valioso.")
        jugador.intentos -= 1

def opcion_acertijo(jugador, habitacion):
    pregunta, correcta = generar_acertijo_matematico()
    print(f"\nTerminal de seguridad: {pregunta}")
    respuesta = input("Respuesta: ")
    
    if verificar_acertijo(respuesta, correcta):
        print("Acceso parcial concedido.")
        jugador.agregar_al_inventario(f"Dígito final del código: {self.codigo_secreto[3]}")
    else:
        print("Respuesta incorrecta. El sistema te penaliza.")
        jugador.intentos -= 1

def opcion_abrir_puerta(jugador, habitacion):
    print("\nEl panel de la puerta requiere un código de 4 dígitos.")
    intento = input("Ingresa el código: ")
    
    if len(intento) == 4 and intento.isdigit():
        print("Verificando integridad del código...")
        # Llama a la función recursiva
        if verificar_codigo_recursivo(habitacion.codigo_secreto, intento):
            return True
        else:
            print("CÓDIGO INCORRECTO. Suena una alarma.")
            jugador.intentos -= 1
            return False
    else:
        print("Formato de código inválido. Deben ser 4 números.")
        jugador.intentos -= 1
        return False

def opcion_pistas(jugador):
    if jugador.pistas_restantes > 0:
        print("\nRecuerdas tu entrenamiento...")
        print("Deberías explorar el mapa para encontrar la primera mitad del código,")
        print("y resolver acertijos para obtener la parte final.")
        jugador.pistas_restantes -= 1
    else:
        print("\nYa no te quedan pistas. Estás por tu cuenta.")

def ejecutar_juego():
    limpiar_pantalla()
    mostrar_bienvenida()
    
    nombre, dificultad = solicitar_datos_jugador()
    jugador = Jugador(nombre, dificultad)
    habitacion = Habitacion()
    
    limpiar_pantalla()
    mostrar_mision()
    
    juego_activo = True
    escapo = False
    
    # Bucle principal del juego
    while juego_activo and jugador.intentos > 0:
        limpiar_pantalla()
        jugador.mostrar_estado()
        mostrar_menu_principal()
        
        opcion = input("\n¿Qué deseas hacer, agente? > ")
        
        if opcion == '1':
            opcion_explorar(jugador, habitacion)
            pausar()
        elif opcion == '2':
            jugador.mostrar_inventario()
            pausar()
        elif opcion == '3':
            pregunta, correcta = generar_acertijo_matematico()
            print(f"\nTerminal de seguridad: {pregunta}")
            respuesta = input("Respuesta: ")
            
            if verificar_acertijo(respuesta, correcta):
                print("Acceso parcial concedido.")
                jugador.agregar_al_inventario(f"Dígitos finales del código: {habitacion.codigo_secreto[2:]}")
            else:
                print("Respuesta incorrecta. El sistema te penaliza.")
                jugador.intentos -= 1
            pausar()
            
        elif opcion == '4':
            escapo = opcion_abrir_puerta(jugador, habitacion)
            if escapo:
                juego_activo = False
            pausar()
        elif opcion == '5':
            opcion_pistas(jugador)
            pausar()
        elif opcion == '6':
            print("\nTe has rendido. El sistema sella la puerta permanentemente.")
            juego_activo = False
            pausar()
        else:
            print("\nComando no reconocido.")
            pausar()
            
    # Resolución final
    limpiar_pantalla()
    if escapo:
        print(f"¡FELICIDADES {jugador.nombre.upper()}! HAS ESCAPADO.")
        print("La puerta se abre y logras salir del laboratorio.")
    else:
        print("MISIÓN FALLIDA.")
        print("Te has quedado sin intentos. Te van a aerodinamizar.")
        print(f"El código era: {habitacion.codigo_secreto}")

if __name__ == "__main__":
    ejecutar_juego()