# 📅 Agenda Virtual - Sistema de Gerenciamento de Tarefas

## 📋 Visão Geral

O **Agenda Virtual** é um sistema completo de gerenciamento de tarefas, eventos e agendamentos desenvolvido em Python com interface gráfica Tkinter. O sistema oferece uma solução robusta para organização pessoal e profissional, com recursos avançados de notificação, dashboard estatístico e gerenciamento de prioridades.

## ✨ Funcionalidades Principais

### 🎯 Gerenciamento de Tarefas
- **Criação de Tarefas**: Adicione tarefas com descrição, prioridade e nome
- **Sistema de Prioridades**: 4 níveis (Muito Importante, Importante, Média, Simples)
- **Status de Conclusão**: Marque tarefas como concluídas ou pendentes
- **Edição e Exclusão**: Modifique ou remova tarefas facilmente

### 📅 Sistema de Eventos
- **Eventos Recorrentes**: Crie eventos que se repetem em dias específicos da semana
- **Geração Automática**: Tarefas são criadas automaticamente para os próximos 90 dias
- **Gerenciamento de Eventos**: Ative/desative eventos conforme necessário

### 📋 Agendamentos
- **Agendamentos Específicos**: Crie compromissos para datas específicas
- **Notificações Inteligentes**: Receba lembretes automáticos
- **Filtros Avançados**: Organize por tipo, urgência e período

### 📊 Dashboard Estatístico
- **Estatísticas em Tempo Real**: Visualize progresso e produtividade
- **Gráficos Interativos**: Gráfico de pizza (status) e barras (prioridades)
- **Métricas de Produtividade**: Taxa de conclusão e distribuição de tarefas

### 🔔 Sistema de Notificações
- **Notificações do Sistema**: Lembretes automáticos para agendamentos
- **Feedback Visual**: Notificações de sucesso, erro e aviso na interface
- **Configuração Flexível**: Ative/desative notificações conforme preferência

### 💾 Backup e Exportação
- **Backup Interno**: Crie backups automáticos dos dados
- **Exportação de Dados**: Exporte dados em formato JSON
- **Recuperação de Dados**: Restaure dados de backups anteriores

## 🏗️ Arquitetura do Sistema

### Estrutura de Diretórios
```
Agenda-virtual/
├── main.py                 # Ponto de entrada da aplicação
├── controller/
│   └── controller.py       # Lógica de negócio e controle
├── model/
│   ├── task.py            # Modelo de dados para tarefas
│   ├── evento.py          # Modelo de dados para eventos
│   ├── priority_flag.py   # Enumeração de prioridades
│   └── db/
│       ├── database.py    # Configuração do banco de dados
│       ├── repository.py  # Acesso aos dados
│       └── config.py      # Configurações do banco
├── view/
│   ├── gui.py             # Interface principal
│   ├── components/        # Componentes da interface
│   └── theme/             # Sistema de temas e cores
├── services/
│   └── notification_service.py  # Serviço de notificações
└── docs/                  # Documentação do projeto
```

### Padrão MVC (Model-View-Controller)

#### **Model (Modelo)**
- **Task**: Representa uma tarefa com propriedades como descrição, prioridade, status
- **Evento**: Representa um evento recorrente com dias da semana
- **Repository**: Gerencia acesso e persistência dos dados

#### **View (Visualização)**
- **AgendaView**: Interface principal com sistema de abas
- **Componentes**: Painéis especializados (calendário, tarefas, eventos, alertas)
- **Tema**: Sistema de cores e estilos unificados

#### **Controller (Controle)**
- **AgendaController**: Coordena interações entre modelo e visualização
- **Lógica de Negócio**: Validações, regras de negócio e operações complexas

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.7 ou superior
- SQLite3 (incluído no Python)
- tkinter (incluído no Python)

### Dependências
```bash
pip install -r requirements.txt
```

### Dependências Principais
- `tkcalendar`: Calendário interativo
- `plyer`: Notificações do sistema operacional

### Execução
```bash
python main.py
```

## 📖 Manual do Usuário

### 🎯 Primeiros Passos

#### 1. Criando sua Primeira Tarefa
1. **Selecione uma data** no calendário
2. **Digite a descrição** da tarefa no campo "Descrição"
3. **Escolha a prioridade** (Muito Importante, Importante, Média, Simples)
4. **Adicione um nome** (opcional) para identificação
5. **Clique em "Adicionar"**

