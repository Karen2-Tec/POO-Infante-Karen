class Libro:
    """
    Clase que representa un libro en la biblioteca digital.
    Utiliza una tupla para almacenar el autor y el título, ya que estos no cambiarán una vez creados.
    """

    def __init__(self, titulo, autor, categoria, isbn):
        # Tupla para autor y título (inmutables)
        self.datos = (autor, titulo)
        self.categoria = categoria
        self.isbn = isbn
        self.disponible = True

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"'{self.datos[1]}' por {self.datos[0]} - {self.categoria} (ISBN: {self.isbn}) - {estado}"

    def obtener_autor(self):
        return self.datos[0]

    def obtener_titulo(self):
        return self.datos[1]


class Usuario:
    """
    Clase que representa a un usuario de la biblioteca.
    Cada usuario tiene una lista de libros actualmente prestados.
    """

    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        # Lista para gestionar los libros prestados al usuario
        self.libros_prestados = []

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.id_usuario}) - Libros prestados: {len(self.libros_prestados)}"

    def prestar_libro(self, libro):
        """Añade un libro a la lista de libros prestados del usuario."""
        self.libros_prestados.append(libro)

    def devolver_libro(self, isbn):
        """Elimina un libro de la lista de libros prestados del usuario por ISBN."""
        for i, libro in enumerate(self.libros_prestados):
            if libro.isbn == isbn:
                return self.libros_prestados.pop(i)
        return None


