import tkinter as tk
from tkinter import ttk, messagebox


class TodoApp:
    def __init__(self, root):
        # Configuración de la ventana principal
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("500x400")
        self.root.resizable(True, True)

        # Lista para almacenar las tareas (cada tarea es un diccionario con texto y estado)
        self.tasks = []

        # Inicializar atributos de instancia
        self.task_entry = None
        self.add_button = None
        self.task_listbox = None
        self.complete_button = None
        self.delete_button = None
        self.clear_completed_button = None

        # Crear y configurar los elementos de la interfaz
        self.create_widgets()

        # Vincular la tecla Enter al campo de entrada
        self.task_entry.bind('<Return>', lambda event: self.add_task())

    def create_widgets(self):
        """Crea y organiza todos los elementos de la interfaz gráfica"""

        # Frame principal para organizar los elementos
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configurar la expansión de la ventana
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Etiqueta y campo de entrada para nuevas tareas
        ttk.Label(main_frame, text="Nueva Tarea:").grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.task_entry = ttk.Entry(main_frame, width=40)
        self.task_entry.grid(row=0, column=1, sticky="ew", pady=(0, 10))

        # Botón para añadir tarea
        self.add_button = ttk.Button(main_frame, text="Añadir Tarea", command=self.add_task)
        self.add_button.grid(row=0, column=2, padx=(10, 0), pady=(0, 10))

        # Frame para la lista de tareas y la barra de desplazamiento
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Listbox para mostrar las tareas con barra de desplazamiento
        self.task_listbox = tk.Listbox(list_frame, height=15, selectmode=tk.SINGLE)
        self.task_listbox.grid(row=0, column=0, sticky="nsew")

        # Vincular doble clic para marcar tarea como completada
        self.task_listbox.bind('<Double-Button-1>', self.toggle_task_completion)

        # Barra de desplazamiento para la lista
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.task_listbox.configure(yscrollcommand=scrollbar.set)

        # Frame para los botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        # Botones para marcar como completada y eliminar tarea
        self.complete_button = ttk.Button(button_frame, text="Marcar como Completada",
                                          command=self.mark_completed)
        self.complete_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.delete_button = ttk.Button(button_frame, text="Eliminar Tarea",
                                        command=self.delete_task)
        self.delete_button.grid(row=0, column=1, padx=5, sticky="ew")

        self.clear_completed_button = ttk.Button(button_frame, text="Limpiar Completadas",
                                                 command=self.clear_completed)
        self.clear_completed_button.grid(row=0, column=2, padx=(5, 0), sticky="ew")

    def add_task(self):
        """Añade una nueva tarea a la lista"""
        task_text = self.task_entry.get().strip()

        # Validar que la tarea no esté vacía
        if not task_text:
            messagebox.showwarning("Advertencia", "Por favor, ingresa una tarea.")
            return

        # Crear nueva tarea (inicialmente no completada)
        new_task = {
            "text": task_text,
            "completed": False
        }

        # Añadir a la lista de tareas
        self.tasks.append(new_task)

        # Actualizar la visualización de la lista
        self.update_task_list()

        # Limpiar el campo de entrada y enfocarlo para nueva entrada
        self.task_entry.delete(0, tk.END)
        self.task_entry.focus()

    def mark_completed(self):
        """Marca la tarea seleccionada como completada"""
        selected_index = self.get_selected_index()

        # Validar que haya una tarea seleccionada
        if selected_index is None:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea.")
            return

        # Cambiar el estado de la tarea
        self.tasks[selected_index]["completed"] = not self.tasks[selected_index]["completed"]

        # Actualizar la visualización
        self.update_task_list()

    def toggle_task_completion(self, event):
        """Alterna el estado de completado de una tarea con doble clic"""
        # Obtener el índice de la tarea bajo el cursor
        index = self.task_listbox.nearest(event.y)

        if 0 <= index < len(self.tasks):
            # Cambiar el estado de la tarea
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]

            # Actualizar la visualización
            self.update_task_list()

    def delete_task(self):
        """Elimina la tarea seleccionada"""
        selected_index = self.get_selected_index()

        # Validar que haya una tarea seleccionada
        if selected_index is None:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para eliminar.")
            return

        # Confirmar eliminación
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar esta tarea?")

        if confirm:
            # Eliminar la tarea de la lista
            del self.tasks[selected_index]

            # Actualizar la visualización
            self.update_task_list()

    def clear_completed(self):
        """Elimina todas las tareas marcadas como completadas"""
        # Filtrar solo las tareas no completadas
        self.tasks = [task for task in self.tasks if not task["completed"]]

        # Actualizar la visualización
        self.update_task_list()

    def get_selected_index(self):
        """Obtiene el índice de la tarea seleccionada en la lista"""
        selection = self.task_listbox.curselection()
        return selection[0] if selection else None

    def update_task_list(self):
        """Actualiza la visualización de la lista de tareas"""
        # Limpiar la lista actual
        self.task_listbox.delete(0, tk.END)

        # Añadir cada tarea con formato según su estado
        for i, task in enumerate(self.tasks):
            task_text = task["text"]

            # Aplicar formato diferente para tareas completadas
            if task["completed"]:
                # Tachar el texto para indicar completado
                task_text = f"✓ {task_text}"
                self.task_listbox.insert(tk.END, task_text)

                # Cambiar el color de fondo para tareas completadas
                self.task_listbox.itemconfig(i, {'bg': '#f0f0f0', 'fg': '#888888'})
            else:
                self.task_listbox.insert(tk.END, task_text)
                # Asegurar que las tareas no completadas tengan colores normales
                self.task_listbox.itemconfig(i, {'bg': 'white', 'fg': 'black'})


def main():
    # Crear la ventana principal
    root = tk.Tk()

    # Crear la aplicación
    app = TodoApp(root)

    # Iniciar el bucle principal de la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()