import tkinter as tk
from tkinter import ttk
from datetime import datetime, date, timedelta
from collections import defaultdict

class AlertPanel:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bd=2, relief="solid", highlightbackground="gray", highlightthickness=1)
        self.frame.pack(side='right', fill='y', padx=(5, 10), pady=10, ipadx=5)

        # O content_frame agora conterá múltiplos widgets
        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(padx=10, pady=10, fill='both', expand=True)

    def update(self, appointments):
        """Atualiza o painel com uma lista de agendamentos futuros, com formatação melhorada."""
        # 1. Limpar o conteúdo anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not appointments:
            self.frame.config(highlightbackground="gray", highlightthickness=1)
            ttk.Label(
                self.content_frame, 
                text="Sem agendamentos\nnos próximos 15 dias.", 
                foreground="gray", 
                justify='center',
                font=("Arial", 10)
            ).pack(expand=True)
            return

        # 2. Configurar o painel para o modo de alerta
        self.frame.config(highlightbackground="red", highlightthickness=2)
        ttk.Label(
            self.content_frame, 
            text="Agendamentos Próximos", 
            foreground="red", 
            font=("Arial", 12, "bold")
        ).pack(anchor='w', pady=(0, 10))

        # 3. Agrupar agendamentos por data
        grouped_appointments = defaultdict(list)
        for appt in appointments:
            grouped_appointments[appt[3]].append(appt)

        # 4. Exibir os agendamentos agrupados
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        for appt_date in sorted(grouped_appointments.keys()):
            # Formatar o cabeçalho da data
            if appt_date == today:
                date_str = "Hoje"
            elif appt_date == tomorrow:
                date_str = "Amanhã"
            else:
                date_str = appt_date.strftime('%d/%m/%Y')
            
            ttk.Label(
                self.content_frame, 
                text=date_str, 
                font=("Arial", 10, "bold"),
            ).pack(anchor='w', pady=(8, 2))
            
            ttk.Separator(self.content_frame, orient='horizontal').pack(fill='x', anchor='w', pady=(0, 5))

            for appt in grouped_appointments[appt_date]:
                desc, _, nome, _ = appt
                text = f"• {nome}: {desc}" if nome else f"• {desc}"
                
                ttk.Label(
                    self.content_frame,
                    text=text,
                    font=("Arial", 10),
                    wraplength=220 # Ajuste para a largura do painel
                ).pack(anchor='w', padx=(5, 0))
