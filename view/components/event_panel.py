import tkinter as tk
from tkinter import ttk

class EventPanel:
    def __init__(self, parent, on_cancel_evento):
        self.on_cancel_evento = on_cancel_evento
        self.controller = None

        self.frame = tk.Frame(parent, bd=2, relief="solid", highlightbackground="gray", highlightthickness=1)
        self.frame.pack(side='left', fill='y', padx=(10, 5), pady=10, ipadx=5)

        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(padx=10, pady=10, fill='both', expand=True)

    def set_controller(self, controller):
        self.controller = controller

    def update(self, eventos):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not any(e.ativo for e in eventos):
            self.frame.config(highlightbackground="gray", highlightthickness=1)
            ttk.Label(
                self.content_frame, 
                text="Sem eventos ativos.", 
                foreground="gray", 
                justify='center',
                font=("Arial", 10)
            ).pack(expand=True)
            return

        self.frame.config(highlightbackground="dodgerblue", highlightthickness=2)
        ttk.Label(
            self.content_frame, 
            text="Eventos Ativos", 
            foreground="dodgerblue", 
            font=("Arial", 12, "bold")
        ).pack(anchor='w', pady=(0, 10))

        for evento in eventos:
            if not evento.ativo:
                continue
                
            row = ttk.Frame(self.content_frame)
            row.pack(fill='x', pady=4)
            
            dias_str = ",".join(evento.dias_semana)
            nome_str = f"{evento.nome}: " if evento.nome else ""
            texto = f"[{dias_str.upper()}] {nome_str}{evento.description}"

            label = ttk.Label(row, text=texto, font=("Arial", 10), wraplength=180)
            label.pack(side='left', anchor='w', expand=True, fill='x')

            btn = ttk.Button(row, text="Encerrar", width=8, command=lambda e=evento: self.on_cancel_evento(e))
            btn.pack(side='right', padx=(5,0))