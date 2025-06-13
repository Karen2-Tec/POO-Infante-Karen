"""
Programa para calcular el promedio semanal de temperaturas usando programación tradicional

Este enfoque utiliza funciones independientes que operan sobre datos pasados como parámetros.
La lógica está organizada en funciones específicas para cada tarea.
"""


def ingresar_temperaturas():
    """Solicita al usuario las temperaturas para cada día de la semana"""
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    temperaturas = []

    for dia in dias_semana:
        while True:
            try:
                temp = float(input(f"Ingrese la temperatura para {dia}: "))
                temperaturas.append(temp)
                break
            except ValueError:
                print("Error: Debe ingresar un número válido.")

    return temperaturas


def calcular_promedio(temps):
    """Calcula el promedio de una lista de temperaturas"""
    return sum(temps) / len(temps)


def mostrar_resultado(promedio):
    """Muestra el resultado formateado al usuario"""
    print(f"\nEl promedio semanal de temperatura es: {promedio:.2f}°C")


def main():
    """Función principal que orquesta el flujo del programa"""
    print("=== CALCULADORA DE PROMEDIO SEMANAL DE TEMPERATURAS ===")
    print("Por favor ingrese las temperaturas para cada día de la semana:\n")

    temps = ingresar_temperaturas()
    promedio = calcular_promedio(temps)
    mostrar_resultado(promedio)


if __name__ == "__main__":
    main()