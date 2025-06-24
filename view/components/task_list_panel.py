import tkinter as tk
from tkinter import ttk, messagebox
from model.priority_flag import PriorityFlag
from datetime import datetime, timedelta
import threading
from typing import List, Optional, Callable
from model.task import Task
from view.theme.colors import ColorPalette, PriorityColors, StatusColors

class TaskListPanel(ttk.Frame):
    # Nova paleta de cores moderna
    PRIORITY_COLORS = {
        PriorityFlag.MUITO_IMPORTANTE.value: ColorPalette.ERROR['main'],      # Vermelho moderno
        PriorityFlag.IMPORTANTE.value: ColorPalette.WARNING['main'],          # Laranja moderno
        PriorityFlag.MEDIA.value: ColorPalette.SECONDARY['main'],             # Roxo moderno
        PriorityFlag.SIMPLES.value: ColorPalette.SUCCESS['main'],             # Verde moderno
        "EVENTO": ColorPalette.PRIMARY['main'],                               # Azul moderno
        "GERAL": ColorPalette.NEUTRAL['gray_600']                             # Cinza moderno
    }
    
    PRIORITY_ICONS = {
        PriorityFlag.MUITO_IMPORTANTE.value: "🔴",
        PriorityFlag.IMPORTANTE.value: "🟠",
        PriorityFlag.MEDIA.value: "🟡",
        PriorityFlag.SIMPLES.value: "🟢",
        "EVENTO": "📅",
        "GERAL": "⚪"
    }

    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.tasks: List[Task] = []
        self.filtered_tasks: List[Task] = []
        self.current_filter = {}
        self.animation_running = False
        self.selected_task: Optional[Task] = None
        self.view_mode = "cards"  # "cards" ou "list"
        
        # Configurar grid weights para responsividade
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._create_widgets()
        self._load_tasks()
        
    def _create_widgets(self):
        """Criar widgets do painel com design moderno"""
        # Header com título, botões e toggle de visualização
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        # Título com ícone e animação
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side="left")
        
        self.title_label = ttk.Label(title_frame, text="📋 Lista de Tarefas", 
                                    font=("Segoe UI", 18, "bold"),
                                    foreground=ColorPalette.TEXT['primary'])
        self.title_label.pack(side=tk.LEFT)
        
        # Contador de tarefas
        self.counter_label = ttk.Label(title_frame, text="(0 tarefas)", 
                                      font=("Segoe UI", 12), 
                                      foreground=ColorPalette.TEXT['secondary'])
        self.counter_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Frame para controles
        controls_frame = ttk.Frame(header_frame)
        controls_frame.pack(side="right")
        
        # Toggle de visualização
        view_frame = ttk.Frame(controls_frame)
        view_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Label(view_frame, text="Visualização:", 
                 foreground=ColorPalette.TEXT['secondary']).pack(side=tk.LEFT)
        self.view_var = tk.StringVar(value="cards")
        view_combo = ttk.Combobox(view_frame, textvariable=self.view_var, 
                                 values=["cards", "lista"], state="readonly", width=8)
        view_combo.pack(side=tk.LEFT, padx=(5, 0))
        view_combo.bind("<<ComboboxSelected>>", self._toggle_view_mode)
        
        # Botões de ação
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.add_btn = ttk.Button(button_frame, text="➕ Nova Tarefa", 
                                 command=self._add_task, style="Accent.TButton")
        self.add_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.refresh_btn = ttk.Button(button_frame, text="🔄 Atualizar", 
                                     command=self._refresh_tasks)
        self.refresh_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Frame principal para conteúdo
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Criar ambos os modos de visualização
        self._create_cards_view()
        self._create_list_view()
        
        # Mostrar modo cards por padrão
        self._show_cards_view()
        
        # Frame para estatísticas
        self.stats_frame = ttk.Frame(self)
        self.stats_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Labels de estatísticas com ícones
        self.total_label = ttk.Label(self.stats_frame, text="📊 Total: 0", 
                                    font=("Segoe UI", 11),
                                    foreground=ColorPalette.TEXT['primary'])
        self.total_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.completed_label = ttk.Label(self.stats_frame, text="✅ Concluídas: 0", 
                                       font=("Segoe UI", 11), 
                                       foreground=ColorPalette.SUCCESS['main'])
        self.completed_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.pending_label = ttk.Label(self.stats_frame, text="⏳ Pendentes: 0", 
                                     font=("Segoe UI", 11), 
                                     foreground=ColorPalette.WARNING['main'])
        self.pending_label.pack(side=tk.LEFT)
        
    def _create_cards_view(self):
        """Criar visualização em cards"""
        self.cards_frame = ttk.Frame(self.content_frame)
        self.cards_frame.pack(fill="both", expand=True)
        
        # Canvas e scrollbar para cards
        self.cards_canvas = tk.Canvas(self.cards_frame, 
                                     bg=ColorPalette.BACKGROUND['primary'], 
                                     highlightthickness=0)
        self.cards_scrollbar = ttk.Scrollbar(self.cards_frame, orient="vertical", command=self.cards_canvas.yview)
        self.cards_scrollable_frame = ttk.Frame(self.cards_canvas)
        
        self.cards_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all"))
        )
        
        self.cards_canvas.create_window((0, 0), window=self.cards_scrollable_frame, anchor="nw")
        self.cards_canvas.configure(yscrollcommand=self.cards_scrollbar.set)
        
        # Empacotar canvas e scrollbar
        self.cards_canvas.pack(fill="both", expand=True)
        self.cards_scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        self.cards_canvas.bind("<MouseWheel>", self._on_mousewheel)
        
    def _create_list_view(self):
        """Criar visualização em lista (TreeView)"""
        self.list_frame = ttk.Frame(self.content_frame)
        self.list_frame.pack(fill="both", expand=True)
        
        # Treeview para lista de tarefas
        columns = ("Nome", "Status", "Tipo", "Prioridade", "Data Limite", "Ações")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Prioridade", text="Prioridade")
        self.tree.heading("Data Limite", text="Data Limite")
        self.tree.heading("Ações", text="Ações")
        
        # Configurar larguras das colunas
        self.tree.column("Nome", width=200, minwidth=150)
        self.tree.column("Status", width=100, minwidth=80)
        self.tree.column("Tipo", width=100, minwidth=80)
        self.tree.column("Prioridade", width=120, minwidth=100)
        self.tree.column("Data Limite", width=120, minwidth=100)
        self.tree.column("Ações", width=150, minwidth=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empacotar treeview e scrollbar
        self.tree.pack(fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bindings para eventos
        self.tree.bind("<Double-1>", self._on_item_double_click)
        self.tree.bind("<Button-1>", self._on_item_click)
        
    def _toggle_view_mode(self, event=None):
        """Alternar entre modos de visualização"""
        if self.view_var.get() == "cards":
            self._show_cards_view()
        else:
            self._show_list_view()
        self._update_task_list()
        
    def _show_cards_view(self):
        """Mostrar visualização em cards"""
        self.list_frame.pack_forget()
        self.cards_frame.pack(fill="both", expand=True)
        
    def _show_list_view(self):
        """Mostrar visualização em lista"""
        self.cards_frame.pack_forget()
        self.list_frame.pack(fill="both", expand=True)
        
    def _create_task_card(self, task, index):
        """Criar um card visual para uma tarefa"""
        # Determinar cores baseadas na prioridade
        if task.priority is None:
            priority_color = PriorityColors.get_color('GERAL', 'main')
            priority_bg = PriorityColors.get_color('GERAL', 'background')
            priority_border = PriorityColors.get_color('GERAL', 'border')
        else:
            priority_color = PriorityColors.get_color(task.priority.value, 'main')
            priority_bg = PriorityColors.get_color(task.priority.value, 'background')
            priority_border = PriorityColors.get_color(task.priority.value, 'border')
        
        # Status da tarefa
        is_completed = hasattr(task, 'completed') and task.completed
        status_color = StatusColors.get_color('completed' if is_completed else 'pending', 'main')
        
        # Criar frame do card com bordas arredondadas e sombra
        card = tk.Frame(self.cards_scrollable_frame, 
                       bg=ColorPalette.BACKGROUND['card'],
                       relief="flat", 
                       bd=1,
                       highlightbackground=priority_border,
                       highlightthickness=1)
        
        # Configurar grid do card
        card.grid_columnconfigure(1, weight=1)
        
        # Header do card com prioridade e status
        header_frame = tk.Frame(card, bg=priority_bg, height=30)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=(5, 0))
        header_frame.grid_propagate(False)
        
        # Ícone de prioridade
        if task.priority is None:
            priority_icon = "⚪"
        else:
            priority_icon = "🔴" if task.priority.value == "MUITO_IMPORTANTE" else \
                           "🟠" if task.priority.value == "IMPORTANTE" else \
                           "🟡" if task.priority.value == "MEDIA" else "🟢"
        
        priority_label = tk.Label(header_frame, text=priority_icon, 
                                 bg=priority_bg, font=("Segoe UI", 12))
        priority_label.pack(side=tk.LEFT, padx=(10, 5))
        
        # Status da tarefa
        status_text = "✅ Concluída" if is_completed else "⏳ Pendente"
        status_label = tk.Label(header_frame, text=status_text, 
                               bg=priority_bg, 
                               fg=status_color,
                               font=("Segoe UI", 9, "bold"))
        status_label.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Conteúdo principal do card
        content_frame = tk.Frame(card, bg=ColorPalette.BACKGROUND['card'])
        content_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Título/Descrição da tarefa
        title_text = task.nome if task.nome else task.description
        title_label = tk.Label(content_frame, text=title_text, 
                              bg=ColorPalette.BACKGROUND['card'],
                              fg=ColorPalette.TEXT['primary'] if not is_completed else ColorPalette.TEXT['disabled'],
                              font=("Segoe UI", 12, "bold"),
                              anchor="w", justify=tk.LEFT)
        title_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        # Descrição (se diferente do nome)
        if task.nome and task.description:
            desc_label = tk.Label(content_frame, text=task.description, 
                                 bg=ColorPalette.BACKGROUND['card'],
                                 fg=ColorPalette.TEXT['secondary'],
                                 font=("Segoe UI", 10),
                                 anchor="w", justify=tk.LEFT)
            desc_label.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        # Informações adicionais
        info_frame = tk.Frame(content_frame, bg=ColorPalette.BACKGROUND['card'])
        info_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Data
        if task.date:
            date_text = task.date.strftime('%d/%m/%Y')
            date_label = tk.Label(info_frame, text=f"📅 {date_text}", 
                                 bg=ColorPalette.BACKGROUND['card'],
                                 fg=ColorPalette.TEXT['tertiary'],
                                 font=("Segoe UI", 9))
            date_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Tipo
        type_text = "📋 Tarefa" if not task.is_evento else "📅 Evento"
        type_label = tk.Label(info_frame, text=type_text, 
                             bg=ColorPalette.BACKGROUND['card'],
                             fg=ColorPalette.TEXT['tertiary'],
                             font=("Segoe UI", 9))
        type_label.pack(side=tk.LEFT)
        
        # Botões de ação
        actions_frame = tk.Frame(card, bg=ColorPalette.BACKGROUND['card'])
        actions_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 10))
        
        # Botão de toggle de conclusão
        toggle_text = "✅ Concluir" if not is_completed else "🔄 Reabrir"
        toggle_btn = tk.Button(actions_frame, text=toggle_text,
                              bg=status_color,
                              fg=ColorPalette.TEXT['inverse'],
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              command=lambda: self._toggle_task_completion(task))
        toggle_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botão de editar
        edit_btn = tk.Button(actions_frame, text="✏️ Editar",
                            bg=ColorPalette.PRIMARY['main'],
                            fg=ColorPalette.TEXT['inverse'],
                            font=("Segoe UI", 9),
                            relief="flat",
                             command=lambda: self._edit_task(task))
        edit_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botão de excluir
        delete_btn = tk.Button(actions_frame, text="🗑️ Excluir",
                              bg=ColorPalette.ERROR['main'],
                              fg=ColorPalette.TEXT['inverse'],
                              font=("Segoe UI", 9),
                              relief="flat",
                              command=lambda: self._delete_task(task))
        delete_btn.pack(side=tk.LEFT)
        
        # Configurar espaçamento entre cards usando pack
        card.pack(fill="x", padx=5, pady=5)
        
        return card
        
    def _on_mousewheel(self, event):
        """Scroll do mouse para o canvas"""
        self.cards_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _load_tasks(self):
        """Carregar tarefas do controller"""
        if self.controller:
            # Carregar tarefas da data atual
            current_date = datetime.now().strftime('%Y-%m-%d')
            self.tasks = self.controller.get_tasks_for_date(current_date)
            self.filtered_tasks = self.tasks.copy()
            self._update_task_list()
            self._update_statistics()
    
    def _update_task_list(self):
        """Atualizar a lista de tarefas no treeview e cards"""
        if self.view_var.get() == "cards":
            self._update_cards_view()
        else:
            self._update_list_view()
        
        self._update_statistics()
    
    def _update_cards_view(self):
        """Atualizar visualização em cards"""
        # Limpar cards existentes
        for widget in self.cards_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Criar cards para cada tarefa
        for i, task in enumerate(self.filtered_tasks):
            card = self._create_task_card(task, i)
            # Adicionar animação de entrada
            self._animate_card_entry(card, i)
    
    def _update_list_view(self):
        """Atualizar a lista de tarefas no treeview"""
        # Limpar lista atual
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar tarefas filtradas
        for i, task in enumerate(self.filtered_tasks):
            # Preparar dados da tarefa
            name = getattr(task, 'description', 'Sem descrição')
            status = "✅ Concluída" if getattr(task, 'status', 'pendente') == 'concluída' else "⏳ Pendente"
            
            # Determinar tipo
            if getattr(task, 'is_evento', False):
                task_type = "📅 Evento"
            elif getattr(task, 'is_agendamento', False):
                task_type = "📋 Agendamento"
            else:
                task_type = "📝 Tarefa"
            
            # Prioridade
            priority = getattr(task, 'priority', None)
            if priority and hasattr(priority, 'value'):
                priority_text = priority.value
            else:
                priority_text = "Normal"
            
            # Data limite
            date_limit = getattr(task, 'date', 'N/A')
            
            # Inserir no treeview
            item_id = self.tree.insert("", "end", values=(
                name, status, task_type, priority_text, date_limit, "Editar | Excluir"
            ))
            
            # Aplicar cor baseada na prioridade
            if priority and hasattr(priority, 'value'):
                color = self.PRIORITY_COLORS.get(priority.value, ColorPalette.NEUTRAL['gray_600'])
                self.tree.tag_configure(color, foreground=color)
                self.tree.item(item_id, tags=(color,))
            else:
                # Usar cor padrão para prioridades nulas
                color = ColorPalette.NEUTRAL['gray_600']
                self.tree.tag_configure(color, foreground=color)
                self.tree.item(item_id, tags=(color,))
    
    def _animate_card_entry(self, card, index):
        """Animar entrada de um card"""
        # Configurar posição inicial (fora da tela)
        card.pack_configure(pady=(0, 5))
        
        # Animar entrada com delay baseado no índice
        def animate():
            try:
                # Verificar se o card ainda existe antes de tentar animá-lo
                if card.winfo_exists():
                    card.pack_configure(pady=(5, 5))
            except Exception as e:
                # Silenciar erros de animação quando o widget foi destruído
                pass
        
        # Agendar animação
        self.after(index * 50, animate)
    
    def _toggle_task_completion(self, task):
        """Alternar status de conclusão de uma tarefa"""
        if self.controller:
            # Usar o atributo correto 'status' em vez de 'completed'
            current_status = getattr(task, 'status', 'pendente') == 'concluída'
            print(f"[DEBUG] Tentando alternar tarefa: {getattr(task, 'description', 'N/A')}")
            print(f"[DEBUG] Status atual: {current_status}")
            print(f"[DEBUG] Task object: {task}")
            print(f"[DEBUG] Task attributes: date={getattr(task, 'date', 'N/A')}, description={getattr(task, 'description', 'N/A')}, nome={getattr(task, 'nome', 'N/A')}")
            print(f"[DEBUG] Task status: {getattr(task, 'status', 'N/A')}")
            
            # Usar o método correto do controller
            task_key = (getattr(task, 'date', datetime.now().strftime('%Y-%m-%d')), 
                       getattr(task, 'description', ''), 
                       getattr(task, 'nome', ''))
            print(f"[DEBUG] Task key: {task_key}")
            
            try:
                self.controller.update_task_status(task_key, not current_status)
                print(f"[DEBUG] Método update_task_status chamado com sucesso")
                self._update_task_list()
                print(f"[DEBUG] Lista atualizada")
                
                # Feedback visual
                task_name = getattr(task, 'nome', '') or getattr(task, 'description', 'Tarefa')
                status = "concluída" if not current_status else "reaberta"
                print(f"✅ Tarefa '{task_name}' marcada como {status}!")
                    
            except Exception as e:
                print(f"[DEBUG] Erro ao atualizar status: {e}")
                print(f"❌ Erro ao alterar status da tarefa: {str(e)}")
        else:
            print("[DEBUG] Controller não disponível")
    
    def _edit_task(self, task):
        """Editar uma tarefa específica"""
        if self.controller:
            try:
                date = getattr(task, 'date', datetime.now().strftime('%Y-%m-%d'))
                self.controller.edit_task(date, task)
                
                # Feedback visual
                task_name = getattr(task, 'nome', '') or getattr(task, 'description', 'Tarefa')
                print(f"ℹ️ Editando tarefa '{task_name}'...")
                    
            except Exception as e:
                print(f"❌ Erro ao editar tarefa: {str(e)}")
    
    def _delete_task(self, task):
        """Excluir uma tarefa específica"""
        if self.controller:
            try:
                date = getattr(task, 'date', datetime.now().strftime('%Y-%m-%d'))
                task_name = getattr(task, 'nome', '') or getattr(task, 'description', 'Tarefa')
                
                # Confirmação antes de excluir
                if messagebox.askyesno("Confirmar Exclusão", 
                                      f"Deseja realmente excluir a tarefa '{task_name}'?"):
                    self.controller.delete_task(date, task)
                    self._update_task_list()
                    print(f"✅ Tarefa '{task_name}' excluída com sucesso!")
                        
            except Exception as e:
                print(f"❌ Erro ao excluir tarefa: {str(e)}")
    
    def _update_statistics(self):
        """Atualizar estatísticas do painel"""
        total = len(self.filtered_tasks)
        completed = len([t for t in self.filtered_tasks if getattr(t, 'status', 'pendente') == 'concluída'])
        pending = total - completed
        
        self.counter_label.configure(text=f"({total} tarefas)")
        self.total_label.configure(text=f"📊 Total: {total}")
        self.completed_label.configure(text=f"✅ Concluídas: {completed}")
        self.pending_label.configure(text=f"⏳ Pendentes: {pending}")
    
    def _on_item_double_click(self, event):
        """Callback para duplo clique em item da lista"""
        if self.view_var.get() == "lista":
            item = self.tree.selection()
            if item:
                item_id = item[0]
                values = self.tree.item(item_id, "values")
                if values:
                    # Encontrar tarefa correspondente
                    task_name = values[0]
                    for task in self.filtered_tasks:
                        if getattr(task, 'description', '') == task_name:
                            self._edit_task(task)
                            break
    
    def _on_item_click(self, event):
        """Callback para clique em item da lista"""
        if self.view_var.get() == "lista":
            item = self.tree.selection()
            if item:
                item_id = item[0]
                values = self.tree.item(item_id, "values")
                if values:
                    task_name = values[0]
                    for task in self.filtered_tasks:
                        if getattr(task, 'description', '') == task_name:
                            self.selected_task = task
                            break
    
    def _add_task(self):
        """Adicionar nova tarefa"""
        if self.controller:
            # Simular adição de tarefa (será tratada pelo calendar panel)
            print("Adicionar nova tarefa - redirecionando para calendar panel")
    
    def _refresh_tasks(self):
        """Atualizar lista de tarefas"""
        self._load_tasks()
    
    def apply_filter(self, filter_params):
        """Aplicar filtros às tarefas."""
        self.current_filter = filter_params
        self.filtered_tasks = []
        
        for task in self.tasks:
            # Filtrar apenas tarefas (não eventos, não agendamentos)
            if not getattr(task, 'is_tarefa', True):
                continue
            
            # Filtro por nome/descrição
            if filter_params.get('nome'):
                search_term = filter_params['nome'].lower()
                task_desc = getattr(task, 'description', '').lower()
                task_nome = getattr(task, 'nome', '').lower()
                if search_term not in task_desc and search_term not in task_nome:
                    continue
            
            # Filtro por status
            if filter_params.get('status') and filter_params['status'] != "Todos":
                task_completed = getattr(task, 'status', 'pendente') == 'concluída'
                if filter_params['status'] == "concluída" and not task_completed:
                    continue
                elif filter_params['status'] == "pendente" and task_completed:
                    continue
            
            # Filtro por tipo (removido, pois agora só mostra tarefas)
            # if filter_params.get('tipo') and filter_params['tipo'] != "Todos":
            #     task_is_evento = getattr(task, 'is_evento', False)
            #     task_is_agendamento = getattr(task, 'is_agendamento', False)
            #     
            #     if filter_params['tipo'] == "Evento" and not task_is_evento:
            #         continue
            #     elif filter_params['tipo'] == "Agendamento" and not task_is_agendamento:
            #         continue
            #     elif filter_params['tipo'] == "Tarefa" and (task_is_evento or task_is_agendamento):
            #         continue
            
            self.filtered_tasks.append(task)
        
        self._update_task_list()
    
    def refresh_theme(self):
        """Atualizar tema do painel"""
        pass
    
    def update_task_list(self, date, tasks):
        """Atualizar lista de tarefas com novas tarefas"""
        self.tasks = tasks
        self.filtered_tasks = tasks.copy()
        self._update_task_list()
    
    def set_controller(self, controller):
        """Definir controller do painel"""
        self.controller = controller
        self._load_tasks()
    
    def update_tasks(self, tasks: List[Task]):
        """Atualizar tarefas do painel"""
        self.tasks = tasks
        self.filtered_tasks = tasks.copy()
        self._update_task_list()
    
    def refresh(self):
        """Atualizar painel"""
        self._load_tasks()