#POo
#Ejemplo 1 clases simples y creación de objetos
class Persona:
    def __init__(self, nombre, edad): #Constructor "Self" es el objeto que se esta creando
        self.nombre = nombre #Guarda nombre
        self.edad = edad #Guarda edad
    def saludar (self): #Este es un método (Una Función dentro de una clase)
        print (f"Hola soy {self.nombre} y tengo {self.edad} años")
#Crear un objeto
p1 = Persona("Bernardo", 25) #crear una instacia (objeto de la clase)
#usarmetodo
p1.saludar()
 
 
#Ejemplo 2
class Perro:
    def ladar(self):
        print("¡Guau, guau!")
#Crear objeto
mi_perro = Perro()
mi_perro.ladar()
 
 
#Ejemplo con atributos cy métodos
class Perro:
    def __init__(self, nombre, raza):
        self.nombre = nombre
        self.raza = raza
 
    def ladrar(self):
        print(f"{self.nombre} dice ¡Guau guau!")
 
#Creación de objetos
perro1 = Perro("Firulais", "Labrador")
perro2 =Perro("Max", "Beagle")
 
perro1.ladrar()
perro2.ladrar()

#Ejemplo de Encapsulamiento
class CuentaBancaria:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.__saldo = saldo #Atributo privado
 
    def depositar(self, cantidad):
        self.__saldo += cantidad
 
    def retirar(self, cantidad):
        if cantidad <= self.__saldo:
            self.__saldo -= cantidad
        else:
            print("Fondos insuficientes")
 
    def mostrar_saldo(self):
        print(f"Saldo actual de {self.titular}: ${self.__saldo}")
 
cuenta =CuentaBancaria("Bernardo", 1000)
cuenta.depositar(500)
cuenta. mostrar_saldo()
cuenta.retirar(200)
cuenta.mostrar_saldo()
 
 
#Ejemplo de abstracción y modularidad
class Motor:
    def encender(self):
        print("El motor está encendido. ")
 
class Auto:
    def __init__(self, marca):
        self.marca = marca
        self.motor = Motor()
 
    def arrancar (self):
        print(f"Arrancando el auto {self.marca}...")
        self.motor.encender()
 
mi_auto = Auto("Volkswagen")
mi_auto.arrancar()


