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

    def __str__(self) -> str:
        """Representación en string del producto"""
        return f"ID: {self._id}, Nombre: {self._nombre}, Cantidad: {self._cantidad}, Precio: ${self._precio:.2f}"