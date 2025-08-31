import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any


class Producto:
    """
    Clase que representa un producto en el inventario.
    Utiliza propiedades para encapsular los atributos y validar los datos.
    """

    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        """
        Constructor de la clase Producto.
        """
        self._id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self._fecha_actualizacion = datetime.now().isoformat()

    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacio")
        self._nombre = valor.strip()
        self._actualizar_fecha()

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int):
        if valor < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self._cantidad = valor
        self._actualizar_fecha()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = valor
        self._actualizar_fecha()

    def _actualizar_fecha(self):
        self._fecha_actualizacion = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self._id,
            'nombre': self._nombre,
            'cantidad': self._cantidad,
            'precio': self._precio,
            'fecha_actualizacion': self._fecha_actualizacion
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Producto':
        return cls(
            data['id'],
            data['nombre'],
            data['cantidad'],
            data['price']
        )

    def __str__(self) -> str:
        return (f"ID: {self._id:04d} | {self._nombre:20} | "
                f"Cant: {self._cantidad:3d} | Precio: ${self._precio:8.2f}")


class Inventario:
    """
    Clase que gestiona el inventario utilizando un diccionario.
    """

    def __init__(self, archivo: str = "inventario_avanzado.json"):
        self._productos_por_id: Dict[int, Producto] = {}
        self._archivo = archivo
        self._cargar_desde_archivo()

    def _cargar_desde_archivo(self) -> None:
        try:
            if os.path.exists(self._archivo):
                with open(self._archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)

                for producto_data in datos:
                    try:
                        producto = Producto(
                            producto_data['id'],
                            producto_data['nombre'],
                            producto_data['cantidad'],
                            producto_data['precio']
                        )
                        self._productos_por_id[producto.id] = producto
                    except (ValueError, KeyError) as e:
                        print(f"Error al cargar producto: {e}")

                print(f"Inventario cargado desde {self._archivo}")

        except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
            print(f"Error al cargar archivo: {e}")

    def _guardar_en_archivo(self) -> bool:
        try:
            datos = [producto.to_dict() for producto in self._productos_por_id.values()]
            with open(self._archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2)
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    def agregar_producto(self, producto: Producto) -> bool:
        if producto.id in self._productos_por_id:
            print(f"Ya existe un producto con ID {producto.id}")
            return False

        self._productos_por_id[producto.id] = producto
        return self._guardar_en_archivo()

    def eliminar_producto(self, id_producto: int) -> bool:
        if id_producto not in self._productos_por_id:
            print(f"No se encontro producto con ID {id_producto}")
            return False

        del self._productos_por_id[id_producto]
        return self._guardar_en_archivo()

    def actualizar_producto(self, id_producto: int, **kwargs: Any) -> bool:
        producto = self._productos_por_id.get(id_producto)
        if not producto:
            print(f"No se encontro producto con ID {id_producto}")
            return False

        try:
            if 'nombre' in kwargs:
                producto.nombre = kwargs['nombre']
            if 'cantidad' in kwargs:
                producto.cantidad = kwargs['cantidad']
            if 'precio' in kwargs:
                producto.precio = kwargs['precio']

            return self._guardar_en_archivo()
        except ValueError as e:
            print(f"Error de validacion: {e}")
            return False

    def buscar_por_id(self, id_producto: int) -> Optional[Producto]:
        return self._productos_por_id.get(id_producto)

    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        resultados = []
        nombre_busqueda = nombre.lower().strip()
        for producto in self._productos_por_id.values():
            if nombre_busqueda in producto.nombre.lower():
                resultados.append(producto)
        return resultados

    def obtener_todos_productos(self) -> List[Producto]:
        return list(self._productos_por_id.values())


