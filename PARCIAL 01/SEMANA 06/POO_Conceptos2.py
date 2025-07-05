from abc import ABC, abstractmethod
import datetime

# Clase abstracta (encapsula el concepto general de empleado)
class Empleado(ABC):
    def __init__(self, nombre, apellido, id_empleado):
        self._nombre = nombre      # Atributo protegido
        self._apellido = apellido
        self.__id_empleado = id_empleado  # Atributo privado
        self._fecha_contratacion = datetime.date.today()
    
    # Propiedades (getters) para atributos encapsulados
    @property
    def nombre_completo(self):
        return f"{self._nombre} {self._apellido}"
    
    @property
    def id_empleado(self):
        return self.__id_empleado
    
    @property
    def antiguedad(self):
        return (datetime.date.today() - self._fecha_contratacion).days // 365
    
    # Método abstracto (obliga a las subclases a implementarlo)
    @abstractmethod
    def calcular_salario(self):
        pass
    
    # Método polimórfico que puede ser sobrescrito
    def mostrar_info(self):
        return (f"ID: {self.__id_empleado}, Nombre: {self.nombre_completo}, "
                f"Antigüedad: {self.antiguedad} años")
    
    # Método estático (no depende de la instancia)
    @staticmethod
    def es_dia_laboral(dia):
        if dia.weekday() >= 5:  # 5 y 6 son sábado y domingo
            return False
        return True

# Clase derivada para empleados a tiempo completo
class EmpleadoTiempoCompleto(Empleado):
    def __init__(self, nombre, apellido, id_empleado, salario_anual):
        super().__init__(nombre, apellido, id_empleado)
        self.__salario_anual = salario_anual
    
    # Implementación del método abstracto
    def calcular_salario(self):
        return self.__salario_anual / 12
    
    # Sobrescritura del método mostrar_info
    def mostrar_info(self):
        info_base = super().mostrar_info()
        return f"{info_base}, Tipo: Tiempo Completo, Salario mensual: ${self.calcular_salario():.2f}"
    
    # Método específico de esta clase
    def calcular_bono(self, porcentaje):
        return self.__salario_anual * porcentaje / 100

# Clase derivada para empleados por hora
class EmpleadoPorHora(Empleado):
    def __init__(self, nombre, apellido, id_empleado, horas_trabajadas, tarifa_hora):
        super().__init__(nombre, apellido, id_empleado)
        self.__horas_trabajadas = horas_trabajadas
        self.__tarifa_hora = tarifa_hora
    
    # Implementación del método abstracto
    def calcular_salario(self):
        return self.__horas_trabajadas * self.__tarifa_hora
    
    # Sobrescritura del método mostrar_info
    def mostrar_info(self):
        info_base = super().mostrar_info()
        return (f"{info_base}, Tipo: Por Hora, "
                f"Horas: {self.__horas_trabajadas}, Tarifa: ${self.__tarifa_hora}/h, "
                f"Salario: ${self.calcular_salario():.2f}")
    
    # Método específico de esta clase
    def actualizar_horas(self, nuevas_horas):
        self.__horas_trabajadas = nuevas_horas

# Función para demostrar polimorfismo
def procesar_empleados(empleados):
    total_nomina = 0
    print("\n--- Informe de Empleados ---")
    for emp in empleados:
        print(emp.mostrar_info())
        total_nomina += emp.calcular_salario()
    print(f"\nTotal nómina mensual: ${total_nomina:.2f}")
    print("-" * 50)

# Ejemplo de uso del sistema
if __name__ == "__main__":
    # Crear algunos empleados
    empleado1 = EmpleadoTiempoCompleto("Juan", "Pérez", "EMP-001", 60000)
    empleado2 = EmpleadoPorHora("María", "Gómez", "EMP-002", 120, 15)
    empleado3 = EmpleadoTiempoCompleto("Carlos", "López", "EMP-003", 75000)
    
    # Demostrar encapsulación
    print(f"Accediendo a propiedad nombre_completo: {empleado1.nombre_completo}")
    print(f"Accediendo a propiedad id_empleado: {empleado1.id_empleado}")
    print(f"Antigüedad de empleado1: {empleado1.antiguedad} años")
    
    # Demostrar método estático
    hoy = datetime.date.today()
    print(f"\n¿Es {hoy} día laboral? {Empleado.es_dia_laboral(hoy)}")
    
    # Demostrar polimorfismo
    lista_empleados = [empleado1, empleado2, empleado3]
    procesar_empleados(lista_empleados)
    
    # Usar métodos específicos de cada clase
    print(f"Bono del 10% para {empleado1.nombre_completo}: ${empleado1.calcular_bono(10):.2f}")
    
    empleado2.actualizar_horas(150)
    print("\nDespués de actualizar horas:")
    procesar_empleados([empleado2])