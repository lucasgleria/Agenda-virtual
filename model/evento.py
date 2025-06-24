from datetime import datetime, timedelta

class Evento:
    def __init__(self, description, nome, dias_semana):
        self.description = description
        self.nome = nome
        self.dias_semana = dias_semana  # Ex: ['seg', 'ter']
        self.ativo = True  # Enquanto ativo, gera tarefas futuras
        self.data_encerramento = None  # Data a partir da qual ele para
        
        # Atributos adicionais para compatibilidade com EventPanel
        self.id = None
        self.date_time = datetime.now()  # Data e hora do evento
        self.event_type = "Outro"  # Tipo do evento (Reunião, Compromisso, Lembrete, etc.)
        self.location = None  # Local do evento
        self.is_recurring = False  # Se é um evento recorrente
        self.recurrence_pattern = None  # Padrão de recorrência (WEEKLY, MONTHLY, etc.)