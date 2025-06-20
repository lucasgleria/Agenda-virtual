class Task:
    def __init__(self, description, priority=None, nome=None, is_agendamento=False, is_evento=False, dias_evento=None, status='pendente'):
        self.description = description
        self.priority = priority
        self.nome = nome
        self.is_agendamento = is_agendamento
        self.is_evento = is_evento
        self.dias_evento = dias_evento or []
        self.status = status
        self.id = None
        self.date = None
