import json
import os


class Producto:
    """
    Clase que representa un producto en el inventario.

    Atributos:
        id_producto (int): Identificador único del producto
        nombre (str): Nombre del producto
        cantidad (int): Cantidad disponible en inventario
        precio (float): Precio unitario del producto
    """

    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        """
        Constructor de la clase Producto.

        Args:
            id_producto: Identificador único
            nombre: Nombre del producto
            cantidad: Cantidad inicial
            precio: Precio unitario
        """
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # Getters
    @property
    def id(self) -> int:
        """Devuelve el ID del producto"""
        return self._id

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del producto"""
        return self._nombre

    @property
    def cantidad(self) -> int:
        """Devuelve la cantidad disponible"""
        return self._cantidad

    @property
    def precio(self) -> float:
        """Devuelve el precio unitario"""
        return self._precio

    # Setters
    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        """Establece un nuevo nombre para el producto"""
        self._nombre = nuevo_nombre

    @cantidad.setter
    def cantidad(self, nueva_cantidad: int):
        """Establece una nueva cantidad para el producto"""
        if nueva_cantidad >= 0:
            self._cantidad = nueva_cantidad
        else:
            raise ValueError("La cantidad no puede ser negativa")

    @precio.setter
    def precio(self, nuevo_precio: float):
        """Establece un nuevo precio para el producto"""
        if nuevo_precio >= 0:
            self._precio = nuevo_precio
        else:
            raise ValueError("El precio no puede ser negativo")

    def to_dict(self) -> dict:
        """
        Convierte el producto a un diccionario para serialización.

        Returns:
            dict: Representación del producto como diccionario
        """
        return {
            'id': self._id,
            'nombre': self._nombre,
            'cantidad': self._cantidad,
            'precio': self._precio
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea un producto a partir de un diccionario.

        Args:
            data: Diccionario con los datos del producto

        Returns:
            Producto: Instancia de Producto
        """
        return cls(data['id'], data['nombre'], data['cantidad'], data['precio'])

    def __str__(self) -> str:
        """Representación en string del producto"""
        return f"ID: {self._id}, Nombre: {self._nombre}, Cantidad: {self._cantidad}, Precio: ${self._precio:.2f}"


