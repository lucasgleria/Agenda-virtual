import tkinter as tk
from tkinter import ttk
from view.theme.colors import ColorPalette

class NotificationPanel:
    """Painel de notificações para feedback visual das ações"""
    
    def __init__(self, parent):
        self.parent = parent
        self.notifications = []
        self.notification_frame = None
        self.is_showing = False
        
        # Criar frame de notificações
        self._create_notification_frame()
    
    def _create_notification_frame(self):
        """Criar frame para notificações"""
        self.notification_frame = tk.Frame(self.parent, 
                                          bg=ColorPalette.BACKGROUND['primary'],
                                          relief="flat",
                                          bd=0)
        
        # Posicionar no canto superior direito
        self.notification_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)
        
        # Inicialmente oculto
        self.notification_frame.pack_forget()
    
    def show_notification(self, message, notification_type="info", duration=3000):
        """
        Mostrar uma notificação
        
        Args:
            message (str): Mensagem da notificação
            notification_type (str): Tipo da notificação (success, error, warning, info)
            duration (int): Duração em milissegundos
        """
        # Criar notificação
        notification = self._create_notification_widget(message, notification_type)
        
        # Adicionar à lista
        self.notifications.append(notification)
        
        # Mostrar frame se não estiver visível
        if not self.is_showing:
            self.notification_frame.pack(fill="x", padx=10, pady=5)
            self.is_showing = True
        
        # Empacotar notificação
        notification.pack(fill="x", pady=(0, 5))
        
        # Animar entrada
        self._animate_notification_enter(notification)
        
        # Agendar remoção
        self.parent.after(duration, lambda: self._remove_notification(notification))
    
    def _create_notification_widget(self, message, notification_type):
        """Criar widget de notificação"""
        # Cores baseadas no tipo
        colors = {
            "success": {
                "bg": ColorPalette.SUCCESS['main'],
                "fg": ColorPalette.TEXT['inverse'],
                "icon": "✅"
            },
            "error": {
                "bg": ColorPalette.ERROR['main'],
                "fg": ColorPalette.TEXT['inverse'],
                "icon": "❌"
            },
            "warning": {
                "bg": ColorPalette.WARNING['main'],
                "fg": ColorPalette.TEXT['inverse'],
                "icon": "⚠️"
            },
            "info": {
                "bg": ColorPalette.PRIMARY['main'],
                "fg": ColorPalette.TEXT['inverse'],
                "icon": "ℹ️"
            }
        }
        
        color_config = colors.get(notification_type, colors["info"])
        
        # Frame da notificação
        notification = tk.Frame(self.notification_frame,
                               bg=color_config["bg"],
                               relief="flat",
                               bd=1,
                               highlightbackground=color_config["bg"],
                               highlightthickness=1)
        
        # Configurar grid
        notification.grid_columnconfigure(1, weight=1)
        
        # Ícone
        icon_label = tk.Label(notification, 
                             text=color_config["icon"],
                             bg=color_config["bg"],
                             fg=color_config["fg"],
                             font=("Segoe UI", 12))
        icon_label.grid(row=0, column=0, padx=(10, 5), pady=10)
        
        # Mensagem
        message_label = tk.Label(notification,
                                text=message,
                                bg=color_config["bg"],
                                fg=color_config["fg"],
                                font=("Segoe UI", 10),
                                wraplength=300,
                                justify=tk.LEFT)
        message_label.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=10)
        
        # Botão de fechar
        close_btn = tk.Button(notification,
                             text="✕",
                             bg=color_config["bg"],
                             fg=color_config["fg"],
                             font=("Segoe UI", 8, "bold"),
                             relief="flat",
                             bd=0,
                             command=lambda: self._remove_notification(notification))
        close_btn.grid(row=0, column=2, padx=(0, 5), pady=10)
        
        return notification
    
    def _animate_notification_enter(self, notification):
        """Animar entrada da notificação"""
        # Configurar posição inicial (fora da tela)
        notification.pack_configure(pady=(0, 5))
        
        # Animar entrada
        def animate():
            try:
                if notification.winfo_exists():
                    notification.pack_configure(pady=(5, 5))
            except:
                pass
        
        self.parent.after(50, animate)
    
    def _remove_notification(self, notification):
        """Remover notificação"""
        try:
            if notification.winfo_exists():
                notification.destroy()
                self.notifications.remove(notification)
                
                # Ocultar frame se não há mais notificações
                if not self.notifications:
                    self.notification_frame.pack_forget()
                    self.is_showing = False
        except:
            pass
    
    def show_success(self, message, duration=3000):
        """Mostrar notificação de sucesso"""
        self.show_notification(message, "success", duration)
    
    def show_error(self, message, duration=4000):
        """Mostrar notificação de erro"""
        self.show_notification(message, "error", duration)
    
    def show_warning(self, message, duration=3500):
        """Mostrar notificação de aviso"""
        self.show_notification(message, "warning", duration)
    
    def show_info(self, message, duration=3000):
        """Mostrar notificação informativa"""
        self.show_notification(message, "info", duration)
