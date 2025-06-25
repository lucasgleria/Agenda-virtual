import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class EditorPanel:
    def __init__(self, parent, on_edit, on_delete):
        self.on_edit = on_edit
        self.on_delete = on_delete

        # Frame principal com design moderno
        self.frame = ttk.LabelFrame(parent, text="✏️ Modo Editor", padding=15)
        self.frame.pack(fill='both', expand=True, padx=15, pady=5)
        self.task_frame = ttk.Frame(self.frame)
        self.task_frame.pack(fill='both', expand=True)
        
        # Configurar grid weights para responsividade
        self.task_frame.grid_columnconfigure(0, weight=1)
        self.task_frame.grid_rowconfigure(0, weight=1)
        
        # Canvas para scroll dos cards
        self.canvas = tk.Canvas(self.task_frame, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.task_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configurar grid weights no frame scrollável
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_width())
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind para redimensionar o conteúdo quando o canvas for redimensionado
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Empacotar canvas e scrollbar usando grid para melhor controle
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind mouse wheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Header do editor
        self.header_frame = ttk.Frame(self.frame)
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        self.title_label = ttk.Label(self.header_frame, text="📝 Editar Tarefas", 
                                    font=("Segoe UI", 14, "bold"))
        self.title_label.pack(side="left")
        
        self.count_label = ttk.Label(self.header_frame, text="(0 tarefas)", 
                                    font=("Segoe UI", 11), foreground="gray")
        self.count_label.pack(side="left", padx=(10, 0))

    def _on_canvas_configure(self, event):
        """Redimensionar o conteúdo do canvas quando ele for redimensionado"""
        # Atualizar a largura do frame scrollável para ocupar toda a largura do canvas
        self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=event.width)

    def _on_mousewheel(self, event):
        """Scroll do mouse para o canvas"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_editor_panel(self, date, tasks, visible):
        """Atualizar painel do editor com novas tarefas"""
        # Limpar widgets anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if visible:
            self.frame.pack(fill='both', expand=False, pady=5, padx=15)
        else:
            self.frame.pack_forget()
            return

        # Configurar grid weights no frame scrollável
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Atualizar contador
        self.count_label.configure(text=f"({len(tasks)} tarefas)")
        
        # Criar cards para cada tarefa
        for i, task in enumerate(tasks):
            self._create_task_editor_card(task, date, i)
        
        # Forçar atualização do canvas
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _create_task_editor_card(self, task, date, index):
        """Criar um card de edição para uma tarefa que ocupa todo o espaço disponível"""
        # Frame principal do card
        card_frame = ttk.Frame(self.scrollable_frame, style="EditorCard.TFrame")
        card_frame.grid(row=index, column=0, sticky="ew", padx=10, pady=5)
        card_frame.grid_columnconfigure(0, weight=1)
        
        # Determinar tipo e ícones
        if getattr(task, 'is_evento', False):
            task_type = "📅 Evento"
            type_color = "#007bff"
        elif getattr(task, 'is_agendamento', False):
            task_type = "📋 Agendamento"
            type_color = "#28a745"
        else:
            task_type = "📝 Tarefa"
            type_color = "#6c757d"
        
        # Status da tarefa
        is_completed = getattr(task, 'completed', False)
        status_icon = "✅" if is_completed else "⏳"
        status_text = "Concluída" if is_completed else "Pendente"
        status_color = "#28a745" if is_completed else "#fd7e14"
        
        # Header do card
        header_frame = ttk.Frame(card_frame)
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Informações principais
        info_frame = ttk.Frame(header_frame)
        info_frame.grid(row=0, column=0, sticky="ew")
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Título da tarefa
        title_text = getattr(task, 'description', 'Sem descrição')
        title_label = ttk.Label(info_frame, text=title_text, 
                               font=("Segoe UI", 12, "bold"),
                               foreground="gray" if is_completed else "black",
                               wraplength=400)  # Permitir quebra de linha
        title_label.grid(row=0, column=0, sticky="ew")
        
        # Informações secundárias
        details_frame = ttk.Frame(info_frame)
        details_frame.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        details_frame.grid_columnconfigure(1, weight=1)
        
        # Tipo
        type_label = ttk.Label(details_frame, text=task_type, 
                              font=("Segoe UI", 10), foreground=type_color)
        type_label.grid(row=0, column=0, padx=(0, 15))
        
        # Status
        status_label = ttk.Label(details_frame, text=f"{status_icon} {status_text}", 
                                font=("Segoe UI", 10), foreground=status_color)
        status_label.grid(row=0, column=1, padx=(0, 15))
        
        # Data
        date_text = getattr(task, 'date', 'N/A')
        if date_text != 'N/A':
            date_label = ttk.Label(details_frame, text=f"📅 {date_text}", 
                                  font=("Segoe UI", 10), foreground="gray")
            date_label.grid(row=0, column=2)
        
        # Nome (se houver)
        nome = getattr(task, 'nome', None)
        if nome:
            nome_frame = ttk.Frame(info_frame)
            nome_frame.grid(row=2, column=0, sticky="ew", pady=(5, 0))
            nome_label = ttk.Label(nome_frame, text=f"👤 {nome}", 
                                  font=("Segoe UI", 10), foreground="gray")
            nome_label.grid(row=0, column=0, sticky="w")
        
        # Ações do card
        actions_frame = ttk.Frame(header_frame)
        actions_frame.grid(row=0, column=1, padx=(10, 0))
        
        # Botão de editar
        edit_btn = ttk.Button(actions_frame, text="✏️ Editar", 
                             command=lambda t=task: self._edit_task(date, t),
                             style="Accent.TButton")
        edit_btn.grid(row=0, column=0, pady=(0, 5))
        
        # Botão de excluir
        delete_btn = ttk.Button(actions_frame, text="🗑️ Excluir", 
                               command=lambda t=task: self._delete_task(date, t),
                               style="Danger.TButton")
        delete_btn.grid(row=1, column=0)
        
        # Aplicar estilo baseado no status
        if is_completed:
            card_frame.configure(style="CompletedEditorCard.TFrame")
        
        # Animar entrada do card
        self._animate_card_entry(card_frame, index)
        
        return card_frame
    
    def _animate_card_entry(self, card, index):
        """Animar entrada de um card no layout de grid"""
        # Configurar posição inicial
        card.grid_configure(pady=(0, 5))
        
        # Animar entrada com delay
        def animate():
            try:
                # Verificar se o card ainda existe antes de tentar animá-lo
                if card.winfo_exists():
                    card.grid_configure(pady=(5, 5))
            except Exception as e:
                # Silenciar erros de animação quando o widget foi destruído
                pass
        
        # Agendar animação
        self.frame.after(index * 50, animate)
    
    def _edit_task(self, date, task):
        """Editar uma tarefa"""
        if self.on_edit:
            self.on_edit(date, task)
    
    def _delete_task(self, date, task):
        """Excluir uma tarefa"""
        task_name = getattr(task, 'description', 'Tarefa')
        if messagebox.askyesno("Confirmar Exclusão", 
                              f"Deseja realmente excluir a tarefa '{task_name}'?"):
            if self.on_delete:
                self.on_delete(date, task)
