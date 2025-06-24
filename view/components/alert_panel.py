import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
from collections import defaultdict
from typing import List, Optional, Callable
from model.evento import Evento
from model.task import Task
from view.theme.colors import ColorPalette, StatusColors

class AlertPanel(ttk.Frame):
    """Painel para exibir alertas e notificações."""
    
    def __init__(self, parent, controller, **kwargs):
        print("[AlertPanel] Iniciando criação...")
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.alerts: List[dict] = []
        self.filtered_alerts: List[dict] = []
        self.selected_alert: Optional[dict] = None
        print("[AlertPanel] Configurando UI...")
        self._setup_ui()
        print("[AlertPanel] Criação concluída")
    
    def _setup_ui(self):
        """Configurar interface do usuário."""
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="📅 Agendamentos", 
                               font=("Arial", 14, "bold"),
                               foreground=ColorPalette.TEXT['primary'])
        title_label.pack(side=tk.LEFT)
        
        # Botões de ação
        button_frame = ttk.Frame(title_frame)
        button_frame.pack(side=tk.RIGHT)
        
        self.refresh_button = ttk.Button(button_frame, text="🔄 Atualizar", 
                                        command=self._refresh_alerts)
        self.refresh_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_button = ttk.Button(button_frame, text="🗑️ Limpar Todos", 
                                      command=self._clear_all_alerts)
        self.clear_button.pack(side=tk.LEFT)
        
        # Filtros
        filter_frame = ttk.LabelFrame(main_frame, text="Filtros", padding=10)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Filtro por tipo
        type_frame = ttk.Frame(filter_frame)
        type_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(type_frame, text="Tipo:", 
                 foreground=ColorPalette.TEXT['primary']).pack(side=tk.LEFT)
        self.type_var = tk.StringVar(value="Todos")
        type_combo = ttk.Combobox(type_frame, textvariable=self.type_var, 
                                 values=["Todos"], 
                                 state="readonly", width=15)
        type_combo.pack(side=tk.LEFT, padx=(5, 0))
        type_combo.bind("<<ComboboxSelected>>", self._apply_filters)
        
        # Filtro por urgência
        urgency_frame = ttk.Frame(filter_frame)
        urgency_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(urgency_frame, text="Urgência:", 
                 foreground=ColorPalette.TEXT['primary']).pack(side=tk.LEFT)
        self.urgency_var = tk.StringVar(value="Todas")
        urgency_combo = ttk.Combobox(urgency_frame, textvariable=self.urgency_var, 
                                    values=["Todas", "Urgente", "Importante", "Normal"], 
                                    state="readonly", width=15)
        urgency_combo.pack(side=tk.LEFT, padx=(5, 0))
        urgency_combo.bind("<<ComboboxSelected>>", self._apply_filters)
        
        # Busca
        search_frame = ttk.Frame(filter_frame)
        search_frame.pack(fill=tk.X)
        
        ttk.Label(search_frame, text="Buscar:", 
                 foreground=ColorPalette.TEXT['primary']).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.search_entry.bind("<KeyRelease>", self._apply_filters)
        
        # Estatísticas
        self.stats_frame = ttk.Frame(main_frame)
        self.stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.total_label = ttk.Label(self.stats_frame, text="Total: 0",
                                    foreground=ColorPalette.TEXT['primary'])
        self.total_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.urgent_label = ttk.Label(self.stats_frame, text="Urgentes: 0",
                                     foreground=ColorPalette.ERROR['main'])
        self.urgent_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.today_label = ttk.Label(self.stats_frame, text="Hoje: 0",
                                    foreground=ColorPalette.WARNING['main'])
        self.today_label.pack(side=tk.LEFT)
        
        # Treeview para alertas
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        columns = ("Tipo", "Título", "Data/Hora", "Urgência", "Descrição")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", 
                                 yscrollcommand=tree_scroll_y.set,
                                 xscrollcommand=tree_scroll_x.set)
        
        # Configurar colunas
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Data/Hora", text="Data/Hora")
        self.tree.heading("Urgência", text="Urgência")
        self.tree.heading("Descrição", text="Descrição")
        
        self.tree.column("Tipo", width=80, minwidth=60)
        self.tree.column("Título", width=150, minwidth=100)
        self.tree.column("Data/Hora", width=120, minwidth=100)
        self.tree.column("Urgência", width=100, minwidth=80)
        self.tree.column("Descrição", width=200, minwidth=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar scrollbars
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Bindings
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", self._on_double_click)
    
    def _apply_theme(self):
        """Aplicar tema atual aos componentes."""
        pass
    
    def update_alerts(self, events: List[Evento], agendamentos: List[Task]):
        """Atualizar lista de agendamentos."""
        self.alerts = []
        today = datetime.now()
        
        # Processar apenas agendamentos
        for agendamento in agendamentos:
            # Só processar se for um agendamento e estiver pendente
            if (agendamento.is_agendamento and not agendamento.is_evento and 
                agendamento.status != "concluída" and agendamento.date):
                
                # Converter data do agendamento para datetime (assumindo início do dia)
                agendamento_datetime = datetime.combine(agendamento.date, datetime.min.time())
                
                # Determinar urgência baseada na data
                time_diff = agendamento_datetime - today
                hours_until = time_diff.total_seconds() / 3600
                
                if hours_until > 0:  # Agendamentos futuros
                    urgency = "Urgente" if hours_until <= 2 else "Importante" if hours_until <= 12 else "Normal"
                    
                    self.alerts.append({
                        'type': 'Agendamento',
                        'title': agendamento.nome or agendamento.description,
                        'date_time': agendamento_datetime,
                        'urgency': urgency,
                        'description': f"Agendamento em {hours_until:.1f} horas: {agendamento.description}",
                        'item': agendamento
                    })
        
        # Ordenar por urgência e data
        self.alerts.sort(key=lambda x: (x['urgency'] == 'Urgente', x['date_time']))
        
        self._apply_filters()
    
    def _apply_filters(self, event=None):
        """Aplicar filtros à lista de agendamentos."""
        urgency_filter = self.urgency_var.get()
        search_text = self.search_var.get().lower()
        
        self.filtered_alerts = []
        
        for alert in self.alerts:
            # Filtro por urgência
            if urgency_filter != "Todas" and alert['urgency'] != urgency_filter:
                continue
                
            # Filtro por busca
            if search_text and search_text not in alert['title'].lower():
                continue
                
            self.filtered_alerts.append(alert)
        
        self._refresh_treeview()
        self._update_statistics()
    
    def _refresh_treeview(self):
        """Atualizar treeview com alertas filtrados."""
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar alertas filtrados com animação
        for i, alert in enumerate(self.filtered_alerts):
            item_id = self.tree.insert("", "end", values=(
                alert['type'],
                alert['title'],
                alert['date_time'].strftime("%d/%m/%Y %H:%M"),
                alert['urgency'],
                alert['description']
            ))
            
            # Aplicar cor baseada na urgência
            if alert['urgency'] == "Urgente":
                self.tree.tag_configure("urgent", background="#ffebee")
                self.tree.item(item_id, tags=("urgent",))
            elif alert['urgency'] == "Importante":
                self.tree.tag_configure("important", background="#fff3e0")
                self.tree.item(item_id, tags=("important",))
            
            # Animar entrada do item
            self._animate_item_entry(item_id, i)
    
    def _animate_item_entry(self, item_id: str, index: int):
        """Animar entrada de um item na lista."""
        def animate():
            try:
                if self.tree.exists(item_id):
                    # Destacar item temporariamente
                    self.tree.selection_set(item_id)
                    self.tree.see(item_id)
                    
                    # Remover seleção após animação
                    self.after(300, lambda: self._safe_remove_selection(item_id))
            except Exception as e:
                # Silenciar erros de animação
                pass
        
        # Delay baseado no índice para efeito cascata
        self.after(index * 50, animate)
    
    def _safe_remove_selection(self, item_id):
        """Remover seleção de forma segura, verificando se o item ainda existe"""
        try:
            if self.tree.exists(item_id):
                self.tree.selection_remove(item_id)
        except Exception:
            # Silenciar erros de remoção de seleção
            pass
    
    def _update_statistics(self):
        """Atualizar estatísticas do painel."""
        total = len(self.filtered_alerts)
        urgent = len([a for a in self.filtered_alerts if a['urgency'] == 'Urgente'])
        
        today = datetime.now().date()
        today_count = len([a for a in self.filtered_alerts if a['date_time'].date() == today])
        
        self.total_label.config(text=f"Total: {total}")
        self.urgent_label.config(text=f"Urgentes: {urgent}")
        self.today_label.config(text=f"Hoje: {today_count}")
    
    def _on_select(self, event):
        """Manipular seleção de item."""
        selection = self.tree.selection()
        if selection:
            item_id = selection[0]
            index = self.tree.index(item_id)
            if 0 <= index < len(self.filtered_alerts):
                self.selected_alert = self.filtered_alerts[index]
        else:
            self.selected_alert = None
    
    def _on_double_click(self, event):
        """Manipular duplo clique."""
        if self.selected_alert:
            # Abrir editor do item relacionado
            item = self.selected_alert['item']
            if self.selected_alert['type'] == 'Agendamento' and hasattr(self.controller, 'edit_task'):
                # Para agendamentos, precisamos da data e da tarefa
                date = item.date
                self.controller.edit_task(date, item)
    
    def _refresh_alerts(self):
        """Atualizar alertas."""
        # Notificar controller para atualizar dados
        if hasattr(self.controller, 'view') and hasattr(self.controller.view, 'update_view'):
            self.controller.view.update_view()
    
    def _clear_all_alerts(self):
        """Limpar todos os alertas."""
        if not self.filtered_alerts:
            messagebox.showinfo("Informação", "Não há alertas para limpar.")
            return
            
        # Confirmar limpeza
        result = messagebox.askyesno("Confirmar Limpeza", 
                                   f"Deseja realmente marcar todos os {len(self.filtered_alerts)} agendamentos como concluídos?\n\n"
                                   "Esta ação irá marcar os agendamentos como concluídos no sistema.")
        if result:
            self._perform_clear()
    
    def _perform_clear(self):
        """Executar limpeza dos alertas."""
        try:
            # Marcar todas as tarefas como concluídas no banco de dados
            tasks_marked = 0
            for alert in self.filtered_alerts:
                if alert['type'] == 'Agendamento' and 'item' in alert:
                    task = alert['item']
                    # Marcar a tarefa como concluída
                    if hasattr(self.controller, 'update_task_status'):
                        task_key = (task.date, task.description, task.nome)
                        self.controller.update_task_status(task_key, True)
                        tasks_marked += 1
            
            # Limpar a lista de alertas filtrados
            self.filtered_alerts = []
            
            # Atualizar a interface
            self._refresh_treeview()
            self._update_statistics()
            
            # Mostrar mensagem de sucesso
            if tasks_marked > 0:
                messagebox.showinfo("Sucesso", 
                                  f"{tasks_marked} agendamento(s) marcado(s) como concluído(s) com sucesso!")
            
            # Atualizar dados na view principal
            if hasattr(self.controller, 'view') and hasattr(self.controller.view, 'update_view'):
                self.controller.view.update_view()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao limpar alertas: {str(e)}")
            print(f"Erro ao limpar alertas: {e}")
    
    def refresh(self):
        """Atualizar painel."""
        self._apply_filters()
