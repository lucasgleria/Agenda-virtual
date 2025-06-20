import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from model.priority_flag import PriorityFlag

class CalendarPanel:
    DIAS_SEMANA = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']

    def __init__(self, parent, on_add_task, on_add_evento, on_date_change):
        self.on_add_task = on_add_task
        self.on_add_evento = on_add_evento
        self.on_date_change = on_date_change
        self.controller = None
        self.nome_opcoes = set()

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='x')

        self.calendar = Calendar(self.frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(pady=10)
        self.calendar.bind("<<CalendarSelected>>", lambda e: self.on_date_change())

        self.task_entry = ttk.Entry(self.frame, width=50)
        self.task_entry.pack(pady=5)
        self.task_entry.insert(0, "Digite a tarefa")

        ttk.Label(self.frame, text="Prioridade:").pack()
        self.priority_var = tk.StringVar()
        self.priority_combo = ttk.Combobox(self.frame, textvariable=self.priority_var)
        self.priority_combo['values'] = [p.value for p in PriorityFlag]
        self.priority_combo.current(0)
        self.priority_combo.pack(pady=5)

        ttk.Label(self.frame, text="Nome (opcional):").pack()
        self.nome_var = tk.StringVar()
        self.nome_combo = ttk.Combobox(self.frame, textvariable=self.nome_var)
        self.nome_combo.pack(pady=5)

        self.agendamento_var = tk.BooleanVar()
        self.agendamento_checkbox = ttk.Checkbutton(
            self.frame, text="É um agendamento?", variable=self.agendamento_var)
        self.agendamento_checkbox.pack(pady=5)

        self.evento_var = tk.BooleanVar()
        self.evento_checkbox = ttk.Checkbutton(
            self.frame, text="É um evento?", variable=self.evento_var, command=self.toggle_dias_semana)
        self.evento_checkbox.pack(pady=5)

        self.dias_vars = {dia: tk.BooleanVar() for dia in self.DIAS_SEMANA}
        self.dias_frame = ttk.Frame(self.frame)
        for dia in self.DIAS_SEMANA:
            ttk.Checkbutton(self.dias_frame, text=dia, variable=self.dias_vars[dia]).pack(side='left')

        self.add_button = ttk.Button(self.frame, text="Adicionar Tarefa ou Evento", command=self.add_entry)
        self.add_button.pack(pady=10)

        self.editor_button = ttk.Button(self.frame, text="Modo Editor", command=self.toggle_editor_mode)
        self.editor_button.pack(pady=5)
        
        # Botões de Backup e Exportação
        self.backup_frame = ttk.Frame(self.frame)
        self.backup_frame.pack(pady=10)

        self.export_button = ttk.Button(self.backup_frame, text="Exportar Dados (JSON)", command=self.handle_export_data)
        self.export_button.pack(side='left', padx=5)

        self.backup_button = ttk.Button(self.backup_frame, text="Criar Backup Interno", command=self.handle_create_backup)
        self.backup_button.pack(side='left', padx=5)

    def set_controller(self, controller):
        self.controller = controller

    def get_selected_date(self):
        return self.calendar.get_date()

    def reset_inputs(self):
        self.task_entry.delete(0, tk.END)
        self.nome_var.set("")
        self.agendamento_var.set(False)
        self.evento_var.set(False)
        for var in self.dias_vars.values():
            var.set(False)
        self.dias_frame.pack_forget()

    def toggle_dias_semana(self):
        if self.evento_var.get():
            self.dias_frame.pack(pady=5)
        else:
            self.dias_frame.pack_forget()

    def add_entry(self):
        description = self.task_entry.get().strip()
        if not description:
            return

        nome = self.nome_var.get().strip()
        if nome:
            self.nome_opcoes.add(nome)
            self.nome_combo['values'] = sorted(self.nome_opcoes)

        if self.evento_var.get():
            dias_ativos = [dia for dia, var in self.dias_vars.items() if var.get()]
            if dias_ativos:
                evento_data = {
                    "description": description,
                    "nome": nome or None,
                    "dias_semana": dias_ativos
                }
                self.on_add_evento(evento_data)
        else:
            task_data = {
                "date": self.get_selected_date(),
                "description": description,
                "priority": self.priority_var.get(),
                "nome": nome or None,
                "is_agendamento": self.agendamento_var.get(),
                "is_evento": False
            }
            self.on_add_task(task_data)

    def set_toggle_editor_mode_callback(self, callback):
        self._toggle_editor_mode_callback = callback

    def toggle_editor_mode(self):
        if hasattr(self, "_toggle_editor_mode_callback"):
            self._toggle_editor_mode_callback()

    def handle_export_data(self):
        if self.controller:
            self.controller.handle_export_data()

    def handle_create_backup(self):
        if self.controller:
            self.controller.handle_create_backup()
