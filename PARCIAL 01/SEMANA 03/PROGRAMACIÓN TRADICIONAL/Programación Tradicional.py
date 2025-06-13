def ingresar_temperaturas():
    """Función para ingresar las temperaturas de la semana"""
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    temperaturas = []
    
    for dia in dias_semana:
        while True:
            try:
                temp = float(input(f"Ingrese la temperatura para {dia}: "))
                temperaturas.append(temp)
                break
            except ValueError:
                print("Por favor ingrese un número válido.")
    
    return temperaturas

def calcular_promedio(temps):
    """Función para calcular el promedio de temperaturas"""
    return sum(temps) / len(temps)

def mostrar_resultado(promedio):
    """Función para mostrar el resultado"""
    print(f"\nEl promedio semanal de temperatura es: {promedio:.2f}°C")

def main():
    """Función principal del programa tradicional"""
    print("=== Programa para calcular el promedio semanal de temperatura ===")
    temperaturas = ingresar_temperaturas()
    promedio = calcular_promedio(temperaturas)
    mostrar_resultado(promedio)

if __name__ == "__main__":
    main()