class Inventario:
    """
    Clase que gestiona una colección de productos con persistencia en archivo.

    Atributos:
        productos (list): Lista de objetos Producto
        archivo (str): Ruta del archivo de persistencia
    """

    def __init__(self, archivo: str = "inventario.json"):
        """
        Inicializa un inventario y carga datos desde archivo si existe.

        Args:
            archivo: Ruta del archivo de persistencia
        """
        self._productos = []
        self._archivo = archivo
        self._cargar_desde_archivo()

    def _cargar_desde_archivo(self):
        """
        Carga los productos desde el archivo de persistencia.
        Si el archivo no existe, crea uno nuevo.
        """
        try:
            if os.path.exists(self._archivo):
                with open(self._archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self._productos = [Producto.from_dict(producto_data) for producto_data in datos]
                print(f"✓ Inventario cargado desde {self._archivo} ({len(self._productos)} productos)")
            else:
                print("ℹ Archivo de inventario no encontrado. Se creará uno nuevo al guardar.")

        except FileNotFoundError:
            print(f"✗ Error: El archivo {self._archivo} no fue encontrado.")
        except PermissionError:
            print(f"✗ Error: No tiene permisos para leer el archivo {self._archivo}.")
        except json.JSONDecodeError:
            print(f"✗ Error: El archivo {self._archivo} está corrupto o tiene formato incorrecto.")
            print("Se iniciará con un inventario vacío.")
        except Exception as e:
            print(f"✗ Error inesperado al cargar el inventario: {e}")

    def _guardar_en_archivo(self):
        """
        Guarda los productos en el archivo de persistencia.

        Returns:
            bool: True si se guardó exitosamente, False en caso de error
        """
        try:
            # Convertir productos a diccionarios
            datos = [producto.to_dict() for producto in self._productos]

            # Guardar en archivo
            with open(self._archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

            return True

        except PermissionError:
            print(f"✗ Error: No tiene permisos para escribir en el archivo {self._archivo}.")
            return False
        except Exception as e:
            print(f"✗ Error inesperado al guardar el inventario: {e}")
            return False

    def agregar_producto(self, producto: Producto):
        """
        Agrega un nuevo producto al inventario y guarda en archivo.

        Args:
            producto: Producto a agregar

        Raises:
            ValueError: Si el ID del producto ya existe
        """
        try:
            if self._buscar_por_id(producto.id) is not None:
                raise ValueError(f"Ya existe un producto con ID {producto.id}")

            self._productos.append(producto)

            if self._guardar_en_archivo():
                print("✓ Producto añadido y guardado exitosamente!")
            else:
                print("⚠ Producto añadido al inventario, pero hubo un error al guardar en archivo.")

        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Error inesperado al agregar producto: {e}")

    def eliminar_producto(self, id_producto: int):
        """
        Elimina un producto por su ID y guarda en archivo.

        Args:
            id_producto: ID del producto a eliminar

        Returns:
            bool: True si se eliminó y guardó exitosamente, False si no se encontró o hubo error
        """
        try:
            producto = self._buscar_por_id(id_producto)
            if producto:
                self._productos.remove(producto)

                if self._guardar_en_archivo():
                    print("✓ Producto eliminado y guardado exitosamente!")
                    return True
                else:
                    print("⚠ Producto eliminado del inventario, pero hubo un error al guardar en archivo.")
                    return False
            print("✗ No se encontró un producto con ese ID")
            return False

        except Exception as e:
            print(f"✗ Error inesperado al eliminar producto: {e}")
            return False

    def actualizar_producto(self, id_producto: int, nombre=None, cantidad=None, precio=None):
        """
        Actualiza los atributos de un producto y guarda en archivo.

        Args:
            id_producto: ID del producto a actualizar
            nombre: Nuevo nombre (opcional)
            cantidad: Nueva cantidad (opcional)
            precio: Nuevo precio (opcional)

        Returns:
            bool: True si se actualizó y guardó exitosamente, False si no se encontró o hubo error
        """
        try:
            producto = self._buscar_por_id(id_producto)
            if producto:
                cambios = []
                if nombre is not None:
                    producto.nombre = nombre
                    cambios.append("nombre")
                if cantidad is not None:
                    producto.cantidad = cantidad
                    cambios.append("cantidad")
                if precio is not None:
                    producto.precio = precio
                    cambios.append("precio")

                if cambios:
                    if self._guardar_en_archivo():
                        print(f"✓ Producto actualizado ({', '.join(cambios)}) y guardado exitosamente!")
                        return True
                    else:
                        print("⚠ Producto actualizado en inventario, pero hubo un error al guardar en archivo.")
                        return False
                else:
                    print("ℹ No se realizaron cambios en el producto.")
                    return True
            print("✗ No se encontró un producto con ese ID")
            return False

        except ValueError as e:
            print(f"✗ Error de validación: {e}")
            return False
        except Exception as e:
            print(f"✗ Error inesperado al actualizar producto: {e}")
            return False

    def buscar_por_nombre(self, nombre: str):
        """
        Busca productos por nombre (coincidencia parcial).

        Args:
            nombre: Cadena a buscar en los nombres de productos

        Returns:
            list: Lista de productos que coinciden
        """
        return [p for p in self._productos if nombre.lower() in p.nombre.lower()]

    def mostrar_todos(self):
        """Devuelve todos los productos del inventario"""
        return self._productos.copy()

    def _buscar_por_id(self, id_producto: int):
        """
        Método interno para buscar producto por ID.

        Args:
            id_producto: ID a buscar

        Returns:
            Producto: El producto encontrado o None
        """
        for producto in self._productos:
            if producto.id == id_producto:
                return producto
        return None

    def __str__(self):
        """Representación en string del inventario"""
        return "\n".join(str(p) for p in self._productos)


def mostrar_menu():
    """
    Muestra un menú interactivo para gestionar el inventario.
    """
    inventario = Inventario()

    while True:
        print("\n" + "=" * 50)
        print("       SISTEMA DE GESTIÓN DE INVENTARIOS")
        print("=" * 50)
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Información del sistema")
        print("7. Salir")
        print("=" * 50)

        try:
            opcion = input("Seleccione una opción (1-7): ").strip()

            if opcion == "1":
                print("\n--- Añadir nuevo producto ---")
                id_producto = int(input("ID del producto: "))
                nombre = input("Nombre: ").strip()
                if not nombre:
                    print("✗ El nombre no puede estar vacío")
                    continue
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))

                producto = Producto(id_producto, nombre, cantidad, precio)
                inventario.agregar_producto(producto)

            elif opcion == "2":
                print("\n--- Eliminar producto ---")
                id_producto = int(input("ID del producto a eliminar: "))
                inventario.eliminar_producto(id_producto)

            elif opcion == "3":
                print("\n--- Actualizar producto ---")
                id_producto = int(input("ID del producto a actualizar: "))

                print("Deje en blanco los campos que no desea modificar")
                nombre = input("Nuevo nombre: ").strip()
                nombre = None if nombre == "" else nombre

                cantidad_str = input("Nueva cantidad: ").strip()
                cantidad = None if cantidad_str == "" else int(cantidad_str)

                precio_str = input("Nuevo precio: ").strip()
                precio = None if precio_str == "" else float(precio_str)

                inventario.actualizar_producto(id_producto, nombre, cantidad, precio)

            elif opcion == "4":
                print("\n--- Buscar producto por nombre ---")
                nombre = input("Nombre o parte del nombre a buscar: ").strip()
                if not nombre:
                    print("✗ Debe ingresar un nombre para buscar")
                    continue

                resultados = inventario.buscar_por_nombre(nombre)

                if resultados:
                    print(f"\n✓ Se encontraron {len(resultados)} resultado(s):")
                    for i, producto in enumerate(resultados, 1):
                        print(f"{i}. {producto}")
                else:
                    print("✗ No se encontraron productos con ese nombre")

            elif opcion == "5":
                print("\n--- Todos los productos ---")
                productos = inventario.mostrar_todos()
                if productos:
                    print(f"✓ Total de productos: {len(productos)}")
                    for i, producto in enumerate(productos, 1):
                        print(f"{i}. {producto}")
                    print(f"Valor total del inventario: ${sum(p.cantidad * p.precio for p in productos):.2f}")
                else:
                    print("ℹ El inventario está vacío")

            elif opcion == "6":
                print("\n--- Información del sistema ---")
                productos = inventario.mostrar_todos()
                print(f"Archivo de inventario: {inventario._Inventario__archivo}")
                print(f"Productos cargados: {len(productos)}")
                print(f"Ubicación actual: {os.getcwd()}")
                print(
                    f"Tamaño del archivo: {os.path.getsize(inventario._Inventario__archivo) if os.path.exists(inventario._Inventario__archivo) else 0} bytes")

            elif opcion == "7":
                print("\n💾 Guardando inventario...")
                print("👋 Saliendo del sistema. ¡Hasta pronto!")
                break

            else:
                print("✗ Opción no válida. Por favor seleccione una opción del 1 al 7.")

        except ValueError:
            print("✗ Error: Por favor ingrese valores numéricos válidos para ID, cantidad y precio.")
        except KeyboardInterrupt:
            print("\n\n⚠ Operación cancelada por el usuario.")
            continuar = input("¿Desea salir del sistema? (s/n): ").lower().strip()
            if continuar == 's':
                print("👋 Saliendo del sistema...")
                break
        except Exception as e:
            print(f"✗ Error inesperado: {e}")


def main():
    """
    Función principal del sistema de gestión de inventarios.
    """
    print("🚀 Iniciando Sistema de Gestión de Inventarios...")
    print("📁 Los datos se guardarán automáticamente en 'inventario.json'")

    try:
        mostrar_menu()
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        print("El sistema se cerrará debido a un error inesperado.")
    finally:
        print("\n" + "=" * 50)
        print("Gracias por usar el Sistema de Gestión de Inventarios")
        print("=" * 50)


if __name__ == "__main__":
    main()