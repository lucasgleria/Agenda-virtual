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
        """Atualizar visualização com sincronização garantida."""
        if not self.controller:
            print("[GUI] Controller não disponível para atualização")
            return
            
        try:
            # Obter data atual selecionada
            current_date = self.calendar_panel.get_selected_date()
            print(f"[GUI] Atualizando view para data: {current_date}")
            
            # Obter tarefas da data atual
            tasks = self.controller.get_tasks_for_date(current_date)
            print(f"[GUI] Tarefas encontradas: {len(tasks)}")
            
            # Atualizar painel de tarefas (sempre)
            if hasattr(self.task_list_panel, 'update_task_list'):
                self.task_list_panel.update_task_list(current_date, tasks)
                print("[GUI] Painel de tarefas atualizado")
            
            # Atualizar painel de editor se estiver visível
            if self.editor_mode and hasattr(self.editor_panel, 'update_editor_panel'):
                self.editor_panel.update_editor_panel(current_date, tasks, True)
                print("[GUI] Painel de editor atualizado")
            
            # Atualizar painel de eventos (sempre)
            try:
                events = self.controller.get_all_active_events()
                if hasattr(self.event_panel, 'update_events'):
                    self.event_panel.update_events(events)
                    print(f"[GUI] Painel de eventos atualizado: {len(events)} eventos")
            except Exception as e:
                print(f"[GUI] Erro ao atualizar painel de eventos: {e}")
            
            # Atualizar label da data no calendário (sempre)
            if hasattr(self.calendar_panel, 'update_date_label'):
                self.calendar_panel.update_date_label()
                print("[GUI] Label da data atualizada")
            
            # Atualizar alertas (sempre)
            self.update_alerts()
            print("[GUI] Alertas atualizados")
            
            # Atualizar dashboard se estiver visível
            if self.current_panel == 'dashboard' and self.dashboard_panel:
                try:
                    if hasattr(self.dashboard_panel, '_load_statistics'):
                        self.dashboard_panel._load_statistics()
                        print("[GUI] Dashboard atualizado")
                except Exception as e:
                    print(f"[GUI] Erro ao atualizar dashboard: {e}")
            
            print("[GUI] Atualização da view concluída com sucesso")
            
        except Exception as e:
            print(f"[GUI] Erro durante atualização da view: {e}")
            # Tentar mostrar notificação de erro se disponível
            if hasattr(self, 'notification_panel'):
                self.notification_panel.show_error(f"Erro ao atualizar interface: {str(e)}")

    def update_alerts(self):
        """Atualizar painel de alertas com tratamento de erro."""
        if not self.controller:
            print("[GUI] Controller não disponível para atualizar alertas")
            return
            
        try:
            # Obter eventos ativos
            events = self.controller.get_all_active_events()
            
            # Obter todos os agendamentos (não apenas da data atual)
            all_tasks = self.controller.get_tasks()
            agendamentos = [task for task in all_tasks if task.is_agendamento and not task.is_evento]
            
            # Atualizar painel de alertas
            if hasattr(self.alert_panel, 'update_alerts'):
                self.alert_panel.update_alerts(events, agendamentos)
                print(f"[GUI] Alertas atualizados: {len(events)} eventos, {len(agendamentos)} agendamentos")
            else:
                print("[GUI] Painel de alertas não possui método update_alerts")
                
        except Exception as e:
            print(f"[GUI] Erro ao atualizar alertas: {e}")
            # Não mostrar notificação de erro para alertas para evitar spam

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
        
        # Configurar grid weights para responsividade
        toolbar_frame.grid_columnconfigure(1, weight=1)
        
        # Título principal
        title_label = ttk.Label(toolbar_frame, text="📅 Agenda Virtual", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky="w", padx=(10, 0))
        
        # Frame para botões de ação
        actions_frame = ttk.Frame(toolbar_frame)
        actions_frame.grid(row=0, column=1, sticky="e", padx=(0, 10))
        
        # Botão de Dashboard
        self.dashboard_btn = ttk.Button(actions_frame, text="📊 Dashboard", 
                                       command=self.toggle_dashboard)
        self.dashboard_btn.pack(side="right", padx=(5, 0))
        
        # Botão de Exportar
        self.export_btn = ttk.Button(actions_frame, text="📤 Exportar", 
                                    command=self._handle_export_data)
        self.export_btn.pack(side="right", padx=(5, 0))
        
        # Botão de Backup
        self.backup_btn = ttk.Button(actions_frame, text="💾 Backup", 
                                    command=self._handle_create_backup)
        self.backup_btn.pack(side="right", padx=(5, 0))
        
        # Botão de Configurações
        self.settings_btn = ttk.Button(actions_frame, text="⚙️ Configurações", 
                                      command=self._show_settings)
        self.settings_btn.pack(side="right", padx=(5, 0))
        
        # Botão de Ajuda
        self.help_btn = ttk.Button(actions_frame, text="❓ Ajuda", 
                                  command=self._show_help)
        self.help_btn.pack(side="right", padx=(5, 0))
    
    def _handle_export_data(self):
        """Handler para exportar dados"""
        if self.controller:
            try:
                self.controller.handle_export_data()
                self.notification_panel.show_success("Dados exportados com sucesso!")
            except Exception as e:
                self.notification_panel.show_error(f"Erro ao exportar dados: {str(e)}")
        else:
            self.notification_panel.show_warning("Controller não disponível para exportação")
    
    def _handle_create_backup(self):
        """Handler para criar backup"""
        if self.controller:
            try:
                self.controller.handle_create_backup()
                self.notification_panel.show_success("Backup criado com sucesso!")
            except Exception as e:
                self.notification_panel.show_error(f"Erro ao criar backup: {str(e)}")
        else:
            self.notification_panel.show_warning("Controller não disponível para backup")
    
    def _show_settings(self):
        """Mostrar janela de configurações"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Configurações - Agenda Virtual")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)
        settings_window.grab_set()
        
        # Centralizar janela
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(settings_window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="⚙️ Configurações", 
                               font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Configurações de notificação
        notif_frame = ttk.LabelFrame(main_frame, text="🔔 Notificações", padding=10)
        notif_frame.pack(fill='x', pady=(0, 10))
        
        notif_var = tk.BooleanVar(value=True)
        notif_check = ttk.Checkbutton(notif_frame, text="Ativar notificações do sistema", 
                                     variable=notif_var)
        notif_check.pack(anchor='w')
        
        # Configurações de interface
        ui_frame = ttk.LabelFrame(main_frame, text="🎨 Interface", padding=10)
        ui_frame.pack(fill='x', pady=(0, 10))
        
        theme_var = tk.StringVar(value="Claro")
        ttk.Label(ui_frame, text="Tema:").pack(anchor='w')
        theme_combo = ttk.Combobox(ui_frame, textvariable=theme_var, 
                                  values=["Claro", "Escuro"], state="readonly")
        theme_combo.pack(anchor='w', pady=(5, 0))
        
        # Botões de ação
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(20, 0))
        
        save_btn = ttk.Button(button_frame, text="💾 Salvar", 
                             command=lambda: self._save_settings(settings_window))
        save_btn.pack(side='right', padx=(5, 0))
        
        cancel_btn = ttk.Button(button_frame, text="❌ Cancelar", 
                               command=settings_window.destroy)
        cancel_btn.pack(side='right')
    
    def _save_settings(self, window):
        """Salvar configurações"""
        # Aqui implementaria a lógica para salvar as configurações
        self.notification_panel.show_success("Configurações salvas com sucesso!")
        window.destroy()
    
    def _show_help(self):
        """Mostrar janela de ajuda"""
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Ajuda - Agenda Virtual")
        help_window.geometry("500x400")
        help_window.resizable(False, False)
        help_window.grab_set()
        
        # Centralizar janela
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Frame principal com scroll
        main_frame = ttk.Frame(help_window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        title_label = ttk.Label(scrollable_frame, text="❓ Ajuda - Agenda Virtual", 
                               font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Seções de ajuda
        help_sections = [
            ("📋 Como Adicionar Tarefas", 
             "1. Selecione uma data no calendário\n"
             "2. Digite a descrição da tarefa\n"
             "3. Escolha a prioridade\n"
             "4. Clique em 'Adicionar'"),
            
            ("📅 Como Criar Eventos", 
             "1. Marque a caixa 'É um evento'\n"
             "2. Selecione os dias da semana\n"
             "3. Digite a descrição\n"
             "4. Clique em 'Adicionar'"),
            
            ("📊 Dashboard", 
             "Acesse o dashboard para ver estatísticas\n"
             "e gráficos das suas tarefas e eventos."),
            
            ("🔔 Notificações", 
             "Configure as notificações em Configurações\n"
             "para receber lembretes dos seus agendamentos."),
            
            ("💾 Backup e Exportação", 
             "Use os botões na barra de ferramentas para\n"
             "fazer backup ou exportar seus dados.")
        ]
        
        for title, content in help_sections:
            section_frame = ttk.LabelFrame(scrollable_frame, text=title, padding=10)
            section_frame.pack(fill='x', pady=(0, 10))
            
            content_label = ttk.Label(section_frame, text=content, 
                                     font=("Segoe UI", 10), justify='left')
            content_label.pack(anchor='w')
        
        # Botão de fechar
        close_btn = ttk.Button(scrollable_frame, text="❌ Fechar", 
                              command=help_window.destroy)
        close_btn.pack(pady=(20, 0))
        
        # Empacotar canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")