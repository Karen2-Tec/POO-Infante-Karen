import tkinter as tk
from tkinter import ttk, messagebox


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas - Aplicación GUI")
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        # Lista para almacenar las tareas
        self.tasks = []

        # Configurar el estilo
        self.setup_styles()

        # Crear la interfaz
        self.create_widgets()

    def setup_styles(self):
        """Configura los estilos para los widgets"""
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure("TButton", font=("Arial", 10))
        style.configure("Treeview", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def create_widgets(self):
        """Crea y coloca todos los widgets en la ventana"""
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar la expansión de filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Título de la aplicación
        title_label = ttk.Label(main_frame, text="Gestor de Tareas", style="Header.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Etiqueta y campo de texto para nueva tarea
        ttk.Label(main_frame, text="Nueva tarea:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.task_entry = ttk.Entry(main_frame, width=40)
        self.task_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        self.task_entry.bind("<Return>", lambda event: self.add_task())  # Permitir agregar con Enter

        # Marco para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        # Botones
        self.add_button = ttk.Button(button_frame, text="Agregar Tarea", command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=(0, 5))

        self.clear_button = ttk.Button(button_frame, text="Limpiar", command=self.clear_fields)
        self.clear_button.grid(row=0, column=1, padx=5)

        self.delete_button = ttk.Button(button_frame, text="Eliminar Seleccionada", command=self.delete_task)
        self.delete_button.grid(row=0, column=2, padx=(5, 0))

        # Tabla para mostrar tareas
        ttk.Label(main_frame, text="Tareas:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))

        # Crear Treeview con scrollbar
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Configurar las columnas del Treeview
        columns = ("id", "task")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.heading("task", text="Tarea")
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("task", width=500, anchor=tk.W)

        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Listo")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        # Enfocar el campo de entrada al iniciar
        self.task_entry.focus()

    def add_task(self):
        """Agrega una nueva tarea a la lista"""
        task_text = self.task_entry.get().strip()

        if not task_text:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una tarea.")
            self.task_entry.focus()
            return

        # Agregar la tarea a la lista
        task_id = len(self.tasks) + 1
        self.tasks.append((task_id, task_text))

        # Actualizar el Treeview
        self.tree.insert("", tk.END, values=(task_id, task_text))

        # Limpiar el campo de entrada y actualizar estado
        self.task_entry.delete(0, tk.END)
        self.status_var.set(f"Tarea agregada: {task_text}")
        self.task_entry.focus()

    def delete_task(self):
        """Elimina la tarea seleccionada"""
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una tarea para eliminar.")
            return

        # Obtener los valores de la tarea seleccionada
        item_values = self.tree.item(selected_item, "values")
        task_id = item_values[0]
        task_text = item_values[1]

        # Eliminar de la lista
        self.tasks = [task for task in self.tasks if task[0] != int(task_id)]

        # Eliminar del Treeview
        self.tree.delete(selected_item)

        # Actualizar estado
        self.status_var.set(f"Tarea eliminada: {task_text}")

    def clear_fields(self):
        """Limpia todos los campos y la selección"""
        self.task_entry.delete(0, tk.END)

        # Deseleccionar cualquier elemento seleccionado en el Treeview
        for item in self.tree.selection():
            self.tree.selection_remove(item)

        self.status_var.set("Campos limpiados")
        self.task_entry.focus()


def main():
    """Función principal que inicia la aplicación"""
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()