import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from typing import List, Optional, Callable
from model.evento import Evento
from model.task import Task
from view.theme.colors import ColorPalette

class EventPanel(ttk.Frame):
    """Painel para exibir e gerenciar eventos."""
    
    def __init__(self, parent, controller, **kwargs):
        print("[EventPanel] Iniciando criação...")
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.events: List[Evento] = []
        self.filtered_events: List[Evento] = []
        self.selected_event: Optional[Evento] = None
        print("[EventPanel] Configurando UI...")
        self._setup_ui()
        print("[EventPanel] Criação concluída")
    
    def _setup_ui(self):
        """Configurar interface do usuário."""
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="📅 Eventos", 
                               font=("Arial", 14, "bold"),
                               foreground=ColorPalette.TEXT['primary'])
        title_label.pack(side=tk.LEFT)
        
        # Botões de ação
        button_frame = ttk.Frame(title_frame)
        button_frame.pack(side=tk.RIGHT)
        
        self.refresh_button = ttk.Button(button_frame, text="🔄 Atualizar", 
                                     command=self.refresh, state="normal")
        self.refresh_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.delete_button = ttk.Button(button_frame, text="🗑️ Excluir", 
                                       command=self._delete_event, state="disabled")
        self.delete_button.pack(side=tk.LEFT)
        
        # Filtros
        filter_frame = ttk.LabelFrame(main_frame, text="Filtros", padding=10)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Filtro por período
        period_frame = ttk.Frame(filter_frame)
        period_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(period_frame, text="Período:").pack(side=tk.LEFT)
        self.period_var = tk.StringVar(value="Todos")
        period_combo = ttk.Combobox(period_frame, textvariable=self.period_var, 
                                   values=["Todos", "Hoje", "Esta Semana", "Este Mês", "Próximos 7 dias"], 
                                   state="readonly", width=15)
        period_combo.pack(side=tk.LEFT, padx=(5, 0))
        period_combo.bind("<<ComboboxSelected>>", self._apply_filters)
        
        # Filtro por tipo
        type_frame = ttk.Frame(filter_frame)
        type_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(type_frame, text="Status:").pack(side=tk.LEFT)
        self.status_var = tk.StringVar(value="Todos")
        status_combo = ttk.Combobox(type_frame, textvariable=self.status_var, 
                                   values=["Todos", "Ativo", "Inativo"], 
                                 state="readonly", width=15)
        status_combo.pack(side=tk.LEFT, padx=(5, 0))
        status_combo.bind("<<ComboboxSelected>>", self._apply_filters)
        
        # Busca
        search_frame = ttk.Frame(filter_frame)
        search_frame.pack(fill=tk.X)
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
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
        
        self.today_label = ttk.Label(self.stats_frame, text="Hoje: 0")
        self.today_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.week_label = ttk.Label(self.stats_frame, text="Esta Semana: 0")
        self.week_label.pack(side=tk.LEFT)
        
        # Treeview para eventos
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        columns = ("Título", "Data/Hora", "Tipo", "Local", "Descrição")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", 
                                 yscrollcommand=tree_scroll_y.set,
                                 xscrollcommand=tree_scroll_x.set)
        
        # Configurar colunas
        self.tree.heading("Título", text="Título")
        self.tree.heading("Data/Hora", text="Data/Hora")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Local", text="Local")
        self.tree.heading("Descrição", text="Descrição")
        
        self.tree.column("Título", width=150, minwidth=100)
        self.tree.column("Data/Hora", width=120, minwidth=100)
        self.tree.column("Tipo", width=100, minwidth=80)
        self.tree.column("Local", width=120, minwidth=100)
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
    
    def update_events(self, events: List[Evento]):
        """Atualizar lista de eventos."""
        self.events = events
        self._apply_filters()
    
    def _apply_filters(self, event=None):
        """Aplicar filtros à lista de eventos."""
        period_filter = self.period_var.get()
        status_filter = self.status_var.get()
        search_text = self.search_var.get().lower()
        
        self.filtered_events = []
        today = datetime.now().date()
        
        for event in self.events:
            # Filtro por status
            if status_filter != "Todos":
                event_status = "Ativo" if event.ativo else "Inativo"
                if status_filter != event_status:
                    continue
                
            # Filtro por busca
            if search_text and search_text not in (event.nome or "").lower():
                continue
                
            self.filtered_events.append(event)
        
        self._refresh_treeview()
        self._update_statistics()
    
    def _refresh_treeview(self):
        """Atualizar treeview com eventos filtrados."""
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar eventos filtrados
        for i, event in enumerate(self.filtered_events):
            nome = event.nome or "Sem nome"
            # Usar data de criação do evento ou data atual
            data_hora = event.date_time.strftime("%d/%m/%Y") if hasattr(event, 'date_time') and event.date_time else "N/A"
            tipo = "Recorrente" if hasattr(event, 'is_recurring') and event.is_recurring else "Único"
            local = getattr(event, 'location', None) or "Não especificado"
            descricao = event.description[:50] + "..." if len(event.description) > 50 else event.description
            
            item_id = self.tree.insert("", "end", values=(
                nome,
                data_hora,
                tipo,
                local,
                descricao
            ))
            
            # Aplicar cor baseada no status do evento
            if event.ativo:
                self.tree.tag_configure("active", background="#e8f5e8")
                self.tree.item(item_id, tags=("active",))
            else:
                self.tree.tag_configure("inactive", background="#ffebee")
                self.tree.item(item_id, tags=("inactive",))

    def _update_statistics(self):
        """Atualizar estatísticas com base nos eventos filtrados."""
        total = len(self.filtered_events)
        active_count = len([e for e in self.filtered_events if e.ativo])
        inactive_count = total - active_count
        
        self.total_label.config(text=f"Total: {total}")
        self.today_label.config(text=f"Ativos: {active_count}")
        self.week_label.config(text=f"Inativos: {inactive_count}")
    
    def _on_select(self, event):
        """Lida com a seleção de um evento no treeview."""
        selected_items = self.tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            # Obter o índice do item selecionado
            index = self.tree.index(selected_item)
            if 0 <= index < len(self.filtered_events):
                self.selected_event = self.filtered_events[index]
                self.delete_button.config(state="normal")
        else:
            self.selected_event = None
            self.delete_button.config(state="disabled")
      
    def _on_double_click(self, event):
        """Lida com o duplo clique em um evento, abrindo o editor."""
        self._edit_event()

    def _delete_event(self):
        """Excluir o evento selecionado."""
        if self.selected_event and self.selected_event.id is not None:
            # Confirmar exclusão
            if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o evento '{self.selected_event.nome}'?"):
                try:
                    self.controller.delete_event(self.selected_event.id)
                    self.selected_event = None
                    self.delete_button.config(state="disabled")
                    # Atualizar a view principal
                    if hasattr(self.master, 'update_view'):
                        self.master.update_view()
                    else:
                        self.refresh()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao excluir evento: {e}")
        else:
            messagebox.showinfo("Nenhum Evento Selecionado", "Por favor, selecione um evento para excluir.")

    def get_selected_event(self) -> Optional[Evento]:
        """Retornar o evento selecionado."""
        return self.selected_event
    
    def refresh(self):
        """Atualizar a lista de eventos a partir do controller."""
        print("[EventPanel] Atualizando eventos...")
        try:
            # Chamar o método do controller que busca todos os eventos ativos
            events = self.controller.get_all_active_events()
            self.update_events(events)
        except Exception as e:
            print(f"Erro ao atualizar eventos: {e}")
            messagebox.showerror("Erro de Atualização", f"Não foi possível carregar os eventos: {e}")