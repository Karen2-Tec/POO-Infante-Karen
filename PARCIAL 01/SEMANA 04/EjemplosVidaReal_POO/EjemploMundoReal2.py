"""
Sistema de Biblioteca - Ejemplo de POO

Este programa modela un sistema de biblioteca con libros, usuarios y préstamos.
"""

class Libro:
    """
    Clase que representa un libro en la biblioteca.
    
    Atributos:
        título (str): Título del libro
        autor (str): Autor del libro
        isbn (str): Identificador único del libro
        disponible (bool): Indica si el libro está disponible para préstamo
    """
    
    def __init__(self, titulo, autor, isbn):
        """
        Inicializa un nuevo libro con título, autor e ISBN.
        Por defecto, el libro está disponible al crearse.
        """
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = True
    
    def prestar(self):
        """
        Marca el libro como prestado si está disponible.
        Retorna True si el préstamo fue exitoso, False en caso contrario.
        """
        if self.disponible:
            self.disponible = False
            return True
        return False
    
    def devolver(self):
        """
        Marca el libro como disponible cuando es devuelto.
        """
        self.disponible = True
    
    def __str__(self):
        """
        Representación en string del libro.
        """
        estado = "Disponible" if self.disponible else "Prestado"
        return f"'{self.titulo}' por {self.autor} ({self.isbn}) - {estado}"


class Usuario:
    """
    Clase que representa un usuario de la biblioteca.
    
    Atributos:
        nombre (str): Nombre del usuario
        id_usuario (str): Identificador único del usuario
        libros_prestados (list): Lista de libros actualmente prestados
    """
    
    def __init__(self, nombre, id_usuario):
        """
        Inicializa un nuevo usuario con nombre e ID.
        """
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []
    
    def tomar_prestado(self, libro):
        """
        Intenta tomar prestado un libro.
        Retorna True si el préstamo fue exitoso, False en caso contrario.
        """
        if libro.prestar():
            self.libros_prestados.append(libro)
            return True
        return False
    
    def devolver_libro(self, libro):
        """
        Devuelve un libro a la biblioteca.
        Retorna True si la devolución fue exitosa, False en caso contrario.
        """
        if libro in self.libros_prestados:
            libro.devolver()
            self.libros_prestados.remove(libro)
            return True
        return False
    
    def __str__(self):
        """
        Representación en string del usuario.
        """
        return f"Usuario: {self.nombre} (ID: {self.id_usuario}) - Libros prestados: {len(self.libros_prestados)}"


class Biblioteca:
    """
    Clase que representa la biblioteca y gestiona libros y usuarios.
    
    Atributos:
        libros (dict): Diccionario de libros (clave: ISBN)
        usuarios (dict): Diccionario de usuarios (clave:ID de usuario)
    """
    
    def __init__(self):
        """
        Inicializa una biblioteca vacía.
        """
        self.libros = {}
        self.usuarios = {}
    
    def agregar_libro(self, libro):
        """
        Agrega un libro a la biblioteca.
        """
        self.libros[libro.isbn] = libro
    
    def registrar_usuario(self, usuario):
        """
        Registra un usuario en la biblioteca.
        """
        self.usuarios[usuario.id_usuario] = usuario
    
    def buscar_libro(self, isbn=None, titulo=None):
        """
        Busca un libro por ISBN o título.
        Retorna el libro si se encuentra, None en caso contrario.
        """
        if isbn and isbn in self.libros:
            return self.libros[isbn]
        
        if titulo:
            for libro in self.libros.values():
                if libro.titulo.lower() == titulo.lower():
                    return libro
        
        return None
    
    def prestar_libro(self, id_usuario, isbn_libro):
        """
        Gestiona el préstamo de un libro a un usuario.
        Retorna True si el préstamo fue exitoso, False en caso contrario.
        """
        usuario = self.usuarios.get(id_usuario)
        libro = self.libros.get(isbn_libro)
        
        if usuario and libro:
            return usuario.tomar_prestado(libro)
        return False
    
    def __str__(self):
        """
        Representación en string de la biblioteca.
        """
        return f"Biblioteca: {len(self.libros)} libros, {len(self.usuarios)} usuarios"


# Ejemplo de uso del sistema de biblioteca
if __name__ == "__main__":
    # Crear una biblioteca
    biblioteca = Biblioteca()
    
    # Agregar algunos libros
    libro1 = Libro("Cien años de soledad", "Gabriel García Márquez", "978-0307474728")
    libro2 = Libro("El Principito", "Antoine de Saint-Exupéry", "978-0156012195")
    libro3 = Libro("1984", "George Orwell", "978-0451524935")
    
    biblioteca.agregar_libro(libro1)
    biblioteca.agregar_libro(libro2)
    biblioteca.agregar_libro(libro3)
    
    # Registrar algunos usuarios
    usuario1 = Usuario("Juan Pérez", "JP001")
    usuario2 = Usuario("María Gómez", "MG002")
    
    biblioteca.registrar_usuario(usuario1)
    biblioteca.registrar_usuario(usuario2)
    
    print("\n=== Estado inicial de la biblioteca ===")
    print(biblioteca)
    print(libro1)
    print(libro2)
    print(libro3)
    
    # Realizar algunos préstamos
    print("\n=== Realizando préstamos ===")
    biblioteca.prestar_libro("JP001", "978-0307474728")  # Juan toma prestado Cien años de soledad
    biblioteca.prestar_libro("MG002", "978-0156012195")  # María toma prestado El Principito
    
    print("\n=== Estado después de préstamos ===")
    print(libro1)
    print(libro2)
    print(usuario1)
    print(usuario2)
    
    # Intentar prestar un libro ya prestado
    print("\n=== Intentando prestar libro ya prestado ===")
    resultado = biblioteca.prestar_libro("JP001", "978-0156012195")
    print(f"Préstamo de 'El Principito' a Juan: {'Éxito' if resultado else 'Fallido'}")
    
    # Devolver un libro
    print("\n=== Devolviendo libro ===")
    usuario2.devolver_libro(libro2)
    print(libro2)
    print(usuario2)