import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')

        # Lista para almacenar las tareas
        self.tasks: List[Dict[str, Any]] = []

        # Definir atributos de la interfaz
        self.task_entry: ttk.Entry
        self.add_button: ttk.Button
        self.complete_button: ttk.Button
        self.delete_button: ttk.Button
        self.task_tree: ttk.Treeview

        # Configurar el estilo
        self.setup_styles()

        # Crear la interfaz
        self.create_widgets()

        # Configurar atajos de teclado
        self.setup_keyboard_shortcuts()

    @staticmethod
    def setup_styles():
        """Configurar estilos para la aplicación"""
        style = ttk.Style()
        style.configure('Completed.TLabel', foreground='gray', font=('Arial', 10, 'overstrike'))
        style.configure('Pending.TLabel', foreground='black', font=('Arial', 10))
        style.configure('Custom.TButton', font=('Arial', 9))

    def create_widgets(self):
        """Crear todos los elementos de la interfaz"""

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Título
        title_label = ttk.Label(main_frame, text="Gestor de Tareas",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        # Frame para entrada de nueva tarea
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)

        # Etiqueta y campo de entrada
        ttk.Label(input_frame, text="Nueva Tarea:").grid(row=0, column=0, sticky=tk.W)

        self.task_entry = ttk.Entry(input_frame, font=('Arial', 11))
        self.task_entry.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 5))
        self.task_entry.focus()

        # Botones de acción
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=3, pady=(0, 10))

        self.add_button = ttk.Button(buttons_frame, text="Añadir Tarea (Enter)",
                                     command=self.add_task, style='Custom.TButton')
        self.add_button.grid(row=0, column=0, padx=(0, 5))

        self.complete_button = ttk.Button(buttons_frame, text="Completar (C)",
                                          command=self.complete_task, style='Custom.TButton')
        self.complete_button.grid(row=0, column=1, padx=5)

        self.delete_button = ttk.Button(buttons_frame, text="Eliminar (Delete)",
                                        command=self.delete_task, style='Custom.TButton')
        self.delete_button.grid(row=0, column=2, padx=5)

        # Frame para la lista de tareas
        list_frame = ttk.LabelFrame(main_frame, text="Lista de Tareas", padding="5")
        list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Crear Treeview para mostrar las tareas
        self.create_task_list(list_frame)

        # Etiqueta de información
        info_label = ttk.Label(main_frame,
                               text="Atajos: Enter=Añadir, C=Completar, Delete=Eliminar, Escape=Salir",
                               font=('Arial', 9), foreground='gray')
        info_label.grid(row=4, column=0, columnspan=3, pady=(10, 0))

    def create_task_list(self, parent):
        """Crear la lista de tareas usando Treeview"""
        # Crear Treeview con una columna
        self.task_tree = ttk.Treeview(parent, columns=('status', 'task'), show='tree headings', height=12)
        self.task_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar columnas
        self.task_tree.heading('#0', text='#')
        self.task_tree.column('#0', width=40, anchor='center')

        self.task_tree.heading('status', text='Estado')
        self.task_tree.column('status', width=80, anchor='center')

        self.task_tree.heading('task', text='Tarea')
        self.task_tree.column('task', width=400, anchor='w')

        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.task_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        # Bind para selección simple
        self.task_tree.bind('<<TreeviewSelect>>', self.on_task_select)

    def setup_keyboard_shortcuts(self):
        """Configurar los atajos de teclado"""
        # Enter para añadir tarea
        self.root.bind('<Return>', lambda event: self.add_task())

        # C para completar tarea
        self.root.bind('<c>', lambda event: self.complete_task())
        self.root.bind('<C>', lambda event: self.complete_task())

        # Delete para eliminar tarea
        self.root.bind('<Delete>', lambda event: self.delete_task())
        self.root.bind('<d>', lambda event: self.delete_task())
        self.root.bind('<D>', lambda event: self.delete_task())

        # Escape para salir
        self.root.bind('<Escape>', lambda event: self.root.quit())

        # Bind especial para el campo de entrada (evitar conflicto con Enter)
        self.task_entry.bind('<Return>', lambda event: self.add_task())

    def on_task_select(self, event=None):
        """Manejar selección de tareas"""
        selection = self.task_tree.selection()
        if selection:
            # Habilitar botones cuando hay selección
            self.complete_button.config(state='normal')
            self.delete_button.config(state='normal')
        else:
            # Deshabilitar botones cuando no hay selección
            self.complete_button.config(state='disabled')
            self.delete_button.config(state='disabled')

    def add_task(self, event=None):
        """Añadir una nueva tarea a la lista"""
        task_text = self.task_entry.get().strip()

        if task_text:
            # Añadir a la lista interna
            task_id = len(self.tasks) + 1
            task_data = {
                'id': task_id,
                'text': task_text,
                'completed': False
            }
            self.tasks.append(task_data)

            # Añadir a la vista
            self.refresh_task_list()

            # Limpiar campo de entrada
            self.task_entry.delete(0, tk.END)

            # Mostrar mensaje de confirmación
            self.show_status_message(f"Tarea añadida: {task_text}")
        else:
            messagebox.showwarning("Entrada vacía", "Por favor, escribe una tarea antes de añadirla.")

        # Regresar el foco al campo de entrada
        self.task_entry.focus()

    def complete_task(self, event=None):
        """Marcar la tarea seleccionada como completada"""
        selection = self.task_tree.selection()
        if selection:
            item = selection[0]
            task_id = int(self.task_tree.item(item, 'text')) - 1

            if 0 <= task_id < len(self.tasks):
                self.tasks[task_id]['completed'] = True
                self.refresh_task_list()
                self.show_status_message("Tarea marcada como completada")

        self.task_entry.focus()

    def delete_task(self, event=None):
        """Eliminar la tarea seleccionada"""
        selection = self.task_tree.selection()
        if selection:
            item = selection[0]
            task_id = int(self.task_tree.item(item, 'text')) - 1

            if 0 <= task_id < len(self.tasks):
                task_text = self.tasks[task_id]['text']

                # Confirmar eliminación
                if messagebox.askyesno("Confirmar eliminación",
                                       f"¿Estás seguro de que quieres eliminar la tarea: '{task_text}'?"):
                    # Eliminar de la lista
                    del self.tasks[task_id]

                    # Reindexar las tareas
                    for i, task in enumerate(self.tasks):
                        task['id'] = i + 1

                    self.refresh_task_list()
                    self.show_status_message("Tarea eliminada")

        self.task_entry.focus()

    def refresh_task_list(self):
        """Actualizar la lista visual de tareas"""
        # Limpiar lista actual
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        # Añadir todas las tareas
        for task in self.tasks:
            status = "✓ Completada" if task['completed'] else "⏳ Pendiente"
            tags = ('completed',) if task['completed'] else ('pending',)

            item_id = str(task['id'])
            status_text = str(status)
            task_text = str(task['text'])

            self.task_tree.insert('', 'end', text=item_id,
                                  values=(status_text, task_text),
                                  tags=tags)

            # Aplicar estilo según el estado
            if task['completed']:
                self.task_tree.tag_configure('completed', foreground='gray')
            else:
                self.task_tree.tag_configure('pending', foreground='black')

    @staticmethod
    def show_status_message(message: str):
        """Mostrar mensaje de estado temporal"""
        # En una aplicación más compleja, podrías tener una barra de estado
        print(f"Estado: {message}")  # Por simplicidad, mostramos en consola


def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()