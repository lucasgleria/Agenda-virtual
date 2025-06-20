import tkinter as tk
from tkinter import ttk

class FilterPanel:
    def __init__(self, parent, on_apply_filters):
        self.on_apply_filters = on_apply_filters

        self.frame = ttk.LabelFrame(parent, text="Filtros e Busca", padding=(15, 10))
        self.frame.pack(fill='x', pady=(0, 10))

        # --- Linha 1: Nome e Status ---
        row1 = ttk.Frame(self.frame)
        row1.pack(fill='x')

        ttk.Label(row1, text="Nome/Descrição:").pack(side='left', padx=(0, 5))
        self.nome_var = tk.StringVar()
        self.nome_entry = ttk.Entry(row1, textvariable=self.nome_var, width=30)
        self.nome_entry.pack(side='left', padx=5, expand=True, fill='x')

        ttk.Label(row1, text="Status:").pack(side='left', padx=(10, 5))
        self.status_var = tk.StringVar(value="Todos")
        self.status_combo = ttk.Combobox(row1, textvariable=self.status_var, values=["Todos", "pendente", "concluída", "cancelada"], state="readonly")
        self.status_combo.pack(side='left', padx=5)
        
        # --- Linha 2: Tipo e Botões ---
        row2 = ttk.Frame(self.frame)
        row2.pack(fill='x', pady=(5, 0))

        ttk.Label(row2, text="Tipo:").pack(side='left', padx=(0, 5))
        self.tipo_var = tk.StringVar(value="Todos")
        self.tipo_combo = ttk.Combobox(row2, textvariable=self.tipo_var, values=["Todos", "Tarefa", "Evento", "Agendamento"], state="readonly")
        self.tipo_combo.pack(side='left', padx=5)

        # Frame para botões à direita
        button_frame = ttk.Frame(row2)
        button_frame.pack(side='right')

        self.apply_button = ttk.Button(button_frame, text="Filtrar", command=self.apply)
        self.apply_button.pack(side='left', padx=5)

        self.clear_button = ttk.Button(button_frame, text="Limpar", command=self.clear)
        self.clear_button.pack(side='left')

    def apply(self):
        filters = {
            'nome': self.nome_var.get().strip(),
            'status': self.status_var.get(),
            'tipo': self.tipo_var.get()
        }
        self.on_apply_filters(filters)

    def clear(self):
        self.nome_var.set("")
        self.status_var.set("Todos")
        self.tipo_var.set("Todos")
        self.apply() 