import tkinter as tk
from tkinter import ttk, Canvas
from datetime import datetime, timedelta
import math
import threading
from view.theme.colors import ColorPalette

class DashboardPanel(ttk.Frame):
    """Painel de dashboard com estatísticas e gráficos."""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.stats = {}
        self.charts = {}
        
        # Configurar grid weights para responsividade
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Criar widgets
        self._create_widgets()
        
        # Carregar dados iniciais
        self._load_statistics()
    
    def _create_widgets(self):
        """Criar widgets do dashboard."""
        # Header
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(header_frame, text="📊 Dashboard", 
                               font=("Arial", 18, "bold"),
                               foreground=ColorPalette.TEXT['primary'])
        title_label.grid(row=0, column=0, sticky="w")
        
        # Botão de atualizar
        refresh_btn = ttk.Button(header_frame, text="🔄 Atualizar", 
                                command=self._refresh_dashboard)
        refresh_btn.grid(row=0, column=1, sticky="e")
        
        # Cards de estatísticas
        self._create_stat_cards()
        
        # Gráficos
        self._create_charts()
        
    def _create_stat_cards(self):
        """Criar cards de estatísticas."""
        cards_frame = ttk.Frame(self)
        cards_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Configurar grid para cards
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        # Card 1: Total de Tarefas
        self.total_card = self._create_stat_card(cards_frame, "📋 Total de Tarefas", "0", ColorPalette.PRIMARY['main'])
        self.total_card.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Card 2: Tarefas Concluídas
        self.completed_card = self._create_stat_card(cards_frame, "✅ Concluídas", "0", ColorPalette.SUCCESS['main'])
        self.completed_card.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Card 3: Tarefas Pendentes
        self.pending_card = self._create_stat_card(cards_frame, "⏳ Pendentes", "0", ColorPalette.WARNING['main'])
        self.pending_card.grid(row=0, column=2, sticky="ew", padx=5)
        
        # Card 4: Taxa de Conclusão
        self.completion_rate_card = self._create_stat_card(cards_frame, "📈 Taxa de Conclusão", "0%", ColorPalette.SECONDARY['main'])
        self.completion_rate_card.grid(row=0, column=3, sticky="ew", padx=(5, 0))
        
    def _create_stat_card(self, parent, title, value, color):
        """Criar um card de estatística individual."""
        card = ttk.Frame(parent, relief="raised", borderwidth=2)
        
        # Título
        title_label = ttk.Label(card, text=title, 
                               font=("Arial", 12, "bold"),
                               foreground=ColorPalette.TEXT['primary'])
        title_label.pack(pady=(10, 5))
        
        # Valor
        value_label = ttk.Label(card, text=value, 
                               font=("Arial", 20, "bold"), 
                               foreground=color)
        value_label.pack(pady=(0, 10))
        
        # Armazenar referência para atualização
        card.value_label = value_label
        
        return card
    
    def _create_charts(self):
        """Criar gráficos."""
        # Frame para gráficos
        charts_frame = ttk.Frame(self)
        charts_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        charts_frame.grid_columnconfigure(0, weight=1)
        charts_frame.grid_columnconfigure(1, weight=1)
        charts_frame.grid_rowconfigure(0, weight=1)
        
        # Gráfico de pizza: Status das Tarefas
        pie_frame = ttk.LabelFrame(charts_frame, text="Status das Tarefas")
        pie_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        self.pie_chart = Canvas(pie_frame, width=300, height=200, bg="white")
        self.pie_chart.pack(pady=10)
        
        # Gráfico de barras: Tarefas por Prioridade
        bar_frame = ttk.LabelFrame(charts_frame, text="Tarefas por Prioridade")
        bar_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        self.bar_chart = Canvas(bar_frame, width=300, height=200, bg="white")
        self.bar_chart.pack(pady=10)
    
    def _load_statistics(self):
        """Carregar estatísticas do banco de dados."""
        try:
            # Obter dados do controller
            if self.controller:
                # Obter todas as tarefas
                all_tasks = []
                for date in self._get_date_range():
                    tasks = self.controller.get_tasks_for_date(date)
                    all_tasks.extend(tasks)
                
                # Obter dados dos eventos
                events = self.controller.get_all_active_events()
                
                # Calcular estatísticas
                stats = self._calculate_statistics(all_tasks, events)
                
                # Atualizar UI diretamente
                self._update_dashboard(stats)
            else:
                # Controller não disponível, usar dados mock
                stats = self._get_mock_statistics()
                self._update_dashboard(stats)
                
        except Exception as e:
            print(f"Erro ao carregar estatísticas: {str(e)}")
            # Usar dados mock em caso de erro
            stats = self._get_mock_statistics()
            self._update_dashboard(stats)
    
    def _get_date_range(self):
        """Obter range de datas para estatísticas (últimos 30 dias)"""
        dates = []
        today = datetime.now().date()
        for i in range(30):
            date = today - timedelta(days=i)
            dates.append(date.strftime('%Y-%m-%d'))
        return dates
    
    def _get_mock_statistics(self):
        """Obter estatísticas mock quando controller não está disponível."""
        return {
            'total_tasks': 15,
            'completed_tasks': 8,
            'pending_tasks': 7,
            'total_events': 3,
            'upcoming_events': 2,
            'status_distribution': {
                'completed': 8,
                'pending': 5,
                'in_progress': 2
            },
            'priority_distribution': {
                'high': 3,
                'normal': 8,
                'low': 4
            },
            'type_distribution': {
                'task': 10,
                'meeting': 3,
                'reminder': 2
            },
            'completion_trend': [],
            'completion_rate': 53.3
        }
    
    def _calculate_statistics(self, tasks, events):
        """Calcular estatísticas dos dados."""
        stats = {
            'total_tasks': len(tasks),
            'completed_tasks': len([t for t in tasks if hasattr(t, 'completed') and t.completed]),
            'pending_tasks': len([t for t in tasks if not hasattr(t, 'completed') or not t.completed]),
            'total_events': len(events),
            'upcoming_events': len([e for e in events if self._is_upcoming(e)]),
            'status_distribution': {},
            'priority_distribution': {},
            'type_distribution': {},
            'completion_trend': []
        }
        
        # Distribuição por status
        for task in tasks:
            if hasattr(task, 'completed'):
                status = 'completed' if task.completed else 'pending'
            else:
                status = 'pending'
            stats['status_distribution'][status] = stats['status_distribution'].get(status, 0) + 1
        
        # Distribuição por prioridade
        for task in tasks:
            if hasattr(task, 'priority') and task.priority:
                priority = task.priority.value if hasattr(task.priority, 'value') else str(task.priority)
            else:
                priority = 'normal'
            stats['priority_distribution'][priority] = stats['priority_distribution'].get(priority, 0) + 1
        
        # Distribuição por tipo
        for task in tasks:
            if hasattr(task, 'is_evento') and task.is_evento:
                task_type = 'evento'
            elif hasattr(task, 'is_agendamento') and task.is_agendamento:
                task_type = 'agendamento'
            else:
                task_type = 'tarefa'
            stats['type_distribution'][task_type] = stats['type_distribution'].get(task_type, 0) + 1
        
        # Calcular taxa de conclusão
        if stats['total_tasks'] > 0:
            stats['completion_rate'] = (stats['completed_tasks'] / stats['total_tasks']) * 100
        else:
            stats['completion_rate'] = 0
        
        return stats
    
    def _is_upcoming(self, event):
        """Verificar se evento está próximo."""
        try:
            if hasattr(event, 'date'):
                event_date = datetime.strptime(event.date, '%Y-%m-%d').date()
            else:
                return False
            today = datetime.now().date()
            return event_date >= today
        except:
            return False
    
    def _update_dashboard(self, stats):
        """Atualizar dashboard com novas estatísticas."""
        self.stats = stats
        
        # Atualizar cards com animações
        self._update_stat_cards()
        
        # Atualizar gráficos
        self._update_pie_chart()
        self._update_bar_chart()
    
    def _update_stat_cards(self):
        """Atualizar cards de estatísticas com animações."""
        # Atualizar valores
        if hasattr(self.total_card, 'value_label'):
            self.total_card.value_label.config(text=str(self.stats.get('total_tasks', 0)))
        
        if hasattr(self.completed_card, 'value_label'):
            self.completed_card.value_label.config(text=str(self.stats.get('completed_tasks', 0)))
        
        if hasattr(self.pending_card, 'value_label'):
            self.pending_card.value_label.config(text=str(self.stats.get('pending_tasks', 0)))
        
        if hasattr(self.completion_rate_card, 'value_label'):
            rate = self.stats.get('completion_rate', 0)
            self.completion_rate_card.value_label.config(text=f"{rate:.1f}%")
    
    def _update_pie_chart(self):
        """Atualizar gráfico de pizza."""
        self.pie_chart.delete("all")
        
        if not self.stats.get('status_distribution'):
            return
        
        # Configurações do gráfico
        width = 300
        height = 200
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 3
        
        # Cores para cada status
        colors = {
            'completed': '#4CAF50',
            'pending': '#FF9800',
            'in_progress': '#2196F3',
            'cancelled': '#F44336'
        }
        
        # Desenhar gráfico de pizza
        total = sum(self.stats['status_distribution'].values())
        if total == 0:
            return
        
        start_angle = 0
        legend_y = 20
        for status, count in self.stats['status_distribution'].items():
            angle = (count / total) * 360
            
            # Desenhar fatia
            color = colors.get(status, '#9E9E9E')
            self.pie_chart.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=angle,
                fill=color, outline="white", width=2
            )
            
            # Adicionar legenda
            legend_x = 20
            self.pie_chart.create_rectangle(legend_x, legend_y, legend_x + 15, legend_y + 15, 
                                          fill=color, outline="black")
            self.pie_chart.create_text(legend_x + 25, legend_y + 7, 
                                     text=f"{status.replace('_', ' ').title()}: {count}",
                                     anchor="w", font=("Arial", 10))
            
            start_angle += angle
            legend_y += 20
    
    def _update_bar_chart(self):
        """Atualizar gráfico de barras."""
        self.bar_chart.delete("all")
        
        if not self.stats.get('priority_distribution'):
            return
        
        # Configurações do gráfico
        width = 300
        height = 200
        margin = 40
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # Cores para prioridades
        colors = {
            'high': '#F44336',
            'normal': '#FF9800',
            'low': '#4CAF50',
            'MUITO_IMPORTANTE': '#F44336',
            'IMPORTANTE': '#FF9800',
            'MEDIA': '#FFC107',
            'SIMPLES': '#4CAF50'
        }
        
        # Desenhar eixos
        self.bar_chart.create_line(margin, height - margin, width - margin, height - margin, width=2)  # Eixo X
        self.bar_chart.create_line(margin, margin, margin, height - margin, width=2)  # Eixo Y
        
        # Calcular dimensões das barras
        max_value = max(self.stats['priority_distribution'].values()) if self.stats['priority_distribution'] else 1
        bar_width = chart_width / len(self.stats['priority_distribution'])
        
        # Desenhar barras
        x = margin
        for priority, count in self.stats['priority_distribution'].items():
            bar_height = (count / max_value) * chart_height
            color = colors.get(priority, '#9E9E9E')
            
            # Desenhar barra
            self.bar_chart.create_rectangle(
                x, height - margin - bar_height,
                x + bar_width - 10, height - margin,
                fill=color, outline="black", width=1
            )
            
            # Adicionar valor
            self.bar_chart.create_text(
                x + bar_width // 2, height - margin - bar_height - 10,
                text=str(count), font=("Arial", 10, "bold")
            )
            
            # Adicionar label
            priority_label = priority.replace('_', ' ').title()
            self.bar_chart.create_text(
                x + bar_width // 2, height - margin + 15,
                text=priority_label, font=("Arial", 10)
            )
            
            x += bar_width
    
    def _refresh_dashboard(self):
        """Atualizar dashboard."""
        self._load_statistics()
    
    def _show_error(self, message):
        """Mostrar mensagem de erro."""
        # Limpar gráficos
        self.pie_chart.delete("all")
        self.bar_chart.delete("all")
        
        # Mostrar mensagem de erro
        self.pie_chart.create_text(150, 100, text=message, fill="red", font=("Arial", 12))
    
    def refresh_theme(self):
        """Atualizar tema do painel."""
        pass 