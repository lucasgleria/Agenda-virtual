class Task:
    def __init__(self, description, priority=None, nome=None, is_agendamento=False, is_evento=False, is_tarefa=True, dias_evento=None, status='pendente', deadline=None, date=None):
        self.description = description
        self.priority = priority
        self.nome = nome
        self.is_agendamento = is_agendamento
        self.is_evento = is_evento
        self.is_tarefa = is_tarefa  # Nova propriedade para distinguir tarefas
        self.dias_evento = dias_evento or []
        self.status = status
        self.id = None
        self.date = date
        self.deadline = deadline  # Data limite da tarefa
