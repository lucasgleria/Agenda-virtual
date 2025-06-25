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
        if self.view is not None:
            self.view.set_controller(self)

    def add_task(self, date, description, priority, nome=None, is_agendamento=False, is_evento=False, dias_evento=None):
        # Determinar se é uma tarefa baseado nos outros campos
        is_tarefa = not (is_agendamento or is_evento)
        
        task_data = {
            'date': date,
            'description': description,
            'priority': PriorityFlag(priority).value if not is_evento else None,
            'nome': nome,
            'is_agendamento': is_agendamento,
            'is_evento': is_evento,
            'is_tarefa': is_tarefa,
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
        
        # Verificar se o evento foi encerrado
        if hasattr(evento, 'data_encerramento') and evento.data_encerramento:
            if hoje > evento.data_encerramento:
                print(f"[DEBUG] Controller: Evento '{evento.description}' foi encerrado em {evento.data_encerramento}, não gerando tarefas")
                return
        
        for i in range(90):
            data = hoje + timedelta(days=i)
            
            # Verificar se a data não ultrapassa a data de encerramento
            if hasattr(evento, 'data_encerramento') and evento.data_encerramento:
                if data > evento.data_encerramento:
                    break
            
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
    
    def get_tarefas_for_date(self, date):
        """Retornar apenas tarefas (não eventos, não agendamentos) para uma data."""
        tasks_db = self.repository.get_tarefas_by_date(date)
        return [self._db_to_task(t) for t in tasks_db]
    
    def get_agendamentos_for_date(self, date):
        """Retornar apenas agendamentos (não eventos, não tarefas) para uma data."""
        tasks_db = self.repository.get_agendamentos_by_date(date)
        return [self._db_to_task(t) for t in tasks_db]
    
    def get_event_tasks_for_date(self, date):
        """Retornar apenas TAREFAS de eventos (não agendamentos, não tarefas) para uma data."""
        tasks_db = self.repository.get_eventos_by_date(date)
        return [self._db_to_task(t) for t in tasks_db]

    def get_tasks(self):
        """Retornar todas as tarefas do banco de dados"""
        tasks_db = self.repository.get_all_tasks()
        return [self._db_to_task(t) for t in tasks_db]

    def get_all_active_events(self):
        """Retornar todos os objetos Evento que estão ativos."""
        eventos_db = self.repository.get_eventos_ativos()
        return [self._db_to_evento(e) for e in eventos_db]

    def get_upcoming_appointments_for_alert(self):
        """Busca agendamentos para o painel de alertas."""
        return self.repository.get_upcoming_appointments()

    def encerrar_evento(self, evento):
        """Encerrar um evento (desativar e limpar tarefas futuras)."""
        try:
            self.repository.deactivate_evento(evento.id)
            # Limpar tarefas futuras associadas a esse evento
            self.repository.delete_future_event_tasks(evento.id, datetime.today().date())
            
            # Atualizar a view
            if self.view is not None:
                self.view.update_view()
                
        except Exception as e:
            if self.view is not None:
                messagebox.showerror("Erro", f"Erro ao encerrar evento: {str(e)}")
            raise e

    def delete_task(self, date, task):
        if self.view is not None:
            if messagebox.askyesno("Confirmar exclusão", f"Excluir '{task.description}'?"):
                self.repository.delete_task_by_content(date, task.description, task.nome)
        else:
            # Em modo teste, apenas exclui sem confirmação
            self.repository.delete_task_by_content(date, task.description, task.nome)

    def edit_task(self, date, task):
        task_id = self.repository.find_task_id(date, task.description, task.nome)
        if not task_id:
            if self.view is not None:
                messagebox.showerror("Erro", "Não foi possível encontrar a tarefa para editar.")
            return
        if self.view is None:
            # Em modo teste, apenas executa update direto
            updated_task_data = {
                'description': task.description,
                'priority': task.priority.value if task.priority else None,
                'nome': task.nome
            }
            self.repository.update_task(task_id, updated_task_data)
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
        self.active_filters = filters
        if self.view is not None:
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
        
        # Determinar se é uma tarefa baseado nos outros campos
        is_agendamento = db_row[4]
        is_evento = db_row[5]
        is_tarefa = not (is_agendamento or is_evento)
        
        task = Task(
            description=db_row[1],
            priority=priority,
            nome=db_row[3],
            is_agendamento=is_agendamento,
            is_evento=is_evento,
            is_tarefa=is_tarefa,
            dias_evento=db_row[6],
            status=db_row[8]
        )
        task.id = db_row[0]
        task.date = db_row[7]
        return task
        
    def _db_to_evento(self, db_row):
        # Converte tupla do DB para objeto Evento
        # Colunas: 0=id, 1=description, 2=nome, 3=dias_semana, 4=ativo, 5=data_encerramento, 6=user_id
        evento = Evento(description=db_row[1], nome=db_row[2], dias_semana=db_row[3])
        evento.id = db_row[0]
        evento.ativo = db_row[4]
        evento.data_encerramento = db_row[5]
        return evento

    def update_task_status(self, task_key, done):
        date, description, nome = task_key
        status = 'concluída' if done else 'pendente'
        
        print(f"[DEBUG] Controller: update_task_status chamado")
        print(f"[DEBUG] Controller: date={date}, description={description}, nome={nome}")
        print(f"[DEBUG] Controller: status={status}")
        
        # Como a view não conhece o ID, precisamos buscá-lo.
        task_id = self.repository.find_task_id(date, description, nome)
        print(f"[DEBUG] Controller: task_id encontrado={task_id}")
        
        if task_id:
            print(f"[DEBUG] Controller: Atualizando status no repository...")
            self.repository.update_task_status(task_id, status)
            print(f"[DEBUG] Controller: Status atualizado no repository")
            
            # Verificar se a atualização foi bem-sucedida
            print(f"[DEBUG] Controller: Verificando se a atualização foi bem-sucedida...")
            updated_task = self.repository.get_task_by_id(task_id)
            if updated_task:
                print(f"[DEBUG] Controller: Tarefa atualizada - Status: {updated_task[8]}")
                
                # Se a tarefa foi marcada como concluída e é um evento ou agendamento
                if done and (updated_task[5] or updated_task[4]):  # is_evento or is_agendamento
                    print(f"[DEBUG] Controller: Tarefa concluída é evento/agendamento, removendo futuras ocorrências...")
                    self._handle_completed_recurring_item(updated_task)
            else:
                print(f"[DEBUG] Controller: Não foi possível verificar a tarefa atualizada")
            
            if self.view is not None:
                print(f"[DEBUG] Controller: Atualizando view...")
                self.view.update_view()
                print(f"[DEBUG] Controller: View atualizada")
        else:
            print(f"[DEBUG] Controller: Tarefa não encontrada no banco!")
            print(f"[DEBUG] Controller: Tentando buscar tarefas similares...")
            # Buscar tarefas similares para debug
            similar_tasks = self.repository.get_tasks_by_date(date)
            print(f"[DEBUG] Controller: Tarefas encontradas para a data {date}: {len(similar_tasks)}")
            for i, t in enumerate(similar_tasks):
                print(f"[DEBUG] Controller: Tarefa {i}: id={t[0]}, desc={t[1]}, nome={t[3]}, status={t[8]}")

    def _handle_completed_recurring_item(self, task):
        """Lidar com eventos e agendamentos concluídos, removendo futuras ocorrências"""
        try:
            task_date = task[7]  # date
            description = task[1]  # description
            nome = task[3]  # nome
            is_evento = task[5]  # is_evento
            is_agendamento = task[4]  # is_agendamento
            
            print(f"[DEBUG] Controller: Lidando com item recorrente concluído")
            print(f"[DEBUG] Controller: Data: {task_date}, Descrição: {description}, Nome: {nome}")
            print(f"[DEBUG] Controller: É evento: {is_evento}, É agendamento: {is_agendamento}")
            
            # Calcular a data do dia seguinte para remover futuras ocorrências
            from datetime import timedelta
            next_day = task_date + timedelta(days=1)
            
            if is_evento:
                # Para eventos, encerrar o evento a partir do dia seguinte
                print(f"[DEBUG] Controller: Encerrando evento a partir do dia seguinte...")
                self._encerrar_evento_concluido(description, nome, next_day)
            elif is_agendamento:
                # Para agendamentos, remover futuras ocorrências a partir do dia seguinte
                print(f"[DEBUG] Controller: Removendo futuras ocorrências do agendamento a partir do dia seguinte...")
                self._remover_futuras_ocorrencias_agendamento(description, nome, next_day)
                
        except Exception as e:
            print(f"[DEBUG] Controller: Erro ao lidar com item recorrente concluído: {e}")

    def _encerrar_evento_concluido(self, description, nome, completion_date):
        """Encerrar um evento quando uma de suas ocorrências é concluída"""
        try:
            # Buscar o evento na tabela de eventos
            evento = self.repository.find_evento_by_description(description, nome)
            if evento:
                print(f"[DEBUG] Controller: Evento encontrado, encerrando...")
                # Encerrar o evento a partir da data de conclusão
                self.repository.deactivate_evento_from_date(evento[0], completion_date)
                # Remover tarefas futuras do evento
                self.repository.delete_future_event_tasks(evento[0], completion_date)
                print(f"[DEBUG] Controller: Evento encerrado com sucesso")
            else:
                print(f"[DEBUG] Controller: Evento não encontrado na tabela de eventos")
        except Exception as e:
            print(f"[DEBUG] Controller: Erro ao encerrar evento: {e}")

    def _remover_futuras_ocorrencias_agendamento(self, description, nome, completion_date):
        """Remover futuras ocorrências de um agendamento quando concluído"""
        try:
            # Remover todas as ocorrências futuras do agendamento
            self.repository.delete_future_agendamento_occurrences(description, nome, completion_date)
            print(f"[DEBUG] Controller: Futuras ocorrências do agendamento removidas")
        except Exception as e:
            print(f"[DEBUG] Controller: Erro ao remover futuras ocorrências do agendamento: {e}")

    def update_task(self, task, original_task=None):
        """Atualizar uma tarefa existente."""
        # Se não foi fornecida a tarefa original, usar a atual (para compatibilidade)
        if original_task is None:
            original_task = task
        
        # Encontrar o ID da tarefa usando os dados originais
        task_id = self.repository.find_task_id(original_task.date, original_task.description, original_task.nome)
        
        if not task_id:
            if self.view is not None:
                messagebox.showerror("Erro", "Não foi possível encontrar a tarefa para editar.")
            return
        
        # Preparar dados para atualização
        updated_task_data = {
            'description': task.description,
            'priority': task.priority.value if task.priority else None,
            'nome': task.nome
        }
        
        # Atualizar no repository
        self.repository.update_task(task_id, updated_task_data)
        
        # Atualizar a view
        if self.view is not None:
            self.view.update_view()

    def update_event(self, evento, original_evento=None):
        """Atualizar um evento existente."""
        # Se não foi fornecido o evento original, usar o atual (para compatibilidade)
        if original_evento is None:
            original_evento = evento
        
        # Verificar se o evento tem ID
        evento_id = original_evento.id if hasattr(original_evento, 'id') and original_evento.id else None
        
        if not evento_id:
            if self.view is not None:
                messagebox.showerror("Erro", "Evento não possui ID válido para edição.")
            return
        
        try:
            # 1. Atualizar o evento na tabela de eventos
            evento_data = {
                'description': evento.description,
                'nome': evento.nome,
                'dias_semana': evento.dias_semana
            }
            self.repository.update_event(evento_id, evento_data)
            
            # 2. Deletar todas as tarefas futuras associadas a este evento
            self.repository.delete_future_event_tasks(evento_id, datetime.today().date())
            
            # 3. Recriar as tarefas futuras com os novos dados do evento
            self.gerar_tarefas_evento(evento)
            
            # 4. Atualizar a view
            if self.view is not None:
                self.view.update_view()
                
        except Exception as e:
            if self.view is not None:
                messagebox.showerror("Erro", f"Erro ao atualizar evento: {str(e)}")
            raise e

    def update_agendamento(self, agendamento, original_agendamento=None):
        """Atualizar um agendamento existente."""
        # Para agendamentos, tratamos como uma tarefa normal
        self.update_task(agendamento, original_agendamento)

    def delete_event(self, event_id):
        self.repository.delete_event(event_id)
        if self.view is not None:
            self.view.update_view()

    def delete_agendamento(self, agendamento):
        """Deletar um agendamento."""
        # Para agendamentos, tratamos como uma tarefa normal
        self.delete_task(agendamento.date, agendamento)

    def get_eventos_ativos_for_global_editor(self):
        """Retornar eventos ativos (objetos Evento) para o painel global."""
        eventos_db = self.repository.get_eventos_ativos()
        return [self._db_to_evento(e) for e in eventos_db]

    def cleanup_old_tasks(self):
        """Limpar tarefas antigas de eventos encerrados."""
        try:
            deleted_count = self.repository.cleanup_old_event_tasks()
            print(f"[DEBUG] Controller: {deleted_count} tarefas antigas de eventos removidas")
            return deleted_count
        except Exception as e:
            print(f"[DEBUG] Controller: Erro ao limpar tarefas antigas: {e}")
            return 0

