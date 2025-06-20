# Este arquivo não é mais necessário, pois a lógica de armazenamento
# de dados em memória foi substituída pela camada de persistência
# com o banco de dados em `model/db/repository.py`.

# A classe `Agenda` e seus métodos foram absorvidos e adaptados
# pelo `AgendaController` e `AgendaRepository`.

from collections import defaultdict
from datetime import datetime
from model.task import Task
from model.priority_flag import PriorityFlag

class Agenda:
    def __init__(self):
        self.tasks_by_date = defaultdict(list)
        self.eventos = []

    def add_task(self, date, task):
        self.tasks_by_date[date].append(task)

    def get_tasks_for_date(self, date):
        tarefas = self.tasks_by_date.get(date, [])
        eventos = self.get_event_tasks_for_date(date)
        print(f"[Agenda] {date} → {len(tarefas)} tarefas, {len(eventos)} eventos")
        return tarefas 

    def add_evento(self, evento):
        self.eventos.append(evento)

    def get_event_tasks_for_date(self, date):
        data_obj = datetime.strptime(date, "%Y-%m-%d").date()
        dias_pt = {
            0: 'seg', 1: 'ter', 2: 'qua',
            3: 'qui', 4: 'sex', 5: 'sáb', 6: 'dom'
        }
        dia_semana = dias_pt[data_obj.weekday()]
        result = []
        for evento in self.eventos:
            if evento.ativo and dia_semana in evento.dias_semana:
                if not evento.data_encerramento or data_obj <= evento.data_encerramento:
                    result.append(Task(
                        description=evento.description,
                        priority=None,
                        nome=evento.nome,
                        is_agendamento=False,
                        is_evento=True,
                        dias_evento=evento.dias_semana
                    ))
        return result
    
    def delete_task(self, date, task):
        if date in self.tasks_by_date:
            self.tasks_by_date[date] = [
                t for t in self.tasks_by_date[date]
                if not (t.description == task.description and t.nome == task.nome and t.is_evento == task.is_evento)
            ]

    def update_task(self, date, updated_task):
        if date in self.tasks_by_date:
            for idx, t in enumerate(self.tasks_by_date[date]):
                if (t.description == updated_task.description and t.nome == updated_task.nome):
                    self.tasks_by_date[date][idx] = updated_task
                    break

    def update_evento(self, edited_task):
        for evento in self.eventos:
            if evento.description == edited_task.description and evento.nome == edited_task.nome:
                evento.description = edited_task.description
                evento.nome = edited_task.nome
                evento.dias_semana = edited_task.dias_evento

        # Regenera as tarefas futuras com os novos dias
        from datetime import datetime, timedelta
        hoje = datetime.today().date()
        for i in range(90):
            data = hoje + timedelta(days=i)
            dia = data.strftime('%Y-%m-%d')
            self.tasks_by_date[dia] = [
                t for t in self.tasks_by_date.get(dia, [])
                if not (t.is_evento and t.description == edited_task.description and t.nome == edited_task.nome)
            ]

        # Regenerar com base nos novos dias
        from model.task import Task
        for i in range(90):
            data = hoje + timedelta(days=i)
            weekday = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom'][data.weekday()]
            if weekday in edited_task.dias_evento:
                date_str = data.strftime('%Y-%m-%d')
                self.add_task(date_str, Task(
                    description=edited_task.description,
                    priority=None,
                    nome=edited_task.nome,
                    is_agendamento=False,
                    is_evento=True,
                    dias_evento=edited_task.dias_evento
                ))

