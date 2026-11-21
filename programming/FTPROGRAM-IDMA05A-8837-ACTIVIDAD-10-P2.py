# Definición de la clase
class Sensor:
    # Método constructor que inicializa los datos
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    # Método para simular la lectura del sensor
    def leer(self):
        print(f"Realizando lectura del sensor de {self.tipo}...")

    # Método para imprimir los datos del estado actual
    def mostrar_estado(self):
        print(f"Tipo de sensor: {self.tipo}")
        print(f"Valor registrado: {self.valor}")

# Creación de un objeto de prueba
mi_sensor = Sensor("Temperatura", 19.5)

# Llamada a los métodos
mi_sensor.leer()
mi_sensor.mostrar_estado()
