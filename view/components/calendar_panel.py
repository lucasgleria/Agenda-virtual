import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from model.priority_flag import PriorityFlag
from datetime import datetime
from view.theme.colors import ColorPalette

class CalendarPanel:
    DIAS_SEMANA = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']

    def __init__(self, parent, on_add_task, on_add_evento, on_date_change):
        self.on_add_task = on_add_task
        self.on_add_evento = on_add_evento
        self.on_date_change = on_date_change
        self.controller = None
        self.nome_opcoes = set()

        # Frame principal com layout horizontal
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='x', padx=15, pady=(10, 5))
        
        # Configurar grid weights para widgets internos
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        # Coluna esquerda: Calendário
        self._create_calendar_section()
        
        # Coluna direita: Formulário de entrada
        self._create_input_section()

    def _create_calendar_section(self):
        """Criar seção do calendário"""
        calendar_frame = ttk.LabelFrame(self.frame, text="📅 Calendário", padding=10)
        calendar_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Calendário compacto
        self.calendar = Calendar(calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd',
                               font=("Segoe UI", 9), selectfont=("Segoe UI", 9, "bold"))
        self.calendar.pack(pady=5)
        self.calendar.bind("<<CalendarSelected>>", lambda e: self.on_date_change())
        
        # Data selecionada
        self.date_label = ttk.Label(calendar_frame, text="Data: Hoje", 
                                   font=("Segoe UI", 10, "bold"),
                                   foreground=ColorPalette.TEXT['primary'])
        self.date_label.pack(pady=5)

    def _create_input_section(self):
        """Criar seção de entrada de dados"""
        input_frame = ttk.LabelFrame(self.frame, text="➕ Nova Tarefa/Evento", padding=15)
        input_frame.grid(row=0, column=1, sticky="nsew")
        
        # Grid para organizar os campos
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Linha 1: Descrição
        ttk.Label(input_frame, text="Descrição:", 
                 font=("Segoe UI", 10, "bold"),
                 foreground=ColorPalette.TEXT['primary']).grid(
            row=0, column=0, sticky="w", pady=(0, 5))
        
        self.task_entry = ttk.Entry(input_frame, font=("Segoe UI", 10))
        self.task_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=(0, 10))
        self.task_entry.insert(0, "Digite a descrição da tarefa...")
        self.task_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.task_entry.bind("<FocusOut>", self._on_entry_focus_out)

        # Linha 2: Prioridade e Nome
        ttk.Label(input_frame, text="Prioridade:", 
                 font=("Segoe UI", 10),
                 foreground=ColorPalette.TEXT['primary']).grid(
            row=1, column=0, sticky="w", pady=(0, 5))
        
        self.priority_var = tk.StringVar()
        self.priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var,
                                          values=[p.value for p in PriorityFlag], 
                                          state="readonly", font=("Segoe UI", 9))
        self.priority_combo.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(0, 10))
        self.priority_combo.current(0)

        ttk.Label(input_frame, text="Nome (opc.):", 
                 font=("Segoe UI", 10),
                 foreground=ColorPalette.TEXT['primary']).grid(
            row=1, column=2, sticky="w", padx=(10, 0), pady=(0, 5))
        
        self.nome_var = tk.StringVar()
        self.nome_combo = ttk.Combobox(input_frame, textvariable=self.nome_var,
                                      font=("Segoe UI", 9))
        self.nome_combo.grid(row=1, column=3, sticky="ew", padx=(10, 0), pady=(0, 10))

        # Linha 3: Checkboxes
        checkbox_frame = ttk.Frame(input_frame)
        checkbox_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        
        self.agendamento_var = tk.BooleanVar()
        self.agendamento_checkbox = ttk.Checkbutton(
            checkbox_frame, text="📋 É um agendamento", variable=self.agendamento_var)
        self.agendamento_checkbox.pack(side="left", padx=(0, 20))

        self.evento_var = tk.BooleanVar()
        self.evento_checkbox = ttk.Checkbutton(
            checkbox_frame, text="📅 É um evento", variable=self.evento_var, 
            command=self.toggle_dias_semana)
        self.evento_checkbox.pack(side="left")

        # Linha 4: Dias da semana (inicialmente oculto)
        self.dias_frame = ttk.LabelFrame(input_frame, text="Dias da Semana", padding=5)
        self.dias_frame.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        
        self.dias_vars = {dia: tk.BooleanVar() for dia in self.DIAS_SEMANA}
        for i, dia in enumerate(self.DIAS_SEMANA):
            ttk.Checkbutton(self.dias_frame, text=dia, variable=self.dias_vars[dia]).grid(row=0, column=i, padx=5)
        
        self.dias_frame.grid_remove()  # Oculto por padrão

        # Linha 5: Botões de ação
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(10, 0))
        
        self.add_button = ttk.Button(button_frame, text="➕ Adicionar", 
                                    command=self.add_entry, style="Success.TButton")
        self.add_button.pack(side="left", padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="🗑️ Limpar", 
                                      command=self.reset_inputs)
        self.clear_button.pack(side="left")
        
        # Botões de backup à direita
        backup_frame = ttk.Frame(button_frame)
        backup_frame.pack(side="right")
        
        self.export_button = ttk.Button(backup_frame, text="📤 Exportar", 
                                       command=self.handle_export_data)
        self.export_button.pack(side="right", padx=(5, 0))
        
        self.backup_button = ttk.Button(backup_frame, text="💾 Backup", 
                                       command=self.handle_create_backup)
        self.backup_button.pack(side="right")

    def _on_entry_focus_in(self, event):
        """Quando o entry recebe foco"""
        if self.task_entry.get() == "Digite a descrição da tarefa...":
            self.task_entry.delete(0, tk.END)
            self.task_entry.configure(foreground=ColorPalette.TEXT['primary'])

    def _on_entry_focus_out(self, event):
        """Quando o entry perde foco"""
        if not self.task_entry.get():
            self.task_entry.insert(0, "Digite a descrição da tarefa...")
            self.task_entry.configure(foreground=ColorPalette.TEXT['tertiary'])

    def set_controller(self, controller):
        self.controller = controller

    def get_selected_date(self):
        return self.calendar.get_date()

    def reset_inputs(self):
        """Limpar todos os campos de entrada"""
        self.task_entry.delete(0, tk.END)
        self.task_entry.insert(0, "Digite a descrição da tarefa...")
        self.task_entry.configure(foreground=ColorPalette.TEXT['tertiary'])
        
        self.nome_var.set("")
        self.agendamento_var.set(False)
        self.evento_var.set(False)
        
        for var in self.dias_vars.values():
            var.set(False)
        
        self.dias_frame.grid_remove()
        self.priority_combo.current(0)

    def toggle_dias_semana(self):
        """Mostrar/ocultar seleção de dias da semana"""
        if self.evento_var.get():
            self.dias_frame.grid()
        else:
            self.dias_frame.grid_remove()

    def add_entry(self):
        """Adicionar nova tarefa ou evento"""
        description = self.task_entry.get().strip()
        if not description or description == "Digite a descrição da tarefa...":
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
                self.reset_inputs()
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
            self.reset_inputs()

    def handle_export_data(self):
        if self.controller:
            self.controller.handle_export_data()

    def handle_create_backup(self):
        if self.controller:
            self.controller.handle_create_backup()
    
    def update_date_label(self):
        """Atualizar label da data selecionada"""
        selected_date = self.get_selected_date()
        today = datetime.now().strftime('%Y-%m-%d')
        
        if selected_date == today:
            self.date_label.configure(text="Data: Hoje")
        else:
            # Formatar data para exibição
            try:
                date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d/%m/%Y')
                self.date_label.configure(text=f"Data: {formatted_date}")
            except:
                self.date_label.configure(text=f"Data: {selected_date}")
    
    def set_toggle_editor_mode_callback(self, callback):
        """Definir callback para alternar modo editor"""
        self.toggle_editor_callback = callback
