import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from typing import List, Optional, Callable
from model.task import Task
from model.evento import Evento
from copy import copy

class GlobalEditorPanel(ttk.Frame):
    """Painel global de edição que cobre toda a interface."""
    
    def __init__(self, parent, controller, on_close_callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.on_close_callback = on_close_callback
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.tarefas = []
        self.eventos = []
        self.agendamentos = []
        self.selected_item = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configurar interface do usuário."""
        # Frame principal simples
        self.configure(relief="raised", borderwidth=2)
        
        # Título
        title_frame = ttk.Frame(self)
        title_frame.pack(fill='x', padx=10, pady=10)
        
        title_label = ttk.Label(title_frame, text="✏️ Modo Editor Global", 
                               font=("Arial", 18, "bold"))
        title_label.pack(side='left')
        
        # Botão de fechar
        close_button = ttk.Button(title_frame, text="❌ Fechar Editor", 
                                 command=self._close_editor)
        close_button.pack(side='right')
        
        # Label de teste para verificar se o painel está funcionando
        test_label = ttk.Label(self, text="Painel Global Carregado - Aguardando dados...", 
                              font=("Arial", 12))
        test_label.pack(pady=10)
        
        # Notebook simples
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de Tarefas
        self.tarefas_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tarefas_frame, text="📝 Tarefas")
        self._setup_tarefas_tab()
        
        # Aba de Eventos
        self.eventos_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.eventos_frame, text="📅 Eventos")
        self._setup_eventos_tab()
        
        # Aba de Agendamentos
        self.agendamentos_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.agendamentos_frame, text="📋 Agendamentos")
        self._setup_agendamentos_tab()
    
    def _setup_tarefas_tab(self):
        """Configurar aba de tarefas com cards editáveis."""
        # Frame simples para as tarefas
        self.tarefas_scrollable_frame = ttk.Frame(self.tarefas_frame)
        self.tarefas_scrollable_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Label de teste para tarefas
        test_label = ttk.Label(self.tarefas_scrollable_frame, text="Aba de Tarefas - Aguardando dados...", 
                              font=("Arial", 10))
        test_label.pack(pady=5)
    
    def _setup_eventos_tab(self):
        """Configurar aba de eventos com cards editáveis."""
        # Frame simples para os eventos
        self.eventos_scrollable_frame = ttk.Frame(self.eventos_frame)
        self.eventos_scrollable_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Label de teste para eventos
        test_label = ttk.Label(self.eventos_scrollable_frame, text="Aba de Eventos - Aguardando dados...", 
                              font=("Arial", 10))
        test_label.pack(pady=5)
    
    def _setup_agendamentos_tab(self):
        """Configurar aba de agendamentos com cards editáveis."""
        # Frame simples para os agendamentos
        self.agendamentos_scrollable_frame = ttk.Frame(self.agendamentos_frame)
        self.agendamentos_scrollable_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Label de teste para agendamentos
        test_label = ttk.Label(self.agendamentos_scrollable_frame, text="Aba de Agendamentos - Aguardando dados...", 
                              font=("Arial", 10))
        test_label.pack(pady=5)
    
    def update_data(self, tarefas, eventos, agendamentos):
        """Atualizar dados do painel."""
        print(f"[GlobalEditor] === INICIANDO UPDATE_DATA ===")
        print(f"[GlobalEditor] Atualizando dados - Tarefas: {len(tarefas)}, Eventos: {len(eventos)}, Agendamentos: {len(agendamentos)}")
        
        # Verificar se os dados são válidos
        if tarefas:
            print(f"[GlobalEditor] Primeira tarefa: {tarefas[0].description if tarefas[0].description else 'Sem descrição'}")
        if eventos:
            print(f"[GlobalEditor] Primeiro evento: {eventos[0].description if eventos[0].description else 'Sem descrição'}")
            print(f"[GlobalEditor] Tipo do primeiro evento: {type(eventos[0])}")
            print(f"[GlobalEditor] ID do primeiro evento: {getattr(eventos[0], 'id', 'N/A')}")
            print(f"[GlobalEditor] Dias do primeiro evento: {getattr(eventos[0], 'dias_semana', 'N/A')}")
        if agendamentos:
            print(f"[GlobalEditor] Primeiro agendamento: {agendamentos[0].description if agendamentos[0].description else 'Sem descrição'}")
        
        self.tarefas = tarefas
        self.eventos = eventos
        self.agendamentos = agendamentos
        
        # Forçar atualização do layout
        self.update_idletasks()
        
        print(f"[GlobalEditor] Chamando refresh methods...")
        self._refresh_tarefas()
        self._refresh_eventos()
        self._refresh_agendamentos()
        
        # Forçar redraw
        self.update_idletasks()
        print(f"[GlobalEditor] === UPDATE_DATA CONCLUÍDO ===")
    
    def _refresh_tarefas(self):
        """Atualizar lista de tarefas com cards editáveis."""
        print(f"[GlobalEditor] Refreshing tarefas - {len(self.tarefas)} tarefas")
        for widget in self.tarefas_scrollable_frame.winfo_children():
            widget.destroy()
        for i, tarefa in enumerate(self.tarefas):
            print(f"[GlobalEditor] Criando card para tarefa {i}: {tarefa.description}")
            self._create_tarefa_card(tarefa, i)
    
    def _create_tarefa_card(self, tarefa, index):
        """Criar um card de tarefa que ocupa todo o espaço disponível"""
        card_frame = ttk.Frame(self.tarefas_scrollable_frame)
        card_frame.grid(row=index, column=0, sticky="ew", padx=10, pady=5)
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.configure(relief="solid", borderwidth=1)  # Borda visível para debug
        
        # Título
        title_label = ttk.Label(card_frame, text=tarefa.description, font=("Segoe UI", 12, "bold"), wraplength=400)
        title_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Nome
        if tarefa.nome:
            nome_label = ttk.Label(card_frame, text=f"👤 {tarefa.nome}", font=("Segoe UI", 10), foreground="gray")
            nome_label.grid(row=1, column=0, sticky="w", padx=5)
        
        # Data
        if tarefa.date:
            date_label = ttk.Label(card_frame, text=f"📅 {tarefa.date.strftime('%d/%m/%Y')}", font=("Segoe UI", 10), foreground="gray")
            date_label.grid(row=2, column=0, sticky="w", padx=5)
        
        # Status
        status = "✅ Concluída" if tarefa.status == "concluída" else "⏳ Pendente"
        status_label = ttk.Label(card_frame, text=status, font=("Segoe UI", 10))
        status_label.grid(row=3, column=0, sticky="w", padx=5)
        
        # Prioridade
        prioridade = tarefa.priority.value if tarefa.priority else "Normal"
        prioridade_label = ttk.Label(card_frame, text=f"Prioridade: {prioridade}", font=("Segoe UI", 10))
        prioridade_label.grid(row=4, column=0, sticky="w", padx=5)
        
        # Botões de ação
        actions_frame = ttk.Frame(card_frame)
        actions_frame.grid(row=5, column=0, sticky="ew", pady=(5, 5), padx=5)
        actions_frame.grid_columnconfigure(2, weight=1)  # Espaço flexível à direita
        
        edit_btn = ttk.Button(actions_frame, text="✏️ Editar", command=lambda t=tarefa: self._abrir_modal_edicao_tarefa(t))
        edit_btn.grid(row=0, column=0, padx=(0, 5))
        delete_btn = ttk.Button(actions_frame, text="🗑️ Excluir", command=lambda t=tarefa: self._confirmar_exclusao_tarefa(t))
        delete_btn.grid(row=0, column=1, padx=(0, 5))
    
    def _refresh_eventos(self):
        """Atualizar lista de eventos com cards editáveis."""
        print(f"[GlobalEditor] Refreshing eventos - {len(self.eventos)} eventos")
        for widget in self.eventos_scrollable_frame.winfo_children():
            widget.destroy()
        for i, evento in enumerate(self.eventos):
            print(f"[GlobalEditor] Criando card para evento {i}: {evento.description}")
            self._create_evento_card(evento, i)
    
    def _create_evento_card(self, evento, index):
        """Cria um card para um objeto Evento que ocupa todo o espaço disponível."""
        card_frame = ttk.Frame(self.eventos_scrollable_frame)
        card_frame.grid(row=index, column=0, sticky="ew", padx=10, pady=5)
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.configure(relief="solid", borderwidth=1)
        
        # Título
        title_label = ttk.Label(card_frame, text=evento.description, font=("Segoe UI", 12, "bold"), wraplength=400)
        title_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Nome
        if evento.nome:
            nome_label = ttk.Label(card_frame, text=f"👤 {evento.nome}", font=("Segoe UI", 10), foreground="gray")
            nome_label.grid(row=1, column=0, sticky="w", padx=5)
        
        # Status do evento
        status = "✅ Ativo" if evento.ativo else "❌ Encerrado"
        status_label = ttk.Label(card_frame, text=status, font=("Segoe UI", 10))
        status_label.grid(row=2, column=0, sticky="w", padx=5)
        
        # Dias do evento
        if hasattr(evento, 'dias_semana') and evento.dias_semana:
            dias_text = ", ".join(evento.dias_semana)
            dias_label = ttk.Label(card_frame, text=f"📅 Dias: {dias_text}", font=("Segoe UI", 10), foreground="gray")
            dias_label.grid(row=3, column=0, sticky="w", padx=5)
        
        # Botões de ação
        actions_frame = ttk.Frame(card_frame)
        actions_frame.grid(row=4, column=0, sticky="ew", pady=(5, 5), padx=5)
        actions_frame.grid_columnconfigure(2, weight=1)  # Espaço flexível à direita
        
        edit_btn = ttk.Button(actions_frame, text="✏️ Editar", command=lambda e=evento: self._abrir_modal_edicao_evento(e))
        edit_btn.grid(row=0, column=0, padx=(0, 5))
        # O botão de exclusão agora encerra o evento
        delete_btn = ttk.Button(actions_frame, text="🗑️ Encerrar", command=lambda e=evento: self._confirmar_exclusao_evento(e))
        delete_btn.grid(row=0, column=1, padx=(0, 5))
    
    def _refresh_agendamentos(self):
        """Atualizar lista de agendamentos com cards editáveis."""
        print(f"[GlobalEditor] Refreshing agendamentos - {len(self.agendamentos)} agendamentos")
        for widget in self.agendamentos_scrollable_frame.winfo_children():
            widget.destroy()
        for i, agendamento in enumerate(self.agendamentos):
            print(f"[GlobalEditor] Criando card para agendamento {i}: {agendamento.description}")
            self._create_agendamento_card(agendamento, i)
    
    def _create_agendamento_card(self, agendamento, index):
        """Criar um card de agendamento que ocupa todo o espaço disponível"""
        card_frame = ttk.Frame(self.agendamentos_scrollable_frame)
        card_frame.grid(row=index, column=0, sticky="ew", padx=10, pady=5)
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.configure(relief="solid", borderwidth=1)  # Borda visível para debug
        
        # Título
        title_label = ttk.Label(card_frame, text=agendamento.description, font=("Segoe UI", 12, "bold"), wraplength=400)
        title_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Nome
        if agendamento.nome:
            nome_label = ttk.Label(card_frame, text=f"👤 {agendamento.nome}", font=("Segoe UI", 10), foreground="gray")
            nome_label.grid(row=1, column=0, sticky="w", padx=5)
        
        # Data
        if agendamento.date:
            date_label = ttk.Label(card_frame, text=f"📅 {agendamento.date.strftime('%d/%m/%Y')}", font=("Segoe UI", 10), foreground="gray")
            date_label.grid(row=2, column=0, sticky="w", padx=5)
        
        # Status
        status = "✅ Concluído" if agendamento.status == "concluída" else "⏳ Pendente"
        status_label = ttk.Label(card_frame, text=status, font=("Segoe UI", 10))
        status_label.grid(row=3, column=0, sticky="w", padx=5)
        
        # Prioridade
        prioridade = agendamento.priority.value if agendamento.priority else "Normal"
        prioridade_label = ttk.Label(card_frame, text=f"Prioridade: {prioridade}", font=("Segoe UI", 10))
        prioridade_label.grid(row=4, column=0, sticky="w", padx=5)
        
        # Botões de ação
        actions_frame = ttk.Frame(card_frame)
        actions_frame.grid(row=5, column=0, sticky="ew", pady=(5, 5), padx=5)
        actions_frame.grid_columnconfigure(2, weight=1)  # Espaço flexível à direita
        
        edit_btn = ttk.Button(actions_frame, text="✏️ Editar", command=lambda a=agendamento: self._abrir_modal_edicao_agendamento(a))
        edit_btn.grid(row=0, column=0, padx=(0, 5))
        delete_btn = ttk.Button(actions_frame, text="🗑️ Excluir", command=lambda a=agendamento: self._confirmar_exclusao_agendamento(a))
        delete_btn.grid(row=0, column=1, padx=(0, 5))
    
    def _filter_tarefas(self):
        """Filtrar tarefas."""
        # Implementar filtros
        pass
    
    def _filter_eventos(self):
        """Filtrar eventos."""
        # Implementar filtros
        pass
    
    def _filter_agendamentos(self):
        """Filtrar agendamentos."""
        # Implementar filtros
        pass
    
    def _on_tab_changed(self, event):
        """Callback para mudança de aba."""
        pass
    
    def _on_tarefa_select(self, event):
        """Callback para seleção de tarefa."""
        pass
    
    def _on_tarefa_double_click(self, event):
        """Callback para duplo clique em tarefa."""
        item_id = self.tarefas_tree.focus()
        if not item_id:
            return
        col = self.tarefas_tree.identify_column(event.x)
        col_num = int(col.replace('#', ''))
        if col_num != 6:  # Coluna "Ações"
            return
        values = self.tarefas_tree.item(item_id, 'values')
        index = self.tarefas_tree.index(item_id)
        tarefa = self.tarefas[index]
        # Detectar se clicou em Editar ou Excluir
        x_col = self.tarefas_tree.bbox(item_id, col_num-1)[0]
        click_x = event.x - x_col
        # Aproximação: metade esquerda = editar, metade direita = excluir
        col_width = self.tarefas_tree.column('Ações', width=None)
        if click_x < col_width // 2:
            self._abrir_modal_edicao_tarefa(tarefa)
        else:
            self._confirmar_exclusao_tarefa(tarefa)

    def _abrir_modal_edicao_tarefa(self, tarefa):
        """Abrir modal para editar tarefa."""
        modal = tk.Toplevel(self)
        modal.title("Editar Tarefa")
        modal.transient(self)
        modal.grab_set()
        tk.Label(modal, text="Descrição:").pack()
        desc_var = tk.StringVar(value=tarefa.description)
        desc_entry = tk.Entry(modal, textvariable=desc_var)
        desc_entry.pack()
        tk.Label(modal, text="Nome:").pack()
        nome_var = tk.StringVar(value=tarefa.nome)
        nome_entry = tk.Entry(modal, textvariable=nome_var)
        nome_entry.pack()
        def salvar():
            # Criar uma cópia da tarefa com os novos dados
            tarefa_editada = copy(tarefa)
            tarefa_editada.description = desc_var.get()
            tarefa_editada.nome = nome_var.get()
            
            if self.controller:
                try:
                    self.controller.update_task(tarefa_editada, tarefa)  # Passar tarefa original como segundo parâmetro
                    # Atualizar o objeto original também
                    tarefa.description = tarefa_editada.description
                    tarefa.nome = tarefa_editada.nome
                    self._refresh_tarefas()
                    modal.destroy()
                    messagebox.showinfo("Sucesso", "Tarefa editada com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao salvar tarefa: {str(e)}")
            else:
                modal.destroy()
        tk.Button(modal, text="Salvar", command=salvar).pack(pady=10)
        tk.Button(modal, text="Cancelar", command=modal.destroy).pack()

    def _confirmar_exclusao_tarefa(self, tarefa):
        """Confirmação visual para exclusão de tarefa."""
        if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir a tarefa '{tarefa.description}'?"):
            if self.controller:
                self.controller.delete_task(tarefa.date, tarefa)
            self._refresh_tarefas()
            messagebox.showinfo("Excluído", "Tarefa excluída com sucesso!")
    
    def _on_evento_select(self, event):
        """Callback para seleção de evento."""
        pass
    
    def _on_evento_double_click(self, event):
        """Callback para duplo clique em evento."""
        item_id = self.eventos_tree.focus()
        if not item_id:
            return
        col = self.eventos_tree.identify_column(event.x)
        col_num = int(col.replace('#', ''))
        if col_num != 6:  # Coluna "Ações"
            return
        index = self.eventos_tree.index(item_id)
        evento = self.eventos[index]
        x_col = self.eventos_tree.bbox(item_id, col_num-1)[0]
        click_x = event.x - x_col
        col_width = self.eventos_tree.column('Ações', width=None)
        if click_x < col_width // 2:
            self._abrir_modal_edicao_evento(evento)
        else:
            self._confirmar_exclusao_evento(evento)

    def _abrir_modal_edicao_evento(self, evento):
        """Abrir modal para editar evento."""
        modal = tk.Toplevel(self)
        modal.title("Editar Evento")
        modal.transient(self)
        modal.grab_set()
        modal.geometry("400x500")
        
        # Frame principal
        main_frame = ttk.Frame(modal, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(main_frame, text="Editar Evento", font=("Segoe UI", 14, "bold")).pack(pady=(0, 20))
        
        # Descrição
        ttk.Label(main_frame, text="Descrição:", font=("Segoe UI", 10, "bold")).pack(anchor='w')
        desc_var = tk.StringVar(value=evento.description)
        desc_entry = ttk.Entry(main_frame, textvariable=desc_var, font=("Segoe UI", 10))
        desc_entry.pack(fill='x', pady=(5, 15))
        
        # Nome
        ttk.Label(main_frame, text="Nome:", font=("Segoe UI", 10, "bold")).pack(anchor='w')
        nome_var = tk.StringVar(value=evento.nome or "")
        nome_entry = ttk.Entry(main_frame, textvariable=nome_var, font=("Segoe UI", 10))
        nome_entry.pack(fill='x', pady=(5, 15))
        
        # Dias da semana
        ttk.Label(main_frame, text="Dias da Semana:", font=("Segoe UI", 10, "bold")).pack(anchor='w')
        dias_frame = ttk.Frame(main_frame)
        dias_frame.pack(fill='x', pady=(5, 15))
        
        dias_semana = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']
        dias_vars = {}
        
        # Criar checkboxes para cada dia
        for i, dia in enumerate(dias_semana):
            var = tk.BooleanVar(value=dia in evento.dias_semana)
            dias_vars[dia] = var
            cb = ttk.Checkbutton(dias_frame, text=dia, variable=var)
            cb.grid(row=0, column=i, padx=5, pady=2)
        
        # Frame para botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(20, 0))
        
        def salvar():
            # Validar se pelo menos um dia foi selecionado
            dias_selecionados = [dia for dia, var in dias_vars.items() if var.get()]
            if not dias_selecionados:
                messagebox.showerror("Erro", "Selecione pelo menos um dia da semana!")
                return
            
            # Validar campos obrigatórios
            descricao = desc_var.get().strip()
            if not descricao:
                messagebox.showerror("Erro", "A descrição é obrigatória!")
                return
            
            # Criar uma cópia do evento com os novos dados
            evento_editado = copy(evento)
            evento_editado.description = descricao
            evento_editado.nome = nome_var.get().strip() or None
            evento_editado.dias_semana = dias_selecionados
            
            if self.controller:
                try:
                    self.controller.update_event(evento_editado, evento)
                    # Atualizar o objeto original também
                    evento.description = evento_editado.description
                    evento.nome = evento_editado.nome
                    evento.dias_semana = evento_editado.dias_semana
                    self._refresh_eventos()
                    modal.destroy()
                    messagebox.showinfo("Sucesso", "Evento editado com sucesso!\nAs tarefas futuras foram atualizadas automaticamente.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao salvar evento: {str(e)}")
            else:
                modal.destroy()
        
        def cancelar():
            modal.destroy()
        
        # Botões
        ttk.Button(button_frame, text="Salvar", command=salvar, style="Success.TButton").pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Cancelar", command=cancelar).pack(side='right')
        
        # Focar no primeiro campo
        desc_entry.focus_set()

    def _confirmar_exclusao_evento(self, evento):
        """Confirmação visual para exclusão de evento."""
        if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente encerrar o evento '{evento.description}'?\n\nIsso irá:\n• Desativar o evento\n• Remover todas as tarefas futuras associadas"):
            if self.controller:
                try:
                    self.controller.encerrar_evento(evento)
                    self._refresh_eventos()
                    messagebox.showinfo("Evento Encerrado", "Evento encerrado com sucesso!\nTodas as tarefas futuras foram removidas.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao encerrar evento: {str(e)}")
            else:
                self._refresh_eventos()
    
    def _on_agendamento_select(self, event):
        """Callback para seleção de agendamento."""
        pass
    
    def _on_agendamento_double_click(self, event):
        """Callback para duplo clique em agendamento."""
        item_id = self.agendamentos_tree.focus()
        if not item_id:
            return
        col = self.agendamentos_tree.identify_column(event.x)
        col_num = int(col.replace('#', ''))
        if col_num != 6:  # Coluna "Ações"
            return
        index = self.agendamentos_tree.index(item_id)
        agendamento = self.agendamentos[index]
        x_col = self.agendamentos_tree.bbox(item_id, col_num-1)[0]
        click_x = event.x - x_col
        col_width = self.agendamentos_tree.column('Ações', width=None)
        if click_x < col_width // 2:
            self._abrir_modal_edicao_agendamento(agendamento)
        else:
            self._confirmar_exclusao_agendamento(agendamento)

    def _abrir_modal_edicao_agendamento(self, agendamento):
        """Abrir modal para editar agendamento."""
        modal = tk.Toplevel(self)
        modal.title("Editar Agendamento")
        modal.transient(self)
        modal.grab_set()
        tk.Label(modal, text="Descrição:").pack()
        desc_var = tk.StringVar(value=agendamento.description)
        desc_entry = tk.Entry(modal, textvariable=desc_var)
        desc_entry.pack()
        tk.Label(modal, text="Nome:").pack()
        nome_var = tk.StringVar(value=agendamento.nome)
        nome_entry = tk.Entry(modal, textvariable=nome_var)
        nome_entry.pack()
        def salvar():
            # Criar uma cópia do agendamento com os novos dados
            agendamento_editado = copy(agendamento)
            agendamento_editado.description = desc_var.get()
            agendamento_editado.nome = nome_var.get()
            
            if self.controller:
                try:
                    self.controller.update_agendamento(agendamento_editado, agendamento)  # Passar agendamento original
                    # Atualizar o objeto original também
                    agendamento.description = agendamento_editado.description
                    agendamento.nome = agendamento_editado.nome
                    self._refresh_agendamentos()
                    modal.destroy()
                    messagebox.showinfo("Sucesso", "Agendamento editado com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao salvar agendamento: {str(e)}")
            else:
                modal.destroy()
        tk.Button(modal, text="Salvar", command=salvar).pack(pady=10)
        tk.Button(modal, text="Cancelar", command=modal.destroy).pack()

    def _confirmar_exclusao_agendamento(self, agendamento):
        """Confirmação visual para exclusão de agendamento."""
        if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir o agendamento '{agendamento.description}'?"):
            if self.controller:
                self.controller.delete_agendamento(agendamento)
            self._refresh_agendamentos()
            messagebox.showinfo("Excluído", "Agendamento excluído com sucesso!")
    
    def _close_editor(self):
        """Fechar o editor."""
        if self.on_close_callback:
            self.on_close_callback() 