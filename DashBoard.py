import os


def mostrar_codigo(ruta_script):
    """Muestra el contenido de un archivo con manejo de errores mejorado."""
    try:
        ruta_absoluta = os.path.abspath(ruta_script)
        print(f"\nBuscando archivo en: {ruta_absoluta}")  # Mensaje de diagnóstico

        if not os.path.exists(ruta_absoluta):
            raise FileNotFoundError(f"El archivo no existe en:\n{ruta_absoluta}")

        with open(ruta_absoluta, 'r', encoding='utf-8') as archivo:
            print(f"\n--- Código de {os.path.basename(ruta_script)} ---\n")
            print(archivo.read())

    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        print("Posibles soluciones:")
        print("1. Verifica que el archivo exista en la ubicación mostrada")
        print("2. Revisa mayúsculas/minúsculas en el nombre del archivo")
        print("3. Comprueba que tengas permisos de lectura")
    except Exception as e:
        print(f"\nError inesperado: {e}")


def mostrar_menu():
    """Muestra el menú principal con diagnóstico de rutas."""
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    print(f"\nDirectorio base del script: {ruta_base}")  # Diagnóstico

    opciones = {
        '1': os.path.join('PARCIAL 01', 'SEMANA 05', 'TipodDedatos.py'),
    }

    # Verificar existencia de archivos
    print("\nVerificación de archivos:")
    for key, ruta in opciones.items():
        ruta_completa = os.path.join(ruta_base, ruta)
        existe = "✓ EXISTE" if os.path.exists(ruta_completa) else "✗ NO EXISTE"
        print(f"Opción {key}: {ruta_completa} {existe}")

    while True:
        print("\n" + "=" * 40)
        print("Menu Principal - Dashboard".center(40))
        print("=" * 40)
        for key in opciones:
            print(f"{key} - {os.path.basename(opciones[key])}")
        print("0 - Salir")
        print("=" * 40)

        eleccion = input("\nElige una opción (0 para salir): ").strip()

        if eleccion == '0':
            print("Saliendo del programa...")
            break

        if eleccion in opciones:
            ruta_completa = os.path.join(ruta_base, opciones[eleccion])
            mostrar_codigo(ruta_completa)
        else:
            print("Opción no válida. Intenta nuevamente.")

        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    mostrar_menu()