#### 2. Criando um Evento Recorrente
1. **Marque a caixa "É um evento"**
2. **Selecione os dias da semana** em que o evento deve ocorrer
3. **Digite a descrição** do evento
4. **Adicione um nome** (opcional)
5. **Clique em "Adicionar"**

#### 3. Criando um Agendamento
1. **Marque a caixa "É um agendamento"**
2. **Digite a descrição** do agendamento
3. **Escolha a prioridade** se necessário
4. **Adicione um nome** (opcional)
5. **Clique em "Adicionar"**

### 📊 Usando o Dashboard

#### Acessando o Dashboard
- Clique no botão **"📊 Dashboard"** na barra de ferramentas
- Ou use a aba **"📊 Dashboard"** no painel central

#### Interpretando as Estatísticas
- **Total de Tarefas**: Número total de tarefas nos últimos 30 dias
- **Concluídas**: Tarefas marcadas como concluídas
- **Pendentes**: Tarefas ainda não concluídas
- **Taxa de Conclusão**: Percentual de tarefas concluídas

#### Gráficos Disponíveis
- **Gráfico de Pizza**: Distribuição por status (Concluída, Pendente)
- **Gráfico de Barras**: Distribuição por prioridade (Alta, Média, Baixa)

### 🔔 Configurando Notificações

#### Ativar/Desativar Notificações
1. Clique em **"⚙️ Configurações"** na barra de ferramentas
2. Marque/desmarque **"Ativar notificações do sistema"**
3. Clique em **"💾 Salvar"**

#### Tipos de Notificação
- **Lembretes de Agendamento**: Notificações automáticas para agendamentos próximos
- **Feedback de Ações**: Confirmações de sucesso, erro ou aviso na interface

### 💾 Backup e Exportação

#### Criando um Backup
1. Clique em **"💾 Backup"** na barra de ferramentas
2. Confirme a criação do backup
3. Aguarde a confirmação de sucesso

#### Exportando Dados
1. Clique em **"📤 Exportar"** na barra de ferramentas
2. Escolha o local e nome do arquivo
3. Os dados serão salvos em formato JSON

### 🎨 Personalizando a Interface

#### Alterando o Tema
1. Clique em **"⚙️ Configurações"**
2. Selecione o tema desejado (Claro/Escuro)
3. Clique em **"💾 Salvar"**

#### Filtros e Busca
- **Painel de Tarefas**: Filtre por status, tipo e nome
- **Painel de Eventos**: Filtre por período, status e nome
- **Painel de Alertas**: Filtre por tipo, urgência e nome

## 🔧 Documentação Técnica

### Modelos de Dados

#### Task (Tarefa)
```python
class Task:
    def __init__(self, description, priority=None, nome=None, 
                 is_agendamento=False, is_evento=False, 
                 dias_evento=None, status="pendente"):
        self.description = description
        self.priority = priority
        self.nome = nome
        self.is_agendamento = is_agendamento
        self.is_evento = is_evento
        self.dias_evento = dias_evento
        self.status = status
```

#### Evento
```python
class Evento:
    def __init__(self, description, nome, dias_semana):
        self.description = description
        self.nome = nome
        self.dias_semana = dias_semana
        self.ativo = True
```

### Banco de Dados

#### Estrutura das Tabelas
```sql
-- Tabela de tarefas
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    priority TEXT,
    nome TEXT,
    is_agendamento BOOLEAN DEFAULT FALSE,
    is_evento BOOLEAN DEFAULT FALSE,
    dias_evento TEXT,
    date DATE,
    status TEXT DEFAULT 'pendente',
    evento_id INTEGER
);

-- Tabela de eventos
CREATE TABLE eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    nome TEXT,
    dias_semana TEXT NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);
```

### API do Controller

#### Métodos Principais
```python
class AgendaController:
    def add_task(self, date, description, priority, nome=None, 
                 is_agendamento=False, is_evento=False, dias_evento=None)
    
    def add_evento(self, description, nome, dias_semana)
    
    def get_tasks_for_date(self, date)
    
    def update_task_status(self, task_key, done)
    
    def edit_task(self, date, task)
    
    def delete_task(self, date, task)
    
    def handle_export_data(self)
    
    def handle_create_backup(self)
```

