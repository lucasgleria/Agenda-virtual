import tkinter as tk
from tkinter import ttk
from model.priority_flag import PriorityFlag
from view.theme.colors import ColorPalette

class FilterPanel:
    def __init__(self, parent, on_apply_filters):
        self.on_apply_filters = on_apply_filters
        self.filters = {}

        # Frame principal
        self.frame = ttk.LabelFrame(parent, text="🔍 Filtros", padding=10)

        # Grid para organizar os campos
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)

        # Linha 1: Prioridade e Status
        ttk.Label(self.frame, text="Prioridade:", 
                 font=("Segoe UI", 10, "bold"),
                 foreground=ColorPalette.TEXT['primary']).grid(
            row=0, column=0, sticky="w", pady=(0, 5))
        
        self.priority_var = tk.StringVar()
        self.priority_combo = ttk.Combobox(self.frame, textvariable=self.priority_var,
                                          values=["Todas"] + [p.value for p in PriorityFlag], 
                                          state="readonly", font=("Segoe UI", 9))
        self.priority_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=(0, 10))
        self.priority_combo.current(0)
        
        ttk.Label(self.frame, text="Status:", 
                 font=("Segoe UI", 10, "bold"),
                 foreground=ColorPalette.TEXT['primary']).grid(
            row=0, column=2, sticky="w", padx=(10, 0), pady=(0, 5))
        
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(self.frame, textvariable=self.status_var,
                                        values=["Todos", "Pendente", "Concluída"], 
                                        state="readonly", font=("Segoe UI", 9))
        self.status_combo.grid(row=0, column=3, sticky="ew", padx=(10, 0), pady=(0, 10))
        self.status_combo.current(0)
        
        # Linha 2: Nome e Tipo
        ttk.Label(self.frame, text="Nome:", 
                 font=("Segoe UI", 10, "bold"),
                 foreground=ColorPalette.TEXT['primary']).grid(
            row=1, column=0, sticky="w", pady=(0, 5))
        
        self.nome_var = tk.StringVar()
        self.nome_entry = ttk.Entry(self.frame, textvariable=self.nome_var, 
                                   font=("Segoe UI", 10))
        self.nome_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(0, 10))
        self.nome_entry.insert(0, "Digite o nome...")
        self.nome_entry.bind("<FocusIn>", self._on_nome_focus_in)
        self.nome_entry.bind("<FocusOut>", self._on_nome_focus_out)
        
        ttk.Label(self.frame, text="Tipo:", 
                 font=("Segoe UI", 10, "bold"),
                 foreground=ColorPalette.TEXT['primary']).grid(
            row=1, column=2, sticky="w", padx=(10, 0), pady=(0, 5))
        
        self.tipo_var = tk.StringVar()
        self.tipo_combo = ttk.Combobox(self.frame, textvariable=self.tipo_var,
                                      values=["Todos", "Tarefa", "Evento", "Agendamento"], 
                                      state="readonly", font=("Segoe UI", 9))
        self.tipo_combo.grid(row=1, column=3, sticky="ew", padx=(10, 0), pady=(0, 10))
        self.tipo_combo.current(0)
        
        # Linha 3: Botões
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(10, 0))
        
        self.apply_button = ttk.Button(button_frame, text="🔍 Aplicar Filtros", 
                                      command=self._apply_filters,
                                      style="Primary.TButton")
        self.apply_button.pack(side="left", padx=(0, 10))

        self.clear_button = ttk.Button(button_frame, text="🗑️ Limpar Filtros", 
                                      command=self._clear_filters)
        self.clear_button.pack(side="left")
        
        # Bindings
        self.priority_combo.bind("<<ComboboxSelected>>", self._on_filter_change)
        self.status_combo.bind("<<ComboboxSelected>>", self._on_filter_change)
        self.tipo_combo.bind("<<ComboboxSelected>>", self._on_filter_change)
        self.nome_entry.bind("<KeyRelease>", self._on_filter_change)
    
    def _on_nome_focus_in(self, event):
        """Quando o entry de nome recebe foco"""
        if self.nome_entry.get() == "Digite o nome...":
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.configure(foreground=ColorPalette.TEXT['primary'])
    
    def _on_nome_focus_out(self, event):
        """Quando o entry de nome perde foco"""
        if not self.nome_entry.get():
            self.nome_entry.insert(0, "Digite o nome...")
            self.nome_entry.configure(foreground=ColorPalette.TEXT['tertiary'])
    
    def _on_filter_change(self, event=None):
        """Callback para mudanças nos filtros"""
        self._apply_filters()
    
    def _apply_filters(self):
        """Aplicar filtros"""
        filters = {
            'nome': self.nome_var.get().strip() if self.nome_var.get() != "Digite o nome..." else "",
            'status': self.status_var.get(),
            'priority': self.priority_var.get(),
            'tipo': self.tipo_var.get()
        }
        self.on_apply_filters(filters)

    def _clear_filters(self):
        """Limpar todos os filtros"""
        self.nome_var.set("")
        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, "Digite o nome...")
        self.nome_entry.configure(foreground=ColorPalette.TEXT['tertiary'])
        
        self.status_var.set("Todos")
        self.priority_var.set("Todas")
        self.tipo_var.set("Todos")
        
        self._apply_filters()
    
    def update_results_count(self, count):
        """Atualizar contador de resultados"""
        pass  # Removido o results_label, então apenas pass
    
    def get_current_filters(self):
        """Obter filtros atuais"""
        filters = {}
        
        if self.nome_var.get() and self.nome_var.get() != "Digite o nome...":
            filters['nome'] = self.nome_var.get().strip()
        
        if self.status_var.get() != "Todos":
            filters['status'] = self.status_var.get()
        
        if self.priority_var.get() != "Todas":
            filters['priority'] = self.priority_var.get()
        
        if self.tipo_var.get() != "Todos":
            filters['tipo'] = self.tipo_var.get()
        
        return filters 