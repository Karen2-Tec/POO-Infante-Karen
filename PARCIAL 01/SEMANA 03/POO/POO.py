"""
Programa para calcular el promedio semanal de temperaturas usando POO

Este enfoque utiliza clases para encapsular los datos y comportamientos relacionados.
Se aplican principios de encapsulamiento y organización lógica de objetos.
"""

class DiaClima:
    """Representa un día de la semana con su temperatura correspondiente"""
    
    def __init__(self, nombre):
        """Inicializa un día con nombre y temperatura sin definir"""
        self.nombre = nombre
        self.temperatura = None
    
    def registrar_temperatura(self):
        """Solicita al usuario la temperatura para este día"""
        while True:
            try:
                temp = float(input(f"Ingrese la temperatura para {self.nombre}: "))
                self.temperatura = temp
                break
            except ValueError:
                print("Error: Debe ingresar un número válido.")

class SemanaClima:
    """Representa una semana completa de registros climáticos"""
    
    def __init__(self):
        """Inicializa la semana con los 7 días"""
        self.dias = [
            DiaClima("Lunes"),
            DiaClima("Martes"),
            DiaClima("Miércoles"),
            DiaClima("Jueves"),
            DiaClima("Viernes"),
            DiaClima("Sábado"),
            DiaClima("Domingo")
        ]
    
    def registrar_temperaturas(self):
        """Registra temperaturas para todos los días de la semana"""
        print("\nPor favor ingrese las temperaturas para cada día:")
        for dia in self.dias:
            dia.registrar_temperatura()
    
    def calcular_promedio(self):
        """Calcula el promedio de temperaturas de la semana"""
        temps_validas = [dia.temperatura for dia in self.dias if dia.temperatura is not None]
        return sum(temps_validas) / len(temps_validas)
    
    def mostrar_resumen(self):
        """Muestra el resumen climático semanal"""
        print("\n=== RESUMEN SEMANAL ===")
        for dia in self.dias:
            print(f"{dia.nombre}: {dia.temperatura}°C")
        
        promedio = self.calcular_promedio()
        print(f"\nPromedio semanal: {promedio:.2f}°C")

def main():
    """Función principal que crea y utiliza los objetos"""
    print("=== CALCULADORA DE CLIMA SEMANAL (POO) ===")
    
    semana_actual = SemanaClima()
    semana_actual.registrar_temperaturas()
    semana_actual.mostrar_resumen()

if __name__ == "__main__":
    main()