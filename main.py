# main.py
import tkinter as tk
from model.db.repository import AgendaRepository
from controller.controller import AgendaController
from view.gui import AgendaView
from services.notification_service import NotificationScheduler
import logging

def main():
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s',
        handlers=[
            logging.FileHandler('notificacao_debug.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # Inicializar banco de dados
    init_database()
    
    # Criar repository e controller
    repository = AgendaRepository()
    controller = AgendaController(repository, None)
    
    # Limpar tarefas antigas de eventos encerrados
    try:
        deleted_count = controller.cleanup_old_tasks()
        if deleted_count > 0:
            print(f"Limpeza automática: {deleted_count} tarefas antigas removidas")
    except Exception as e:
        print(f"Erro na limpeza automática: {e}")
    
    # Criar view
    view = AgendaView(controller)
    controller.view = view
    
    # Iniciar aplicação
    view.run()

if __name__ == "__main__":
    root = tk.Tk()
    
    repository = AgendaRepository()
    
    # Inicia o agendador de notificações
    # Para testes, um intervalo menor pode ser usado, ex: 10 segundos
    scheduler = NotificationScheduler(repository, check_interval=10)
    scheduler.start()

    view = AgendaView(root)
    controller = AgendaController(repository, view)

    def on_closing():
        """Função para ser chamada quando a janela for fechada."""
        print("Fechando a aplicação...")
        scheduler.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
