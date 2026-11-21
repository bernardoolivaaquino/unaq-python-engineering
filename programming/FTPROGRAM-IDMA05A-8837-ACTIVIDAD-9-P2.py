class Estudiante:
    # Método constructor que se ejecuta al crear un objeto
    def __init__(self, nombre, matricula):
        self.nombre = nombre
        self.matricula = matricula

    # Método que imprime los datos del estudiante
    def mostrar_informacion(self):
        print(f"Nombre: {self.nombre}")
        print(f"Matrícula: {self.matricula}")

# Se crea un objeto llamado est1
est1 = Estudiante("Bernardo", "8837")

# Se llama al método mostrar_informacion()
est1.mostrar_informacion()
