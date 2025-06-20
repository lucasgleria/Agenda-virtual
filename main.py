# main.py
import tkinter as tk
from model.db.repository import AgendaRepository
from controller.controller import AgendaController
from view.gui import AgendaView
from services.notification_service import NotificationScheduler

if __name__ == "__main__":
    root = tk.Tk()
    
    repository = AgendaRepository()
    
    # Inicia o agendador de notificações
    # Para testes, um intervalo menor pode ser usado, ex: 10 segundos
    scheduler = NotificationScheduler(repository, check_interval=3600)
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
