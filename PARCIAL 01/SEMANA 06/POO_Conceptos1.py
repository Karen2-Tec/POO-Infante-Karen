# Clase base que representa un Animal
class Animal:
    def __init__(self, nombre, edad):
        self._nombre = nombre  # Atributo encapsulado (convención con _)
        self._edad = edad      # Atributo encapsulado
    
    # Método getter para nombre (encapsulación)
    @property
    def nombre(self):
        return self._nombre
    
    # Método getter para edad (encapsulación)
    @property
    def edad(self):
        return self._edad
    
    def hacer_sonido(self):
        # Método que será sobrescrito por las clases derivadas (polimorfismo)
        return "Este animal hace un sonido"
    
    def moverse(self):
        # Método que puede ser sobrescrito
        return "Este animal se mueve"
    
    def __str__(self):
        return f"Animal: {self._nombre}, Edad: {self._edad}"


# Clase derivada que hereda de Animal (herencia)
class Perro(Animal):
    def __init__(self, nombre, edad, raza):
        super().__init__(nombre, edad)  # Llamada al constructor de la clase base
        self.__raza = raza              # Atributo privado (encapsulación fuerte)
    
    # Método getter para raza
    @property
    def raza(self):
        return self.__raza
    
    # Sobrescritura del método hacer_sonido (polimorfismo)
    def hacer_sonido(self):
        return "¡Guau guau!"
    
    # Método específico de Perro
    def buscar(self, objeto):
        return f"{self._nombre} está buscando {objeto}"
    
    def __str__(self):
        return f"Perro: {self._nombre}, Raza: {self.__raza}, Edad: {self._edad}"


# Otra clase derivada de Animal
class Pajaro(Animal):
    def __init__(self, nombre, edad, tipo):
        super().__init__(nombre, edad)
        self.__tipo = tipo  # Atributo privado
    
    @property
    def tipo(self):
        return self.__tipo
    
    # Sobrescritura del método hacer_sonido (polimorfismo)
    def hacer_sonido(self):
        return "¡Pío pío!"
    
    # Sobrescritura del método moverse
    def moverse(self):
        return "Este animal vuela"
    
    # Método específico de Pajaro
    def construir_nido(self):
        return f"{self._nombre} está construyendo un nido"
    
    def __str__(self):
        return f"Pájaro: {self._nombre}, Tipo: {self.__tipo}, Edad: {self._edad}"


# Función que demuestra polimorfismo
def describir_animal(animal):
    print(animal)
    print(animal.hacer_sonido())
    print(animal.moverse())
    print("-" * 30)


# Ejemplo de uso del programa
if __name__ == "__main__":
    # Creación de instancias
    animal_generico = Animal("Genérico", 3)
    perro = Perro("Fido", 5, "Labrador")
    pajaro = Pajaro("Piolín", 2, "Canario")
    
    # Demostración de encapsulación
    print(f"Nombre del perro (usando getter): {perro.nombre}")
    print(f"Edad del pájaro (usando getter): {pajaro.edad}")
    print(f"Raza del perro: {perro.raza}")
    print(f"Tipo de pájaro: {pajaro.tipo}")
    print("-" * 50)
    
    # Demostración de polimorfismo con la misma función
    describir_animal(animal_generico)
    describir_animal(perro)
    describir_animal(pajaro)
    
    # Llamada a métodos específicos
    print(perro.buscar("pelota"))
    print(pajaro.construir_nido())