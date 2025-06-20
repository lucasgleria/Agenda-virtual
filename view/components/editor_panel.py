import tkinter as tk
from tkinter import ttk

class EditorPanel:
    def __init__(self, parent, on_edit, on_delete):
        self.on_edit = on_edit
        self.on_delete = on_delete

        self.frame = ttk.LabelFrame(parent, text="Modo Editor", padding=10)
        self.task_frame = ttk.Frame(self.frame)
        self.task_frame.pack(fill='both', expand=True)

    def update_editor_panel(self, date, tasks, visible):
        # Limpa os widgets anteriores
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        if visible:
            self.frame.pack(fill='both', expand=False, pady=5)
        else:
            self.frame.pack_forget()
            return

        for task in tasks:
            row = ttk.Frame(self.task_frame)
            row.pack(anchor='w', fill='x', pady=2)

            nome_info = f" [{task.nome}]" if task.nome else ""
            evento_info = f" [EVENTO: {', '.join(task.dias_evento)}]" if task.is_evento else ""
            agendamento_info = " [Agendamento]" if task.is_agendamento else ""

            label = ttk.Label(row, text=f"{task.description}{nome_info}{evento_info}{agendamento_info}")
            label.pack(side='left', padx=5)

            btn_edit = ttk.Button(row, text="Editar", width=8, command=lambda t=task: self.on_edit(date, t))
            btn_edit.pack(side='right', padx=(2, 0))

            btn_delete = ttk.Button(row, text="Excluir", width=8, command=lambda t=task: self.on_delete(date, t))
            btn_delete.pack(side='right')
