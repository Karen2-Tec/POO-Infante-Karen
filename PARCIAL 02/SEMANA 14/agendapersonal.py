import tkinter as tk
from tkinter import ttk, messagebox
import datetime


class AgendaPersonal:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Personal")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Lista para almacenar eventos
        self.eventos = []

        # Configurar estilo
        self.configurar_estilos()

        # Crear la interfaz
        self.crear_interfaz()

    def configurar_estilos(self):
        """Configura los estilos para los widgets de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configurar estilo para los botones
        style.configure('TButton', font=('Arial', 10), padding=5)

        # Configurar estilo para el TreeView
        style.configure('Treeview', font=('Arial', 10), rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 11, 'bold'))

    def crear_interfaz(self):
        """Crea y organiza todos los componentes de la interfaz"""
        # Frame principal que contendrá todos los elementos
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid para que se expanda
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Título de la aplicación
        titulo = ttk.Label(main_frame, text="Agenda Personal", font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Frame para la entrada de datos
        input_frame = ttk.LabelFrame(main_frame, text="Nuevo Evento", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)

        # Etiqueta y campo para la fecha
        ttk.Label(input_frame, text="Fecha (YYYY-MM-DD):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        self.fecha_var = tk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))
        self.fecha_entry = ttk.Entry(input_frame, textvariable=self.fecha_var, width=12)
        self.fecha_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=5)

        # Etiqueta y campo para la hora
        ttk.Label(input_frame, text="Hora (HH:MM):").grid(row=0, column=2, sticky=tk.W, padx=(0, 5), pady=5)
        self.hora_var = tk.StringVar(value=datetime.datetime.now().strftime("%H:%M"))
        self.hora_entry = ttk.Entry(input_frame, textvariable=self.hora_var, width=8)
        self.hora_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 10), pady=5)

        # Etiqueta y campo para la descripción
        ttk.Label(input_frame, text="Descripción:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        self.descripcion_entry = ttk.Entry(input_frame, width=40)
        self.descripcion_entry.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), padx=(0, 10), pady=5)

        # Frame para los botones de acción
        botones_frame = ttk.Frame(input_frame)
        botones_frame.grid(row=2, column=0, columnspan=4, pady=10)

        # Botón para agregar evento
        self.agregar_btn = ttk.Button(botones_frame, text="Agregar Evento", command=self.agregar_evento)
        self.agregar_btn.pack(side=tk.LEFT, padx=5)

        # Botón para eliminar evento
        self.eliminar_btn = ttk.Button(botones_frame, text="Eliminar Evento Seleccionado",
                                       command=self.eliminar_evento)
        self.eliminar_btn.pack(side=tk.LEFT, padx=5)

        # Frame para la lista de eventos
        lista_frame = ttk.LabelFrame(main_frame, text="Eventos Programados", padding="10")
        lista_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        lista_frame.columnconfigure(0, weight=1)
        lista_frame.rowconfigure(0, weight=1)

        # TreeView para mostrar los eventos
        columnas = ('fecha', 'hora', 'descripcion')
        self.treeview = ttk.Treeview(lista_frame, columns=columnas, show='headings')

        # Definir encabezados
        self.treeview.heading('fecha', text='Fecha')
        self.treeview.heading('hora', text='Hora')
        self.treeview.heading('descripcion', text='Descripción')

        # Definir anchos de columnas
        self.treeview.column('fecha', width=100, anchor=tk.CENTER)
        self.treeview.column('hora', width=80, anchor=tk.CENTER)
        self.treeview.column('descripcion', width=400, anchor=tk.W)

        # Scrollbar para el TreeView
        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Colocar TreeView y Scrollbar en la interfaz
        self.treeview.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Frame para el botón de salir
        salir_frame = ttk.Frame(main_frame)
        salir_frame.grid(row=3, column=0, columnspan=3, pady=20)

        # Botón para salir
        self.salir_btn = ttk.Button(salir_frame, text="Salir", command=self.root.quit)
        self.salir_btn.pack()

        # Bind para permitir agregar eventos con Enter
        self.descripcion_entry.bind('<Return>', lambda e: self.agregar_evento())

    def agregar_evento(self):
        """Agrega un nuevo evento a la lista"""
        fecha = self.fecha_var.get()
        hora = self.hora_var.get()
        descripcion = self.descripcion_entry.get().strip()

        # Validar los datos de entrada
        if not descripcion:
            messagebox.showerror("Error", "La descripción no puede estar vacía")
            return

        if not self.validar_fecha(fecha):
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            return

        if not self.validar_hora(hora):
            messagebox.showerror("Error", "Formato de hora inválido. Use HH:MM")
            return

        # Agregar el evento a la lista
        evento = {
            'fecha': fecha,
            'hora': hora,
            'descripcion': descripcion
        }
        self.eventos.append(evento)

        # Actualizar el TreeView
        self.actualizar_treeview()

        # Limpiar el campo de descripción
        self.descripcion_entry.delete(0, tk.END)

    def eliminar_evento(self):
        """Elimina el evento seleccionado de la lista"""
        seleccion = self.treeview.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un evento para eliminar")
            return

        # Mostrar diálogo de confirmación
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar el evento seleccionado?"):
            # Obtener el índice del elemento seleccionado
            index = int(seleccion[0].lstrip('I')) - 1

            # Eliminar el evento de la lista
            if 0 <= index < len(self.eventos):
                del self.eventos[index]

            # Actualizar el TreeView
            self.actualizar_treeview()

    def actualizar_treeview(self):
        """Actualiza el TreeView con los eventos actuales"""
        # Limpiar el TreeView
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Ordenar eventos por fecha y hora
        eventos_ordenados = sorted(self.eventos, key=lambda x: (x['fecha'], x['hora']))

        # Agregar eventos al TreeView
        for evento in eventos_ordenados:
            self.treeview.insert('', tk.END, values=(
                evento['fecha'], evento['hora'], evento['descripcion']
            ))

    def validar_fecha(self, fecha_str):
        """Valida que el formato de fecha sea correcto (YYYY-MM-DD)"""
        try:
            datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validar_hora(self, hora_str):
        """Valida que el formato de hora sea correcto (HH:MM)"""
        try:
            datetime.datetime.strptime(hora_str, "%H:%M")
            return True
        except ValueError:
            return False


def main():
    """Función principal que inicia la aplicación"""
    root = tk.Tk()
    app = AgendaPersonal(root)
    root.mainloop()


if __name__ == "__main__":
    main()