class Biblioteca:
    """
    Clase principal que gestiona la biblioteca digital.
    Utiliza diversas estructuras de datos para gestionar libros, usuarios y préstamos.
    """

    def __init__(self):
        # Diccionario para almacenar libros por ISBN (búsqueda eficiente)
        self.libros = {}
        # Conjunto para IDs de usuario únicos
        self.ids_usuarios = set()
        # Diccionario para almacenar usuarios por ID
        self.usuarios = {}
        # Lista para el historial de préstamos
        self.historial_prestamos = []

    def añadir_libro(self, titulo, autor, categoria, isbn):
        """Añade un nuevo libro a la biblioteca."""
        if isbn in self.libros:
            print(f"Error: Ya existe un libro con ISBN {isbn}.")
            return False

        nuevo_libro = Libro(titulo, autor, categoria, isbn)
        self.libros[isbn] = nuevo_libro
        print(f"Libro '{titulo}' añadido correctamente.")
        return True

    def quitar_libro(self, isbn):
        """Elimina un libro de la biblioteca por ISBN."""
        if isbn not in self.libros:
            print(f"Error: No existe un libro con ISBN {isbn}.")
            return False

        libro = self.libros[isbn]
        if not libro.disponible:
            print(f"Error: El libro '{libro.obtener_titulo()}' está prestado y no se puede eliminar.")
            return False

        del self.libros[isbn]
        print(f"Libro '{libro.obtener_titulo()}' eliminado correctamente.")
        return True

    def registrar_usuario(self, nombre, id_usuario):
        """Registra un nuevo usuario en la biblioteca."""
        if id_usuario in self.ids_usuarios:
            print(f"Error: Ya existe un usuario con ID {id_usuario}.")
            return False

        nuevo_usuario = Usuario(nombre, id_usuario)
        self.usuarios[id_usuario] = nuevo_usuario
        self.ids_usuarios.add(id_usuario)
        print(f"Usuario '{nombre}' registrado correctamente con ID {id_usuario}.")
        return True

    def dar_de_baja_usuario(self, id_usuario):
        """Da de baja a un usuario de la biblioteca."""
        if id_usuario not in self.ids_usuarios:
            print(f"Error: No existe un usuario con ID {id_usuario}.")
            return False

        usuario = self.usuarios[id_usuario]
        if usuario.libros_prestados:
            print(f"Error: El usuario tiene {len(usuario.libros_prestados)} libros prestados.")
            return False

        del self.usuarios[id_usuario]
        self.ids_usuarios.remove(id_usuario)
        print(f"Usuario '{usuario.nombre}' dado de baja correctamente.")
        return True

    def prestar_libro(self, isbn, id_usuario):
        """Presta un libro a un usuario."""
        if isbn not in self.libros:
            print(f"Error: No existe un libro con ISBN {isbn}.")
            return False

        if id_usuario not in self.ids_usuarios:
            print(f"Error: No existe un usuario con ID {id_usuario}.")
            return False

        libro = self.libros[isbn]
        usuario = self.usuarios[id_usuario]

        if not libro.disponible:
            print(f"Error: El libro '{libro.obtener_titulo()}' no está disponible.")
            return False

        # Realizar el préstamo
        libro.disponible = False
        usuario.prestar_libro(libro)

        # Registrar en el historial
        from datetime import datetime
        self.historial_prestamos.append({
            'accion': 'préstamo',
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'usuario': usuario.nombre,
            'libro': libro.obtener_titulo(),
            'isbn': isbn
        })

        print(f"Libro '{libro.obtener_titulo()}' prestado a {usuario.nombre}.")
        return True

    def devolver_libro(self, isbn, id_usuario):
        """Devuelve un libro prestado por un usuario."""
        if isbn not in self.libros:
            print(f"Error: No existe un libro con ISBN {isbn}.")
            return False

        if id_usuario not in self.ids_usuarios:
            print(f"Error: No existe un usuario con ID {id_usuario}.")
            return False

        libro = self.libros[isbn]
        usuario = self.usuarios[id_usuario]

        if libro.disponible:
            print(f"Error: El libro '{libro.obtener_titulo()}' ya está disponible.")
            return False

        # Verificar que el usuario tiene el libro prestado
        libro_devuelto = usuario.devolver_libro(isbn)
        if not libro_devuelto:
            print(f"Error: El usuario {usuario.nombre} no tiene prestado el libro con ISBN {isbn}.")
            return False

        # Realizar la devolución
        libro.disponible = True

        # Registrar en el historial
        from datetime import datetime
        self.historial_prestamos.append({
            'accion': 'devolución',
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'usuario': usuario.nombre,
            'libro': libro.obtener_titulo(),
            'isbn': isbn
        })

        print(f"Libro '{libro.obtener_titulo()}' devuelto por {usuario.nombre}.")
        return True

    def buscar_libros(self, criterio, valor):
        """Busca libros por título, autor o categoría."""
        resultados = []

        for isbn, libro in self.libros.items():
            if criterio == 'titulo' and valor.lower() in libro.obtener_titulo().lower():
                resultados.append(libro)
            elif criterio == 'autor' and valor.lower() in libro.obtener_autor().lower():
                resultados.append(libro)
            elif criterio == 'categoria' and valor.lower() in libro.categoria.lower():
                resultados.append(libro)

        return resultados

    def listar_libros_prestados(self, id_usuario):
        """Lista todos los libros prestados a un usuario específico."""
        if id_usuario not in self.ids_usuarios:
            print(f"Error: No existe un usuario con ID {id_usuario}.")
            return None

        usuario = self.usuarios[id_usuario]
        return usuario.libros_prestados

    def mostrar_estado(self):
        """Muestra el estado actual de la biblioteca."""
        print("\n=== ESTADO DE LA BIBLIOTECA ===")
        print(f"Total de libros: {len(self.libros)}")
        print(f"Total de usuarios: {len(self.usuarios)}")

        # Contar libros prestados
        libros_prestados = sum(1 for libro in self.libros.values() if not libro.disponible)
        print(f"Libros prestados: {libros_prestados}")
        print(f"Préstamos en historial: {len(self.historial_prestamos)}")
        print("===============================\n")

    def mostrar_libros(self):
        """Muestra todos los libros en la biblioteca."""
        if not self.libros:
            print("No hay libros en la biblioteca.")
            return

        print("\n=== LIBROS EN LA BIBLIOTECA ===")
        for libro in self.libros.values():
            print(f"- {libro}")
        print("===============================\n")

    def mostrar_usuarios(self):
        """Muestra todos los usuarios registrados."""
        if not self.usuarios:
            print("No hay usuarios registrados.")
            return

        print("\n=== USUARIOS REGISTRADOS ===")
        for usuario in self.usuarios.values():
            print(f"- {usuario}")
        print("============================\n")


