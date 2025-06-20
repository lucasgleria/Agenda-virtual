class Evento:
    def __init__(self, description, nome, dias_semana):
        self.description = description
        self.nome = nome
        self.dias_semana = dias_semana  # Ex: ['seg', 'ter']
        self.ativo = True  # Enquanto ativo, gera tarefas futuras
        self.data_encerramento = None  # Data a partir da qual ele para