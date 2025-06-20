from plyer import notification
import threading
import time

def send_notification(title, message):
    """
    Envia uma notificação para o sistema operacional.
    """
    try:
        notification.notify(
            title=title,
            message=message,
            app_name='Agenda Virtual',
            timeout=10  # A notificação desaparecerá após 10 segundos
        )
        print(f"Notificação enviada: '{title}'")
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")
        # Em um app real, poderíamos ter um fallback para um alerta na UI 

class NotificationScheduler:
    def __init__(self, repository, check_interval=3600): # Default: verifica a cada hora
        self.repository = repository
        self.check_interval = check_interval
        self._timer = None
        self._running = False
        self.notified_ids = set() # Rastreia IDs notificados nesta sessão para evitar spam

    def _check_schedules(self):
        """Verifica os agendamentos e envia notificações."""
        if not self._running:
            return

        print("Scheduler: Verificando agendamentos...")
        try:
            schedules = self.repository.get_upcoming_schedules()
            for schedule in schedules:
                task_id, description, nome, date = schedule
                if task_id not in self.notified_ids:
                    title = f"Lembrete: {nome or description}"
                    message = f"Você tem um agendamento para amanhã ({date.strftime('%d/%m')}): {description}."
                    send_notification(title, message)
                    self.notified_ids.add(task_id)
        except Exception as e:
            print(f"Erro no agendador de notificações: {e}")
        
        # Reagenda a próxima verificação
        if self._running:
            self._timer = threading.Timer(self.check_interval, self._check_schedules)
            self._timer.start()

    def start(self):
        """Inicia o scheduler em uma thread separada."""
        if not self._running:
            self._running = True
            print("Agendador de notificações iniciado.")
            self._check_schedules() # Executa a primeira verificação imediatamente

    def stop(self):
        """Para o scheduler."""
        self._running = False
        if self._timer:
            self._timer.cancel()
        print("Agendador de notificações parado.") 