import tkinter as tk
from tkinter import ttk
from model.priority_flag import PriorityFlag

class TaskListPanel:
    PRIORITY_COLORS = {
        PriorityFlag.MUITO_IMPORTANTE.value: "maroon",
        PriorityFlag.IMPORTANTE.value: "darkorange",
        PriorityFlag.MEDIA.value: "gold",
        PriorityFlag.SIMPLES.value: "forestgreen",
        "EVENTO": "dodgerblue",
        "GERAL": "gray"
    }

    def __init__(self, parent, toggle_callback):
        self.toggle_callback = toggle_callback
        self.container = ttk.Frame(parent)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.task_frame = ttk.Frame(self.container)
        self.task_frame.pack(fill=tk.BOTH, expand=True)

    def update_task_list(self, date, tasks, editor_mode=False):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        if not tasks:
            ttk.Label(self.task_frame, text="Nenhuma tarefa para esta data.").pack(pady=20)
            return

        grouped_tasks = {
            "EVENTO": [],
            PriorityFlag.MUITO_IMPORTANTE.value: [],
            PriorityFlag.IMPORTANTE.value: [],
            PriorityFlag.MEDIA.value: [],
            PriorityFlag.SIMPLES.value: [],
            "GERAL": []
        }
        for task in tasks:
            if task.is_evento:
                grouped_tasks["EVENTO"].append(task)
            elif task.priority:
                grouped_tasks[task.priority.value].append(task)
            else:
                grouped_tasks["GERAL"].append(task)

        # Renderizar seções em colunas
        priority_order = ["EVENTO", PriorityFlag.MUITO_IMPORTANTE.value, PriorityFlag.IMPORTANTE.value, PriorityFlag.MEDIA.value, PriorityFlag.SIMPLES.value, "GERAL"]
        
        active_groups = [p for p in priority_order if grouped_tasks[p]]

        for col_index, priority in enumerate(active_groups):
            self.task_frame.grid_columnconfigure(col_index, weight=1, uniform="group1")

            color = self.PRIORITY_COLORS.get(priority, "gray")
            
            section_frame = tk.Frame(self.task_frame, bd=2, relief="solid", highlightbackground=color, highlightthickness=2)
            section_frame.grid(row=0, column=col_index, padx=5, pady=5, sticky='nsew')
            
            content_frame = ttk.Frame(section_frame)
            content_frame.pack(padx=10, pady=10, fill='both', expand=True)

            title_text = "Eventos" if priority == "EVENTO" else priority.replace('-', ' ').title()
            ttk.Label(content_frame, text=title_text, foreground=color, font=("Arial", 12, "bold")).pack(anchor='w', pady=(0, 10))

            for task in grouped_tasks[priority]:
                self._create_task_row(content_frame, date, task)
    
    def _create_task_row(self, parent, date, task):
        task_var = tk.BooleanVar(value=(task.status == 'concluída'))
        task_key = (date, task.description, task.nome)
        
        row = ttk.Frame(parent)
        row.pack(fill='x', pady=2)

        checkbox = ttk.Checkbutton(row, variable=task_var)
        checkbox.pack(side='left', padx=(0, 5))

        desc_text = f"{task.nome}: {task.description}" if task.nome else task.description
        if task.is_evento and task.dias_evento:
            desc_text = f"[{','.join(task.dias_evento).upper()}] {desc_text}"

        label_fg = "gray" if task_var.get() else "black"
        label_font = ("Arial", 10, "overstrike") if task_var.get() else ("Arial", 10)
        
        task_label = ttk.Label(row, text=desc_text, font=label_font, foreground=label_fg, wraplength=150) # Reduzido wraplength para colunas
        task_label.pack(side='left', anchor='w', fill='x', expand=True)
        
        def toggle_command():
            is_done = task_var.get()
            new_fg = "gray" if is_done else "black"
            new_font = ("Arial", 10, "overstrike") if is_done else ("Arial", 10)
            task_label.config(foreground=new_fg, font=new_font)
            self.toggle_callback(task_key, is_done)

        checkbox.config(command=toggle_command)