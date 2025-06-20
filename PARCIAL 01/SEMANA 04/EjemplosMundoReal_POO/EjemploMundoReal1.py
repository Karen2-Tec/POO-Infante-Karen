"""
Sistema de gestión para una clínica veterinaria que demuestra los principios de POO:
- Encapsulación
- Abstracción
- Herencia
- Polimorfismo
"""

class Mascota:
    """Clase base que representa una mascota en la veterinaria"""
    
    def __init__(self, nombre, especie, edad, peso):
        self._nombre = nombre  # Encapsulación: atributo protegido
        self._especie = especie
        self._edad = edad
        self._peso = peso
        self._vacunas = []
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        if len(nuevo_nombre) < 2:
            print("El nombre debe tener al menos 2 caracteres")
        else:
            self._nombre = nuevo_nombre
    
    def agregar_vacuna(self, vacuna):
        self._vacunas.append(vacuna)
        print(f"Vacuna {vacuna} registrada para {self._nombre}")
    
    def mostrar_info(self):
        """Método abstracto para mostrar información de la mascota"""
        info = f"""
        Nombre: {self._nombre}
        Especie: {self._especie}
        Edad: {self._edad} años
        Peso: {self._peso} kg
        Vacunas: {', '.join(self._vacunas) if self._vacunas else 'Ninguna'}
        """
        print(info)


class Perro(Mascota):
    """Clase que hereda de Mascota para representar un perro"""
    
    def __init__(self, nombre, edad, peso, raza):
        super().__init__(nombre, "Perro", edad, peso)
        self._raza = raza
        self._entrenado = False
    
    def entrenar(self):
        """Método específico para perros"""
        self._entrenado = True
        print(f"{self._nombre} ha sido entrenado!")
    
    def mostrar_info(self):  # Polimorfismo: sobrescribe el método de la clase base
        super().mostrar_info()
        print(f"Raza: {self._raza}")
        print(f"Entrenado: {'Sí' if self._entrenado else 'No'}")


class Gato(Mascota):
    """Clase que hereda de Mascota para representar un gato"""
    
    def __init__(self, nombre, edad, peso, color):
        super().__init__(nombre, "Gato", edad, peso)
        self._color = color
        self._caza_ratones = False
    
    def cazar_raton(self):
        """Método específico para gatos"""
        self._caza_ratones = True
        print(f"{self._nombre} ha cazado un ratón!")
    
    def mostrar_info(self):  # Polimorfismo: sobrescribe el método de la clase base
        super().mostrar_info()
        print(f"Color: {self._color}")
        print(f"Caza ratones: {'Sí' if self._caza_ratones else 'No'}")


class Dueño:
    """Clase que representa al dueño de una mascota"""
    
    def __init__(self, nombre, telefono, email):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.mascotas = []
    
    def agregar_mascota(self, mascota):
        """Agrega una mascota a la lista de mascotas del dueño"""
        self.mascotas.append(mascota)
        print(f"{mascota.nombre} ha sido registrado/a para {self.nombre}")
    
    def mostrar_mascotas(self):
        """Muestra todas las mascotas del dueño"""
        print(f"\nMascotas de {self.nombre}:")
        for mascota in self.mascotas:
            mascota.mostrar_info()


class CitaMedica:
    """Clase que representa una cita médica en la veterinaria"""
    
    def __init__(self, mascota, dueño, fecha, motivo):
        self.mascota = mascota
        self.dueño = dueño
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = None
        self.tratamiento = None
    
    def agregar_diagnostico(self, diagnostico):
        """Agrega un diagnóstico a la cita"""
        self.diagnostico = diagnostico
    
    def agregar_tratamiento(self, tratamiento):
        """Agrega un tratamiento a la cita"""
        self.tratamiento = tratamiento
    
    def mostrar_cita(self):
        """Muestra la información completa de la cita"""
        print("\n--- Información de la Cita ---")
        print(f"Fecha: {self.fecha}")
        print(f"Mascota: {self.mascota.nombre}")
        print(f"Dueño: {self.dueño.nombre}")
        print(f"Motivo: {self.motivo}")
        if self.diagnostico:
            print(f"Diagnóstico: {self.diagnostico}")
        if self.tratamiento:
            print(f"Tratamiento: {self.tratamiento}")


# Ejemplo de uso del sistema
if __name__ == "__main__":
    # Crear dueños
    dueño1 = Dueño("María López", "555-1234", "maria@email.com")
    dueño2 = Dueño("Carlos Ruiz", "555-5678", "carlos@email.com")
    
    # Crear mascotas
    perro1 = Perro("Max", 3, 12.5, "Labrador")
    gato1 = Gato("Luna", 2, 4.2, "Negro")
    perro2 = Perro("Bobby", 5, 8.7, "Chihuahua")
    
    # Asignar mascotas a dueños
    dueño1.agregar_mascota(perro1)
    dueño1.agregar_mascota(gato1)
    dueño2.agregar_mascota(perro2)
    
    # Agregar vacunas
    perro1.agregar_vacuna("Rabia")
    perro1.agregar_vacuna("Moquillo")
    gato1.agregar_vacuna("Leucemia felina")
    
    # Entrenar perro
    perro1.entrenar()
    
    # Hacer que el gato cace un ratón
    gato1.cazar_raton()
    
    # Mostrar información de mascotas
    dueño1.mostrar_mascotas()
    dueño2.mostrar_mascotas()
    
    # Crear una cita médica
    cita1 = CitaMedica(perro1, dueño1, "2023-05-15 10:00", "Revisión anual")
    cita1.agregar_diagnostico("Saludable")
    cita1.agregar_tratamiento("Vacuna refuerzo")
    cita1.mostrar_cita()