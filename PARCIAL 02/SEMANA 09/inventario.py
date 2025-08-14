from producto import Producto


class Inventario:
    """
    Clase que gestiona una colección de productos.

    Atributos:
        productos (list): Lista de objetos Producto
    """

    def __init__(self):
        """Inicializa un inventario vacío"""
        self._productos = []

    def agregar_producto(self, producto: Producto):
        """
        Agrega un nuevo producto al inventario.

        Args:
            producto: Producto a agregar

        Raises:
            ValueError: Si el ID del producto ya existe
        """
        if self._buscar_por_id(producto.id) is not None:
            raise ValueError(f"Ya existe un producto con ID {producto.id}")
        self._productos.append(producto)

    def eliminar_producto(self, id_producto: int):
        """
        Elimina un producto por su ID.

        Args:
            id_producto: ID del producto a eliminar

        Returns:
            bool: True si se eliminó, False si no se encontró
        """
        producto = self._buscar_por_id(id_producto)
        if producto:
            self._productos.remove(producto)
            return True
        return False

    def actualizar_producto(self, id_producto: int, nombre=None, cantidad=None, precio=None):
        """
        Actualiza los atributos de un producto.

        Args:
            id_producto: ID del producto a actualizar
            nombre: Nuevo nombre (opcional)
            cantidad: Nueva cantidad (opcional)
            precio: Nuevo precio (opcional)

        Returns:
            bool: True si se actualizó, False si no se encontró
        """
        producto = self._buscar_por_id(id_producto)
        if producto:
            if nombre is not None:
                producto.nombre = nombre
            if cantidad is not None:
                producto.cantidad = cantidad
            if precio is not None:
                producto.precio = precio
            return True
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
        print("\n--- Sistema de Gestión de Inventarios ---")
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                print("\n--- Añadir nuevo producto ---")
                id_producto = int(input("ID del producto: "))
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))

                producto = Producto(id_producto, nombre, cantidad, precio)
                inventario.agregar_producto(producto)
                print("Producto añadido con éxito!")

            elif opcion == "2":
                print("\n--- Eliminar producto ---")
                id_producto = int(input("ID del producto a eliminar: "))
                if inventario.eliminar_producto(id_producto):
                    print("Producto eliminado con éxito!")
                else:
                    print("No se encontró un producto con ese ID")

            elif opcion == "3":
                print("\n--- Actualizar producto ---")
                id_producto = int(input("ID del producto a actualizar: "))

                print("Deje en blanco los campos que no desea modificar")
                nombre = input("Nuevo nombre: ")
                nombre = None if nombre == "" else nombre

                cantidad_str = input("Nueva cantidad: ")
                cantidad = None if cantidad_str == "" else int(cantidad_str)

                precio_str = input("Nuevo precio: ")
                precio = None if precio_str == "" else float(precio_str)

                if inventario.actualizar_producto(id_producto, nombre, cantidad, precio):
                    print("Producto actualizado con éxito!")
                else:
                    print("No se encontró un producto con ese ID")

            elif opcion == "4":
                print("\n--- Buscar producto por nombre ---")
                nombre = input("Nombre o parte del nombre a buscar: ")
                resultados = inventario.buscar_por_nombre(nombre)

                if resultados:
                    print("\nResultados de la búsqueda:")
                    for producto in resultados:
                        print(producto)
                else:
                    print("No se encontraron productos con ese nombre")

            elif opcion == "5":
                print("\n--- Todos los productos ---")
                productos = inventario.mostrar_todos()
                if productos:
                    for producto in productos:
                        print(producto)
                else:
                    print("El inventario está vacío")

            elif opcion == "6":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción no válida. Intente nuevamente.")

        except ValueError as e:
            print(f"Error: {e}. Por favor ingrese datos válidos.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    mostrar_menu()