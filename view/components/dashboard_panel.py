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
                # Obter todas as tarefas dos últimos 30 dias
                all_tasks = []
                date_range = self._get_date_range()
                
                for date_str in date_range:
                    try:
                        tasks = self.controller.get_tasks_for_date(date_str)
                        all_tasks.extend(tasks)
                    except Exception as e:
                        print(f"Erro ao carregar tarefas para {date_str}: {e}")
                        continue
                
                # Obter dados dos eventos
                events = self.controller.get_all_active_events()
                
                # Calcular estatísticas
                stats = self._calculate_statistics(all_tasks, events)
                
                # Atualizar UI
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
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if hasattr(t, 'status') and t.status == "concluída"])
        pending_tasks = total_tasks - completed_tasks
        
        # Calcular taxa de conclusão
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Distribuição por status
        status_distribution = {
            'completed': completed_tasks,
            'pending': pending_tasks,
            'in_progress': 0  # Não implementado ainda
        }
        
        # Distribuição por prioridade
        priority_distribution = {'high': 0, 'normal': 0, 'low': 0}
        for task in tasks:
            if hasattr(task, 'priority') and task.priority:
                priority = task.priority.value
                if priority in ['MUITO_IMPORTANTE', 'IMPORTANTE']:
                    priority_distribution['high'] += 1
                elif priority == 'MEDIA':
                    priority_distribution['normal'] += 1
                else:
                    priority_distribution['low'] += 1
        
        # Distribuição por tipo
        type_distribution = {'task': 0, 'meeting': 0, 'reminder': 0}
        for task in tasks:
            if hasattr(task, 'is_agendamento') and task.is_agendamento:
                type_distribution['meeting'] += 1
            elif hasattr(task, 'is_evento') and task.is_evento:
                type_distribution['reminder'] += 1
            else:
                type_distribution['task'] += 1
        
        stats = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'total_events': len(events),
            'upcoming_events': len([e for e in events if self._is_upcoming(e)]),
            'status_distribution': status_distribution,
            'priority_distribution': priority_distribution,
            'type_distribution': type_distribution,
            'completion_trend': [],
            'completion_rate': round(completion_rate, 1)
        }
        
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
        self._update_stat_cards()
        self._update_pie_chart()
        self._update_bar_chart()
    
    def _update_stat_cards(self):
        """Atualizar cards de estatísticas."""
        if hasattr(self, 'total_card') and hasattr(self.total_card, 'value_label'):
            self.total_card.value_label.configure(text=str(self.stats['total_tasks']))
        
        if hasattr(self, 'completed_card') and hasattr(self.completed_card, 'value_label'):
            self.completed_card.value_label.configure(text=str(self.stats['completed_tasks']))
        
        if hasattr(self, 'pending_card') and hasattr(self.pending_card, 'value_label'):
            self.pending_card.value_label.configure(text=str(self.stats['pending_tasks']))
        
        if hasattr(self, 'completion_rate_card') and hasattr(self.completion_rate_card, 'value_label'):
            self.completion_rate_card.value_label.configure(text=f"{self.stats['completion_rate']}%")
    
    def _update_pie_chart(self):
        """Atualizar gráfico de pizza com dados reais."""
        if not hasattr(self, 'pie_chart'):
            return
            
        # Limpar canvas
        self.pie_chart.delete("all")
        
        # Obter dados de distribuição
        status_data = self.stats.get('status_distribution', {})
        if not status_data or sum(status_data.values()) == 0:
            # Desenhar gráfico vazio
            self.pie_chart.create_text(150, 100, text="Sem dados", font=("Arial", 12))
            return
        
        # Cores para cada status
        colors = {
            'completed': ColorPalette.SUCCESS['main'],
            'pending': ColorPalette.WARNING['main'],
            'in_progress': ColorPalette.PRIMARY['main']
        }
        
        # Configurações do gráfico
        center_x, center_y = 150, 100
        radius = 80
        total = sum(status_data.values())
        
        # Desenhar fatias do gráfico
        start_angle = 0
        for status, count in status_data.items():
            if count > 0:
                # Calcular ângulo da fatia
                angle = (count / total) * 360
                end_angle = start_angle + angle
                
                # Converter para coordenadas
                start_rad = math.radians(start_angle)
                end_rad = math.radians(end_angle)
                
                # Desenhar fatia
                color = colors.get(status, ColorPalette.NEUTRAL['gray_400'])
                self.pie_chart.create_arc(
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius,
                    start=start_angle, extent=angle,
                    fill=color, outline="white", width=2
                )
                
                # Adicionar legenda
                legend_x = 250
                legend_y = 50 + len([s for s in status_data.keys() if s <= status]) * 20
                self.pie_chart.create_rectangle(
                    legend_x, legend_y - 8,
                    legend_x + 15, legend_y + 8,
                    fill=color, outline=""
                )
                self.pie_chart.create_text(
                    legend_x + 25, legend_y,
                    text=f"{status.title()}: {count}",
                    anchor="w", font=("Arial", 10)
                )
                
                start_angle = end_angle
    
    def _update_bar_chart(self):
        """Atualizar gráfico de barras com dados reais."""
        if not hasattr(self, 'bar_chart'):
            return
            
        # Limpar canvas
        self.bar_chart.delete("all")
        
        # Obter dados de prioridade
        priority_data = self.stats.get('priority_distribution', {})
        if not priority_data or sum(priority_data.values()) == 0:
            # Desenhar gráfico vazio
            self.bar_chart.create_text(150, 100, text="Sem dados", font=("Arial", 12))
            return
        
        # Cores para cada prioridade
        colors = {
            'high': ColorPalette.ERROR['main'],
            'normal': ColorPalette.WARNING['main'],
            'low': ColorPalette.SUCCESS['main']
        }
        
        # Configurações do gráfico
        chart_width = 280
        chart_height = 150
        margin = 40
        bar_width = (chart_width - 2 * margin) / len(priority_data)
        
        # Encontrar valor máximo para escala
        max_value = max(priority_data.values()) if priority_data.values() else 1
        
        # Desenhar eixos
        self.bar_chart.create_line(margin, chart_height - margin, 
                                  chart_width - margin, chart_height - margin, 
                                  fill="black", width=2)  # Eixo X
        self.bar_chart.create_line(margin, margin, 
                                  margin, chart_height - margin, 
                                  fill="black", width=2)  # Eixo Y
        
        # Desenhar barras
        x_pos = margin + bar_width / 2
        for priority, count in priority_data.items():
            if count > 0:
                # Calcular altura da barra
                bar_height = (count / max_value) * (chart_height - 2 * margin)
                
                # Desenhar barra
                color = colors.get(priority, ColorPalette.NEUTRAL['gray_400'])
                self.bar_chart.create_rectangle(
                    x_pos - bar_width/3, chart_height - margin - bar_height,
                    x_pos + bar_width/3, chart_height - margin,
                    fill=color, outline="white", width=1
                )
                
                # Adicionar valor no topo da barra
                self.bar_chart.create_text(
                    x_pos, chart_height - margin - bar_height - 10,
                    text=str(count), font=("Arial", 10, "bold")
                )
                
                # Adicionar label da prioridade
                priority_labels = {'high': 'Alta', 'normal': 'Média', 'low': 'Baixa'}
                label = priority_labels.get(priority, priority.title())
                self.bar_chart.create_text(
                    x_pos, chart_height - margin + 15,
                    text=label, font=("Arial", 9)
                )
            
            x_pos += bar_width
    
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