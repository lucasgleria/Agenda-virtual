from tkinter import ttk
import tkinter as tk

from view.components.calendar_panel import CalendarPanel
from view.components.task_list_panel import TaskListPanel
from view.components.alert_panel import AlertPanel
from view.components.event_panel import EventPanel
from view.components.editor_panel import EditorPanel
from view.components.filter_panel import FilterPanel
from view.components.dashboard_panel import DashboardPanel
from view.components.notification_panel import NotificationPanel
from model.task import Task
from view.theme.styles import StyleManager
from view.theme.colors import ColorPalette
import json
import os

class AgendaView:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Virtual - Sistema de Gerenciamento de Tarefas")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Configurar estilos
        StyleManager.setup_styles()
        
        # Configurar cor de fundo da janela principal
        self.root.configure(bg=ColorPalette.BACKGROUND['primary'])

        self.completed_tasks = {}
        self.editor_mode = False
        self.controller = None
        self.current_panel = 'tasks'  # 'tasks', 'dashboard'
        
        # Main container
        self.main_frame = ttk.Frame(self.root, style='Panel.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Sistema de notificações
        self.notification_panel = NotificationPanel(self.root)

        # Barra de ferramentas
        self._create_toolbar()

        # Container principal com layout horizontal
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Ajustar grid para proporções: 25%/50%/25%
        self.content_frame.grid_columnconfigure(0, weight=100)  # Esquerda (25%)
        self.content_frame.grid_columnconfigure(1, weight=40)  # Centro (50%)
        self.content_frame.grid_columnconfigure(2, weight=100)  # Direita (25%)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Painel esquerdo (event panel) - 20% da largura
        self.left_panel = ttk.Frame(self.content_frame, style='Card.TFrame')
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(0, weight=1)
        self.left_panel.grid_propagate(False)

        # Painel central com sistema de abas - 60% da largura
        self.center_panel = ttk.Frame(self.content_frame)
        self.center_panel.grid(row=0, column=1, sticky="nsew", padx=5)
        self.center_panel.grid_columnconfigure(0, weight=1)
        self.center_panel.grid_rowconfigure(0, weight=1)

        # Painel direito (alert panel) - 20% da largura
        self.right_panel = ttk.Frame(self.content_frame, style='Card.TFrame')
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_propagate(False)

        # Criar sistema de abas para o painel central
        self._create_tab_system()
        
        # Subcomponents
        self.filter_panel = FilterPanel(self.tab_content_frame, self.handle_apply_filters)
        self.calendar_panel = CalendarPanel(self.tab_content_frame, self.handle_add_task, self.handle_add_evento, self.update_view)
        self.task_list_panel = TaskListPanel(self.tab_content_frame, None)
        self.task_list_panel.pack(fill='both', expand=True, pady=(10, 0))
        
        print("[GUI] Criando AlertPanel...")
        self.alert_panel = AlertPanel(self.right_panel, None)
        print("[GUI] AlertPanel criado")
        self.alert_panel.grid(row=0, column=0, sticky="nsew")
        
        print("[GUI] Criando EventPanel...")
        self.event_panel = EventPanel(self.left_panel, None)
        print("[GUI] EventPanel criado")
        self.event_panel.grid(row=0, column=0, sticky="nsew")
        
        self.editor_panel = EditorPanel(self.tab_content_frame, self.handle_edit_task, self.handle_delete_task)
        
        # Painel de dashboard (inicialmente oculto)
        self.dashboard_panel = None
        
        # Verificar estado final dos painéis
        print(f"[GUI] Estado final - EventPanel visível: {self.event_panel.winfo_ismapped()}")
        print(f"[GUI] Estado final - AlertPanel visível: {self.alert_panel.winfo_ismapped()}")
        print(f"[GUI] Estado final - Left panel visível: {self.left_panel.winfo_ismapped()}")
        print(f"[GUI] Estado final - Right panel visível: {self.right_panel.winfo_ismapped()}")

    def _create_tab_system(self):
        """Criar sistema de abas para o painel central"""
        # Frame para as abas
        self.tab_frame = ttk.Frame(self.center_panel)
        self.tab_frame.pack(fill="x", pady=(0, 5))
        
        # Notebook para as abas
        self.notebook = ttk.Notebook(self.tab_frame)
        self.notebook.pack(fill="x")
        
        # Aba de Tarefas
        self.tasks_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.tasks_tab, text="📋 Tarefas")
        
        # Aba de Dashboard
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="📊 Dashboard")
        
        # Frame de conteúdo da aba atual
        self.tab_content_frame = ttk.Frame(self.tasks_tab)
        self.tab_content_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Bind para mudança de aba
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _on_tab_changed(self, event):
        """Callback para mudança de aba"""
        current_tab = self.notebook.select()
        tab_id = self.notebook.index(current_tab)
        
        if tab_id == 0:  # Aba de Tarefas
            self.current_panel = 'tasks'
            self._show_tasks_tab()
        elif tab_id == 1:  # Aba de Dashboard
            self.current_panel = 'dashboard'
            self._show_dashboard_tab()

    def _show_tasks_tab(self):
        """Mostrar conteúdo da aba de tarefas"""
        # Ocultar dashboard se estiver visível
        if self.dashboard_panel:
            self.dashboard_panel.pack_forget()
        
        # Mostrar componentes de tarefas
        self.filter_panel.frame.pack(fill='x', pady=(0, 5))
        self.calendar_panel.frame.pack(fill='x', pady=(0, 5))
        self.task_list_panel.pack(fill='both', expand=True, pady=(10, 0))
        self.editor_panel.frame.pack_forget()
        
        # Atualizar dados
        if self.controller:
            self.update_view()

    def _show_dashboard_tab(self):
        """Mostrar conteúdo da aba de dashboard"""
        # Ocultar componentes de tarefas
        self.filter_panel.frame.pack_forget()
        self.calendar_panel.frame.pack_forget()
        self.task_list_panel.pack_forget()
        self.editor_panel.frame.pack_forget()
        
        # Criar dashboard se não existir
        if self.dashboard_panel is None:
            self.dashboard_panel = DashboardPanel(self.dashboard_tab, self.controller)
        
        # Mostrar dashboard
        self.dashboard_panel.pack(fill='both', expand=True, padx=15, pady=10)

    def set_controller(self, controller):
        self.controller = controller
        self.calendar_panel.set_controller(controller)
        
        # Atualizar controllers dos painéis
        if hasattr(self.event_panel, 'controller'):
            self.event_panel.controller = controller
        if hasattr(self.task_list_panel, 'controller'):
            self.task_list_panel.controller = controller
        if hasattr(self.alert_panel, 'controller'):
            self.alert_panel.controller = controller
            
        self.calendar_panel.set_toggle_editor_mode_callback(self.toggle_editor_mode)
        self.load_initial_data()

    def toggle_dashboard(self):
        """Alterna entre o painel de tarefas e o dashboard."""
        if self.current_panel == 'tasks':
            self.notebook.select(1)  # Selecionar aba dashboard
        else:
            self.notebook.select(0)  # Selecionar aba tarefas
    
    def handle_add_task(self, task_data):
        """Callback para adicionar tarefa."""
        if self.controller:
            try:
                # Desempacotar os dados da tarefa para os parâmetros esperados pelo controller
                self.controller.add_task(
                    date=task_data['date'],
                    description=task_data['description'],
                    priority=task_data['priority'],
                    nome=task_data.get('nome'),
                    is_agendamento=task_data.get('is_agendamento', False),
                    is_evento=task_data.get('is_evento', False),
                    dias_evento=task_data.get('dias_evento')
                )
                self.update_view()
                
                # Feedback visual de sucesso
                task_name = task_data.get('nome') or task_data['description']
                self.notification_panel.show_success(f"Tarefa '{task_name}' adicionada com sucesso!")
                
            except Exception as e:
                # Feedback visual de erro
                self.notification_panel.show_error(f"Erro ao adicionar tarefa: {str(e)}")

    def handle_add_evento(self, evento_data):
        """Callback para adicionar evento."""
        if self.controller:
            try:
                self.controller.add_evento(
                    evento_data['description'],
                    evento_data['nome'],
                    evento_data['dias_semana']
                )
                self.update_view()
                
                # Feedback visual de sucesso
                evento_name = evento_data.get('nome') or evento_data['description']
                self.notification_panel.show_success(f"Evento '{evento_name}' criado com sucesso!")
                
            except Exception as e:
                # Feedback visual de erro
                self.notification_panel.show_error(f"Erro ao criar evento: {str(e)}")

    def handle_encerrar_evento(self, evento):
        """Callback para encerrar evento."""
        if self.controller:
            try:
                self.controller.encerrar_evento(evento)
                self.update_view()
                
                # Feedback visual de sucesso
                evento_name = getattr(evento, 'nome', 'Evento') or getattr(evento, 'description', 'Evento')
                self.notification_panel.show_success(f"Evento '{evento_name}' encerrado com sucesso!")
                
            except Exception as e:
                # Feedback visual de erro
                self.notification_panel.show_error(f"Erro ao encerrar evento: {str(e)}")

    def handle_edit_task(self, date, task):
        """Callback para editar tarefa."""
        if self.controller:
            try:
                self.controller.edit_task(date, task)
                self.update_view()
                
                # Feedback visual de sucesso
                task_name = getattr(task, 'nome', 'Tarefa') or getattr(task, 'description', 'Tarefa')
                self.notification_panel.show_success(f"Tarefa '{task_name}' editada com sucesso!")
                
            except Exception as e:
                # Feedback visual de erro
                self.notification_panel.show_error(f"Erro ao editar tarefa: {str(e)}")

    def handle_delete_task(self, date, task):
        """Callback para excluir tarefa."""
        if self.controller:
            try:
                self.controller.delete_task(date, task)
                self.update_view()
                
                # Feedback visual de sucesso
                task_name = getattr(task, 'nome', 'Tarefa') or getattr(task, 'description', 'Tarefa')
                self.notification_panel.show_success(f"Tarefa '{task_name}' excluída com sucesso!")
                
            except Exception as e:
                # Feedback visual de erro
                self.notification_panel.show_error(f"Erro ao excluir tarefa: {str(e)}")

    def toggle_completion(self, task_key, done):
        """Alternar status de conclusão de uma tarefa."""
        if self.controller:
            try:
                self.controller.toggle_task_completion(task_key, done)
                self.update_view()
                
                # Feedback visual de sucesso
                status = "concluída" if done else "reaberta"
                self.notification_panel.show_success(f"Tarefa marcada como {status}!")
                
            except Exception as e:
                # Feedback visual de erro
                self.notification_panel.show_error(f"Erro ao alterar status da tarefa: {str(e)}")

    def toggle_editor_mode(self):
        """Alternar modo editor."""
        self.editor_mode = not self.editor_mode
        if self.editor_mode:
            self._show_editor()
        else:
            self._hide_editor()
        self.update_view()

    def _show_editor(self):
        """Mostrar painel de editor."""
        # Ocultar painel de tarefas
        self.task_list_panel.pack_forget()
        
        # Mostrar painel de editor
        self.editor_panel.frame.pack(fill='both', expand=True, pady=(10, 0))

    def _hide_editor(self):
        """Ocultar painel de editor."""
        # Ocultar painel de editor
        self.editor_panel.frame.pack_forget()
        
        # Mostrar painel de tarefas
        self.task_list_panel.pack(fill='both', expand=True, pady=(10, 0))

    def update_view(self):
        """Atualizar visualização."""
        if self.controller:
            current_date = self.calendar_panel.get_selected_date()
            tasks = self.controller.get_tasks_for_date(current_date)
            
            # Atualizar painel de tarefas
            self.task_list_panel.update_task_list(current_date, tasks)
            
            # Atualizar painel de editor se estiver visível
            if self.editor_mode:
                self.editor_panel.update_editor_panel(current_date, tasks, True)
            
            # Atualizar painel de eventos
            if hasattr(self.event_panel, 'update_events'):
                events = self.controller.get_all_active_events()
                self.event_panel.update_events(events)
            
            # Atualizar label da data no calendário
            if hasattr(self.calendar_panel, 'update_date_label'):
                self.calendar_panel.update_date_label()
            
            # Atualizar alertas
            self.update_alerts()

    def update_alerts(self):
        """Atualizar painel de alertas."""
        if self.controller and hasattr(self.alert_panel, 'update_alerts'):
            # Obter eventos e agendamentos para os alertas
            events = self.controller.get_all_active_events()
            
            # Obter todos os agendamentos (não apenas da data atual)
            all_tasks = self.controller.get_tasks()
            agendamentos = [task for task in all_tasks if task.is_agendamento and not task.is_evento]
            
            self.alert_panel.update_alerts(events, agendamentos)

    def handle_apply_filters(self, filters):
        """Callback para aplicar filtros."""
        if hasattr(self.task_list_panel, 'apply_filter'):
            self.task_list_panel.apply_filter(filters)

    def load_initial_data(self):
        """Carregar dados iniciais."""
        self.update_view()

    def _create_toolbar(self):
        """Criar barra de ferramentas com design moderno"""
        toolbar_frame = ttk.Frame(self.main_frame, style='Panel.TFrame')
        toolbar_frame.pack(fill='x', pady=(0, 10))
        
        # Título principal
        title_label = ttk.Label(toolbar_frame, text="📅 Agenda Virtual", 
                               style='Title.TLabel')
        title_label.pack(side='left', padx=(10, 0))
    
    def _show_settings(self):
        """Mostrar janela de configurações"""
        # Placeholder para futura implementação
        print("Configurações - Funcionalidade em desenvolvimento")
    
    def _show_help(self):
        """Mostrar janela de ajuda"""
        # Placeholder para futura implementação
        print("Ajuda - Funcionalidade em desenvolvimento")