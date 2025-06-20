from model.task import Task
from model.priority_flag import PriorityFlag
from model.evento import Evento
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import simpledialog, Toplevel, StringVar, BooleanVar, ttk, filedialog, messagebox
import json

class AgendaController:
    def __init__(self, repository, view):
        self.repository = repository
        self.view = view
        self.active_filters = {}
        self.view.set_controller(self)

    def add_task(self, date, description, priority, nome=None, is_agendamento=False, is_evento=False, dias_evento=None):
        task_data = {
            'date': date,
            'description': description,
            'priority': PriorityFlag(priority).value if not is_evento else None,
            'nome': nome,
            'is_agendamento': is_agendamento,
            'is_evento': is_evento,
            'dias_evento': dias_evento
        }
        self.repository.add_task(task_data)
        # A view será atualizada pelo próprio método que chamou este.

    def add_evento(self, description, nome, dias_semana):
        evento_data = {
            "description": description,
            "nome": nome,
            "dias_semana": dias_semana
        }
        evento_id = self.repository.add_evento(evento_data)
        
        # Gerar tarefas para o novo evento
        evento = Evento(description, nome, dias_semana)
        evento.id = evento_id
        self.gerar_tarefas_evento(evento)

    def gerar_tarefas_evento(self, evento):
        hoje = datetime.today().date()
        for i in range(90):
            data = hoje + timedelta(days=i)
            dias_pt = {0: 'seg', 1: 'ter', 2: 'qua', 3: 'qui', 4: 'sex', 5: 'sáb', 6: 'dom'}
            if dias_pt[data.weekday()] in evento.dias_semana:
                task_data = {
                    'description': evento.description, 'priority': None, 'nome': evento.nome,
                    'is_agendamento': False, 'is_evento': True, 'dias_evento': evento.dias_semana,
                    'date': data.strftime("%Y-%m-%d"), 'evento_id': evento.id
                }
                self.repository.add_task(task_data)

    def get_tasks_for_date(self, date):
        # Se houver filtros ativos, usa a busca com filtros. Senão, busca normal.
        if self.active_filters and (self.active_filters.get('nome') or self.active_filters.get('status') != 'Todos' or self.active_filters.get('tipo') != 'Todos'):
            tasks_db = self.repository.get_tasks_with_filters(date, self.active_filters)
        else:
            tasks_db = self.repository.get_tasks_by_date(date)
            
        return [self._db_to_task(t) for t in tasks_db]
    
    def get_eventos_ativos(self):
        eventos_db = self.repository.get_eventos_ativos()
        return [self._db_to_evento(e) for e in eventos_db]

    def get_upcoming_appointments_for_alert(self):
        """Busca agendamentos para o painel de alertas."""
        return self.repository.get_upcoming_appointments()

    def encerrar_evento(self, evento):
        self.repository.deactivate_evento(evento.id)
        # Limpar tarefas futuras associadas a esse evento
        self.repository.delete_future_event_tasks(evento.id, datetime.today().date())

    def delete_task(self, date, task):
        if messagebox.askyesno("Confirmar exclusão", f"Excluir '{task.description}'?"):
            self.repository.delete_task_by_content(date, task.description, task.nome)

    def edit_task(self, date, task):
        task_id = self.repository.find_task_id(date, task.description, task.nome)
        if not task_id:
            messagebox.showerror("Erro", "Não foi possível encontrar a tarefa para editar.")
            return

        # Popup de edição
        edit_window = Toplevel(self.view.root)
        edit_window.title("Editar Tarefa")
        edit_window.grab_set()
        edit_window.geometry("300x300")

        tk.Label(edit_window, text="Prioridade:").pack()
        priority_var = tk.StringVar(value=task.priority.value if task.priority else "")
        priority_menu = ttk.Combobox(edit_window, textvariable=priority_var, values=[p.value for p in PriorityFlag])
        priority_menu.pack(pady=5)

        # Campos de edição
        tk.Label(edit_window, text="Descrição:").pack()
        desc_var = StringVar(value=task.description)
        desc_entry = tk.Entry(edit_window, textvariable=desc_var)
        desc_entry.pack(pady=5)

        tk.Label(edit_window, text="Nome (opcional):").pack()
        nome_var = StringVar(value=task.nome or "")
        nome_entry = tk.Entry(edit_window, textvariable=nome_var)
        nome_entry.pack(pady=5)

        dias_vars = {}
        if task.is_evento:
            tk.Label(edit_window, text="Dias da semana (para eventos):").pack()
            dias = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']
            for dia in dias:
                var = BooleanVar(value=(dia in task.dias_evento))
                dias_vars[dia] = var
                ttk.Checkbutton(edit_window, text=dia, variable=var).pack(anchor='w')

        def salvar():
            updated_task_data = {
                'description': desc_var.get().strip(),
                'priority': PriorityFlag(priority_var.get()).value,
                'nome': nome_var.get().strip() or None,
            }
            self.repository.update_task(task_id, updated_task_data)
            
            # Se for evento, a lógica é mais complexa e fica para um próximo passo (update_evento)
            
            self.view.update_view()
            edit_window.destroy()

        ttk.Button(edit_window, text="Salvar", command=salvar).pack(pady=10)

    def handle_apply_filters(self, filters):
        # O filtro de 'nome' (texto livre) deve buscar em todo o sistema,
        # ignorando a data selecionada no calendário.
        # Os outros filtros (status, tipo) podem ser combinados.
        
        # Armazena os filtros para serem usados em get_tasks_for_date
        self.active_filters = filters
        
        # Atualiza a view para refletir os resultados filtrados
        self.view.update_view()

    def handle_export_data(self):
        data = self.repository.get_all_data()
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Salvar dados como..."
        )
        if not filepath:
            return
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        messagebox.showinfo("Exportação Concluída", f"Dados salvos com sucesso em:\n{filepath}")

    def handle_create_backup(self):
        if not messagebox.askyesno("Confirmar Backup", "Deseja criar um backup interno de todos os dados?"):
            return
            
        data = self.repository.get_all_data()
        json_data = json.dumps(data).encode('utf-8')  #  Converte para bytes
        self.repository.create_backup(json_data)
        messagebox.showinfo("Backup Concluído", "Backup interno criado com sucesso.")

    def _db_to_task(self, db_row):
        # Converte tupla do DB para objeto Task
        # Colunas: 0=id, 1=description, 2=priority, 3=nome, 4=is_agendamento, 5=is_evento, 6=dias_evento, 7=date, 8=status
        priority = PriorityFlag(db_row[2]) if db_row[2] else None
        task = Task(
            description=db_row[1],
            priority=priority,
            nome=db_row[3],
            is_agendamento=db_row[4],
            is_evento=db_row[5],
            dias_evento=db_row[6],
            status=db_row[8]
        )
        task.id = db_row[0]
        task.date = db_row[7]
        return task
        
    def _db_to_evento(self, db_row):
        # Converte tupla do DB para objeto Evento
        evento = Evento(description=db_row[1], nome=db_row[2], dias_semana=db_row[3])
        evento.id = db_row[0]
        evento.ativo = db_row[4]
        return evento

    def update_task_status(self, task_key, done):
        date, description, nome = task_key
        status = 'concluída' if done else 'pendente'
        
        # Como a view não conhece o ID, precisamos buscá-lo.
        # Em um sistema real, a view deveria receber e guardar o ID.
        task_id = self.repository.find_task_id(date, description, nome)
        if task_id:
            self.repository.update_task_status(task_id, status)
        else:
            # Em um caso real, seria bom logar ou mostrar um erro.
            print(f"Alerta: Tarefa '{description}' não encontrada para a data {date} para atualizar status.")

