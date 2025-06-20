from tkinter import ttk
import tkinter as tk

from view.components.calendar_panel import CalendarPanel
from view.components.task_list_panel import TaskListPanel
from view.components.alert_panel import AlertPanel
from view.components.event_panel import EventPanel
from view.components.editor_panel import EditorPanel
from view.components.filter_panel import FilterPanel

class AgendaView:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Virtual")
        self.root.geometry("1100x650")

        self.completed_tasks = {}
        self.editor_mode = False
        self.controller = None

        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Left (event panel), center (calendar/task), right (alert)
        self.left_panel = ttk.Frame(self.main_frame)
        self.left_panel.pack(side='left', fill='y', padx=(10, 5), pady=10)

        self.center_panel = ttk.Frame(self.main_frame)
        self.center_panel.pack(side='left', fill='both', expand=True, pady=10)

        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.pack(side='right', fill='y', padx=(5, 10), pady=10)

        # Subcomponents
        self.filter_panel = FilterPanel(self.center_panel, self.handle_apply_filters)
        self.calendar_panel = CalendarPanel(self.center_panel, self.handle_add_task, self.handle_add_evento, self.update_view)
        self.task_list_panel = TaskListPanel(self.center_panel, self.toggle_completion)
        self.alert_panel = AlertPanel(self.right_panel)
        self.event_panel = EventPanel(self.left_panel, self.handle_encerrar_evento)
        self.editor_panel = EditorPanel(self.center_panel, self.handle_edit_task, self.handle_delete_task)

    def set_controller(self, controller):
        self.controller = controller
        self.calendar_panel.set_controller(controller)
        self.event_panel.set_controller(controller)
        self.calendar_panel.set_toggle_editor_mode_callback(self.toggle_editor_mode)
        self.load_initial_data()

    def handle_add_task(self, task_data):
        if self.controller:
            self.controller.add_task(**task_data)
            self.calendar_panel.reset_inputs()
            self.update_view()

    def handle_add_evento(self, evento_data):
        if self.controller:
            self.controller.add_evento(**evento_data)
            self.calendar_panel.reset_inputs()
            self.update_view()

    def handle_encerrar_evento(self, evento):
        if self.controller:
            self.controller.encerrar_evento(evento)
            self.update_view()

    def handle_edit_task(self, date, task):
        if self.controller:
            self.controller.edit_task(date, task)
            self.update_view()

    def handle_delete_task(self, date, task):
        if self.controller:
            self.controller.delete_task(date, task)
            self.update_view()

    def toggle_completion(self, task_key, done):
        if self.controller:
            self.controller.update_task_status(task_key, done)
        # A view será atualizada para refletir a mudança no DB
        self.update_view()

    def toggle_editor_mode(self):
        self.editor_mode = not self.editor_mode
        self.update_view()

    def update_view(self):
        if not self.controller:
            return
            
        date = self.calendar_panel.get_selected_date()
        
        # Busca os dados mais recentes do banco através do controller
        tasks = self.controller.get_tasks_for_date(date)
        eventos = self.controller.get_eventos_ativos()

        # Atualiza os painéis com os novos dados
        self.task_list_panel.update_task_list(date, tasks, self.editor_mode)
        self.editor_panel.update_editor_panel(date, tasks, self.editor_mode)
        self.event_panel.update(eventos)
        self.update_alerts()

    def update_alerts(self):
        """Busca os agendamentos futuros e atualiza o painel de alertas."""
        if self.controller:
            upcoming_appointments = self.controller.get_upcoming_appointments_for_alert()
            self.alert_panel.update(upcoming_appointments)
    
    def handle_apply_filters(self, filters):
        if self.controller:
            self.controller.handle_apply_filters(filters)

    def load_initial_data(self):
        self.update_view()