from .database import get_db_connection, release_db_connection
from datetime import datetime, timedelta
import logging
import json

class AgendaRepository:
    def add_task(self, task_data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO tasks (description, priority, nome, is_agendamento, is_evento, dias_evento, date, status, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        task_data['description'],
                        task_data.get('priority'),
                        task_data.get('nome'),
                        task_data.get('is_agendamento', False),
                        task_data.get('is_evento', False),
                        task_data.get('dias_evento'),
                        task_data['date'],
                        'pendente',
                        1  #  Hardcoded para o usuário 1 por enquanto
                    )
                )
                task_id = cur.fetchone()[0]
                conn.commit()
                return task_id
        except Exception as e:
            logging.error(f"Erro ao adicionar tarefa: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if conn:
                release_db_connection(conn)

    def get_tasks_by_date(self, date):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM tasks WHERE date = %s;", (date,))
                tasks = cur.fetchall()
                return tasks
        finally:
            release_db_connection(conn)
            
    def add_evento(self, evento_data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO eventos (description, nome, dias_semana, user_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        evento_data['description'],
                        evento_data.get('nome'),
                        evento_data['dias_semana'],
                        1  # Hardcoded para o usuário 1 por enquanto
                    )
                )
                evento_id = cur.fetchone()[0]
                conn.commit()
                return evento_id
        except Exception as e:
            logging.error(f"Erro ao adicionar evento: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if conn:
                release_db_connection(conn)

    def get_eventos_ativos(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM eventos WHERE ativo = TRUE;")
                eventos = cur.fetchall()
                return eventos
        finally:
            release_db_connection(conn)

    def deactivate_evento(self, evento_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE eventos SET ativo = FALSE, data_encerramento = %s WHERE id = %s;",
                    (datetime.today().date(), evento_id)
                )
                conn.commit()
        except Exception as e:
            logging.error(f"Erro ao desativar evento: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                release_db_connection(conn)
    
    def delete_future_event_tasks(self, evento_id, from_date):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM tasks WHERE evento_id = %s AND date > %s;",
                    (evento_id, from_date)
                )
                conn.commit()
        except Exception as e:
            logging.error(f"Erro ao deletar tarefas de evento futuro: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                release_db_connection(conn)

    def delete_task_by_content(self, date, description, nome):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                # Lógica para deletar baseado no conteúdo, já que a view não tem ID
                if nome:
                    cur.execute(
                        "DELETE FROM tasks WHERE date = %s AND description = %s AND nome = %s;",
                        (date, description, nome)
                    )
                else:
                    cur.execute(
                        "DELETE FROM tasks WHERE date = %s AND description = %s AND nome IS NULL;",
                        (date, description)
                    )
                conn.commit()
        except Exception as e:
            logging.error(f"Erro ao deletar tarefa por conteúdo: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                release_db_connection(conn)

    def update_task(self, task_id, task_data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE tasks
                    SET description = %s, priority = %s, nome = %s
                    WHERE id = %s;
                    """,
                    (
                        task_data['description'],
                        task_data['priority'],
                        task_data.get('nome'),
                        task_id
                    )
                )
                conn.commit()
        except Exception as e:
            logging.error(f"Erro ao atualizar tarefa: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                release_db_connection(conn)

    def update_task_status(self, task_id, status):
        """Atualiza o status de uma tarefa (ex: 'pendente', 'concluída')."""
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE tasks SET status = %s WHERE id = %s;",
                    (status, task_id)
                )
                conn.commit()
        except Exception as e:
            logging.error(f"Erro ao atualizar status da tarefa: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                release_db_connection(conn)

    def find_task_id(self, date, description, nome):
        """Encontra o ID de uma tarefa com base no seu conteúdo."""
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                if nome:
                    cur.execute(
                        "SELECT id FROM tasks WHERE date = %s AND description = %s AND nome = %s LIMIT 1;",
                        (date, description, nome)
                    )
                else:
                    cur.execute(
                        "SELECT id FROM tasks WHERE date = %s AND description = %s AND nome IS NULL LIMIT 1;",
                        (date, description)
                    )
                result = cur.fetchone()
                return result[0] if result else None
        finally:
            release_db_connection(conn)

    def get_all_data(self):
        """Busca todas as tarefas e eventos para exportação."""
        conn = get_db_connection()
        data = {'tasks': [], 'eventos': []}
        try:
            with conn.cursor() as cur:
                # Exportar tarefas
                cur.execute("SELECT id, description, priority, nome, is_agendamento, is_evento, dias_evento, date, status, evento_id, user_id FROM tasks;")
                tasks_db = cur.fetchall()
                for t in tasks_db:
                    data['tasks'].append({
                        'id': t[0], 'description': t[1], 'priority': t[2], 'nome': t[3],
                        'is_agendamento': t[4], 'is_evento': t[5], 'dias_evento': t[6],
                        'date': t[7].strftime('%Y-%m-%d'), 'status': t[8], 'evento_id': t[9], 'user_id': t[10]
                    })
                
                # Exportar eventos
                cur.execute("SELECT id, description, nome, dias_semana, ativo, data_encerramento, user_id FROM eventos;")
                eventos_db = cur.fetchall()
                for e in eventos_db:
                    data['eventos'].append({
                        'id': e[0], 'description': e[1], 'nome': e[2], 'dias_semana': e[3],
                        'ativo': e[4], 'data_encerramento': e[5].strftime('%Y-%m-%d') if e[5] else None, 'user_id': e[6]
                    })
            return data
        finally:
            if conn:
                release_db_connection(conn)

    def create_backup(self, json_data):
        """Salva um backup na tabela 'backups'."""
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO backups (user_id, arquivo) VALUES (%s, %s);",
                    (1, json_data) # Hardcoded user_id 1
                )
                conn.commit()
        except Exception as e:
            logging.error(f"Erro ao criar backup: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                release_db_connection(conn)

    def get_tasks_with_filters(self, date, filters):
        """Busca tarefas com base em filtros dinâmicos."""
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                query_conditions = []
                params = []

                # Filtro por nome (busca textual)
                if filters.get('nome'):
                    query_conditions.append("description ILIKE %s")
                    params.append(f"%{filters['nome']}%")
                else:
                    # Se não houver busca por nome, filtra pela data selecionada
                    query_conditions.append("date = %s")
                    params.append(date)

                # Filtro por status
                status_filter = filters.get('status')
                if status_filter and status_filter != 'Todos':
                    query_conditions.append("status = %s")
                    params.append(status_filter.lower())

                # Filtro por tipo de tarefa
                tipo_filter = filters.get('tipo')
                if tipo_filter and tipo_filter != 'Todos':
                    if tipo_filter == 'Tarefa':
                        query_conditions.append("is_agendamento = FALSE AND is_evento = FALSE")
                    elif tipo_filter == 'Agendamento':
                        query_conditions.append("is_agendamento = TRUE")
                    elif tipo_filter == 'Evento':
                        query_conditions.append("is_evento = TRUE")

                # Constrói a query final
                if not query_conditions:
                    # Fallback para buscar todas as tarefas do dia se nenhum filtro for válido
                    base_query = "SELECT * FROM tasks WHERE date = %s;"
                    params = [date]
                else:
                    base_query = "SELECT * FROM tasks WHERE " + " AND ".join(query_conditions) + ";"
                
                cur.execute(base_query, tuple(params))
                tasks = cur.fetchall()
                return tasks
        finally:
            release_db_connection(conn)

    def get_upcoming_schedules(self):
        """Busca agendamentos pendentes que ocorrerão no dia seguinte."""
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                tomorrow = datetime.now().date() + timedelta(days=1)
                
                query = """
                    SELECT id, description, nome, date FROM tasks
                    WHERE is_agendamento = TRUE
                      AND status = 'pendente'
                      AND date = %s;
                """
                cur.execute(query, (tomorrow,))
                schedules = cur.fetchall()
                return schedules
        finally:
            if conn:
                release_db_connection(conn)

    def get_upcoming_appointments(self, days=15):
        """Busca agendamentos pendentes para os próximos X dias."""
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                today = datetime.now().date()
                future_date = today + timedelta(days=days)
                
                query = """
                    SELECT description, priority, nome, date
                    FROM tasks
                    WHERE is_agendamento = TRUE
                      AND status = 'pendente'
                      AND date >= %s AND date <= %s
                    ORDER BY date;
                """
                cur.execute(query, (today, future_date))
                appointments = cur.fetchall()
                return appointments
        finally:
            if conn:
                release_db_connection(conn) 