class SistemaInventario:
    """
    Clase principal del sistema con manejo robusto de inputs.
    """

    def __init__(self):
        self.inventario = Inventario()

    @staticmethod
    def mostrar_menu_principal():
        print("\n" + "=" * 50)
        print("SISTEMA DE GESTION DE INVENTARIO")
        print("=" * 50)
        print("1. Anadir nuevo producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por ID")
        print("5. Buscar producto por nombre")
        print("6. Mostrar todos los productos")
        print("7. Salir")
        print("=" * 50)

    @staticmethod
    def _leer_entero(mensaje: str) -> int:
        """Lee un numero entero con validacion."""
        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print("Error: Debe ingresar un numero entero valido.")

    @staticmethod
    def _leer_decimal(mensaje: str) -> float:
        """Lee un numero decimal con validacion."""
        while True:
            try:
                return float(input(mensaje))
            except ValueError:
                print("Error: Debe ingresar un numero decimal valido.")

    @staticmethod
    def _leer_texto(mensaje: str) -> str:
        """Lee texto con validacion de no vacio."""
        while True:
            texto = input(mensaje).strip()
            if texto:
                return texto
            print("Error: Este campo no puede estar vacio.")

    def ejecutar(self):
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione una opcion: ").strip()

            if opcion == "1":
                self._agregar_producto()
            elif opcion == "2":
                self._eliminar_producto()
            elif opcion == "3":
                self._actualizar_producto()
            elif opcion == "4":
                self._buscar_por_id()
            elif opcion == "5":
                self._buscar_por_nombre()
            elif opcion == "6":
                self._mostrar_todos()
            elif opcion == "7":
                print("Saliendo del sistema...")
                break
            else:
                print("Opcion no valida. Intente nuevamente.")

    def _agregar_producto(self):
        print("\n--- Anadir Nuevo Producto ---")
        try:
            id_producto = self._leer_entero("ID del producto: ")
            nombre = self._leer_texto("Nombre: ")
            cantidad = self._leer_entero("Cantidad: ")
            precio = self._leer_decimal("Precio: ")

            producto = Producto(id_producto, nombre, cantidad, precio)
            if self.inventario.agregar_producto(producto):
                print("Producto agregado exitosamente!")

        except Exception as e:
            print(f"Error: {e}")

    def _eliminar_producto(self):
        print("\n--- Eliminar Producto ---")
        id_producto = self._leer_entero("ID del producto a eliminar: ")
        if self.inventario.eliminar_producto(id_producto):
            print("Producto eliminado exitosamente!")

    def _actualizar_producto(self):
        print("\n--- Actualizar Producto ---")
        id_producto = self._leer_entero("ID del producto a actualizar: ")

        producto = self.inventario.buscar_por_id(id_producto)
        if not producto:
            print("Producto no encontrado.")
            return

        print(f"Producto actual: {producto}")
        print("Deje en blanco los campos que no desea modificar")

        nombre = input("Nuevo nombre: ").strip()
        nombre = nombre if nombre else None

        cantidad_str = input("Nueva cantidad: ").strip()
        cantidad = int(cantidad_str) if cantidad_str else None

        precio_str = input("Nuevo precio: ").strip()
        precio = float(precio_str) if precio_str else None

        if self.inventario.actualizar_producto(
                id_producto, nombre=nombre, cantidad=cantidad, precio=precio
        ):
            print("Producto actualizado exitosamente!")

    def _buscar_por_id(self):
        print("\n--- Buscar Producto por ID ---")
        id_producto = self._leer_entero("ID del producto a buscar: ")
        producto = self.inventario.buscar_por_id(id_producto)

        if producto:
            print("\nProducto encontrado:")
            print(producto)
        else:
            print("No se encontro el producto.")

    def _buscar_por_nombre(self):
        print("\n--- Buscar Producto por Nombre ---")
        nombre = input("Nombre a buscar: ").strip()

        if not nombre:
            print("Debe ingresar un nombre para buscar.")
            return

        resultados = self.inventario.buscar_por_nombre(nombre)

        if resultados:
            print(f"\nSe encontraron {len(resultados)} productos:")
            for producto in resultados:
                print(producto)
        else:
            print("No se encontraron productos.")

    def _mostrar_todos(self):
        print("\n--- Todos los Productos ---")
        productos = self.inventario.obtener_todos_productos()

        if productos:
            for producto in productos:
                print(producto)
            print(f"\nTotal: {len(productos)} productos")
        else:
            print("El inventario esta vacio.")


def main():
    sistema = SistemaInventario()
    sistema.ejecutar()


if __name__ == "__main__":
    main()