# Función para mostrar el menú principal
def mostrar_menu():
    """Muestra el menú principal de la aplicación."""
    print("\n=== SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL ===")
    print("1. Añadir libro")
    print("2. Quitar libro")
    print("3. Registrar usuario")
    print("4. Dar de baja usuario")
    print("5. Prestar libro")
    print("6. Devolver libro")
    print("7. Buscar libros")
    print("8. Listar libros prestados a un usuario")
    print("9. Mostrar todos los libros")
    print("10. Mostrar todos los usuarios")
    print("11. Mostrar estado de la biblioteca")
    print("0. Salir")
    print("==============================================")


# Función principal para ejecutar el sistema
def main():
    """Función principal que ejecuta el sistema de biblioteca."""
    biblioteca = Biblioteca()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n--- AÑADIR LIBRO ---")
            titulo = input("Título: ")
            autor = input("Autor: ")
            categoria = input("Categoría: ")
            isbn = input("ISBN: ")
            biblioteca.añadir_libro(titulo, autor, categoria, isbn)

        elif opcion == "2":
            print("\n--- QUITAR LIBRO ---")
            isbn = input("ISBN del libro a eliminar: ")
            biblioteca.quitar_libro(isbn)

        elif opcion == "3":
            print("\n--- REGISTRAR USUARIO ---")
            nombre = input("Nombre: ")
            id_usuario = input("ID de usuario: ")
            biblioteca.registrar_usuario(nombre, id_usuario)

        elif opcion == "4":
            print("\n--- DAR DE BAJA USUARIO ---")
            id_usuario = input("ID del usuario a dar de baja: ")
            biblioteca.dar_de_baja_usuario(id_usuario)

        elif opcion == "5":
            print("\n--- PRESTAR LIBRO ---")
            isbn = input("ISBN del libro: ")
            id_usuario = input("ID del usuario: ")
            biblioteca.prestar_libro(isbn, id_usuario)

        elif opcion == "6":
            print("\n--- DEVOLVER LIBRO ---")
            isbn = input("ISBN del libro: ")
            id_usuario = input("ID del usuario: ")
            biblioteca.devolver_libro(isbn, id_usuario)

        elif opcion == "7":
            print("\n--- BUSCAR LIBROS ---")
            print("Criterios de búsqueda: título, autor, categoria")
            criterio = input("Criterio de búsqueda: ")
            valor = input("Valor a buscar: ")
            resultados = biblioteca.buscar_libros(criterio, valor)

            if resultados:
                print(f"\nResultados de la búsqueda ({len(resultados)} encontrados):")
                for libro in resultados:
                    print(f"- {libro}")
            else:
                print("No se encontraron resultados.")

        elif opcion == "8":
            print("\n--- LIBROS PRESTADOS A USUARIO ---")
            id_usuario = input("ID del usuario: ")
            libros_prestados = biblioteca.listar_libros_prestados(id_usuario)

            if libros_prestados is not None:
                if libros_prestados:
                    print(f"\nLibros prestados a {biblioteca.usuarios[id_usuario].nombre}:")
                    for libro in libros_prestados:
                        print(f"- {libro}")
                else:
                    print("El usuario no tiene libros prestados.")

        elif opcion == "9":
            biblioteca.mostrar_libros()

        elif opcion == "10":
            biblioteca.mostrar_usuarios()

        elif opcion == "11":
            biblioteca.mostrar_estado()

        elif opcion == "0":
            print("¡Gracias por usar el Sistema de Gestión de Biblioteca Digital!")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")


if __name__ == "__main__":
    main()