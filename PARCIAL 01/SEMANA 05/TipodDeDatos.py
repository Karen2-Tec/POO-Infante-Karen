"""
Calculadora de Índice de Masa Corporal (IMC)

Este programa calcula el IMC de una persona basado en su peso y altura,
y proporciona una clasificación según los estándares de salud.

Características:
- Utiliza diferentes tipos de datos (float, string, boolean)
- Sigue convenciones de nomenclatura snake_case
- Incluye validación de entrada de datos
"""

def calcular_imc(peso_kg: float, altura_m: float) -> float:
    """
    Calcula el Índice de Masa Corporal (IMC)
    
    Args:
        peso_kg: peso en kilogramos
        altura_m: altura en metros
    
    Returns:
        Valor del IMC redondeado a 2 decimales
    """
    if altura_m <= 0 or peso_kg <= 0:
        raise ValueError("El peso y la altura deben ser valores positivos.")
    
    imc = peso_kg / (altura_m ** 2)
    return round(imc, 2)


def clasificar_imc(imc: float) -> str:
    """
    Clasifica el IMC según los estándares de la OMS
    
    Args:
        imc: valor del índice de masa corporal
    
    Returns:
        Clasificación del estado de peso
    """
    if imc < 18.5:
        return "Bajo peso"
    elif 18.5 <= imc < 25:
        return "Peso normal"
    elif 25 <= imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"


def main():
    # Datos de entrada
    print("Calculadora de IMC")
    try:
        peso = float(input("Ingrese su peso en kilogramos: "))
        altura = float(input("Ingrese su altura en metros: "))
        
        # Calcular IMC
        imc_resultado = calcular_imc(peso, altura)
        
        # Clasificar IMC
        clasificacion = clasificar_imc(imc_resultado)
        
        # Mostrar resultados
        print(f"\nResultados:")
        print(f"IMC: {imc_resultado}")
        print(f"Clasificación: {clasificacion}")
        
        # Variable booleana para indicar si el peso es saludable
        peso_saludable = 18.5 <= imc_resultado < 25
        print(f"¿Peso saludable? {'Sí' if peso_saludable else 'No'}")
        
    except ValueError as e:
        print(f"Error: {e}. Por favor ingrese valores numéricos válidos.")


if __name__ == "__main__":
    main()