### Sistema de Notificações

#### NotificationScheduler
```python
class NotificationScheduler:
    def __init__(self, repository, check_interval=3600)
    def start(self)
    def stop(self)
    def _check_schedules(self)
```

#### Tipos de Notificação
- **Sistema**: Notificações do sistema operacional
- **Interface**: Feedback visual na aplicação
- **Lembretes**: Alertas automáticos para agendamentos

## 🎨 Sistema de Temas

### Paleta de Cores
```python
class ColorPalette:
    PRIMARY = {
        'main': '#2563eb',    # Azul principal
        'light': '#3b82f6',   # Azul claro
        'dark': '#1d4ed8'     # Azul escuro
    }
    
    SUCCESS = {'main': '#059669'}  # Verde
    WARNING = {'main': '#d97706'}  # Laranja
    ERROR = {'main': '#dc2626'}    # Vermelho
    
    NEUTRAL = {
        'gray_50': '#f9fafb',
        'gray_600': '#4b5563',
        'gray_700': '#374151'
    }
```

### Aplicação de Estilos
```python
class StyleManager:
    @staticmethod
    def setup_styles()
    
    @staticmethod
    def get_button_style(style_type)
```

## 🐛 Solução de Problemas

### Problemas Comuns

#### 1. Aplicação não inicia
**Sintoma**: Erro ao executar `python main.py`
**Solução**: 
- Verifique se todas as dependências estão instaladas
- Execute `pip install -r requirements.txt`

#### 2. Notificações não funcionam
**Sintoma**: Não recebe lembretes de agendamentos
**Solução**:
- Verifique se as notificações estão ativadas nas configurações
- Confirme se o sistema operacional permite notificações

#### 3. Dashboard não carrega dados
**Sintoma**: Dashboard mostra "Sem dados"
**Solução**:
- Verifique se há tarefas criadas
- Clique em "🔄 Atualizar" no dashboard

#### 4. Erro de banco de dados
**Sintoma**: Erro ao salvar ou carregar dados
**Solução**:
- Verifique se o arquivo do banco não está corrompido
- Restaure de um backup anterior

### Logs de Debug
O sistema gera logs detalhados para facilitar o debug:
```
[GUI] Atualizando view para data: 2025-06-24
[GUI] Tarefas encontradas: 9
[GUI] Painel de tarefas atualizado
[GUI] Atualização da view concluída com sucesso
```

## 🔄 Atualizações e Manutenção

### Versão Atual
- **Versão**: 1.0
- **Data**: Dezembro 2024
- **Compatibilidade**: Python 3.7+

### Histórico de Versões
- **v1.0**: Versão inicial com funcionalidades básicas
- Implementação completa do sistema MVC
- Dashboard estatístico funcional
- Sistema de notificações
- Backup e exportação de dados

### Próximas Versões
- **v1.1**: Tema escuro e personalização avançada
- **v1.2**: Sincronização na nuvem
- **v1.3**: Relatórios avançados e métricas
- **v2.0**: Interface web e aplicativo móvel

## 🤝 Contribuição

### Como Contribuir
1. **Fork** o repositório
2. **Crie** uma branch para sua feature
3. **Implemente** suas mudanças
4. **Teste** todas as funcionalidades
5. **Envie** um Pull Request

### Padrões de Código
- **PEP 8**: Seguir padrões de estilo Python
- **Docstrings**: Documentar todas as funções
- **Type Hints**: Usar tipagem quando possível
- **Testes**: Incluir testes para novas funcionalidades

### Estrutura de Commits
```
feat: adiciona nova funcionalidade
fix: corrige bug
docs: atualiza documentação
style: formatação de código
refactor: refatoração sem mudança funcional
test: adiciona ou corrige testes
```

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

### Contato
- **Email**: suporte@agendavirtual.com
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/agenda-virtual/issues)
- **Documentação**: [Wiki do Projeto](https://github.com/seu-usuario/agenda-virtual/wiki)

### Recursos Adicionais
- **FAQ**: Perguntas frequentes
- **Tutoriais**: Guias passo a passo
- **Vídeos**: Demonstrações em vídeo
- **Comunidade**: Fórum de discussão

---

**Desenvolvido com ❤️ para facilitar sua organização pessoal e profissional.**