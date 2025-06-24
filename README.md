# 📅 Agenda Virtual - Sistema de Gerenciamento de Tarefas

Um sistema completo de gerenciamento de tarefas e eventos com interface moderna e intuitiva, desenvolvido em Python com Tkinter.

## ✨ Novas Funcionalidades de UX/UI

### 🎨 Interface Modernizada
- **Design de Cards**: Visualização moderna das tarefas em formato de cards visuais
- **Sistema de Abas**: Organização clara com abas para Tarefas e Dashboard
- **Layout Responsivo**: Interface que se adapta a diferentes tamanhos de janela

### 🔍 Melhorias na Usabilidade
- **Filtros Avançados**: Busca por nome, status, tipo e prioridade
- **Visualização Dupla**: Alternância entre visualização em cards e lista
- **Animações Suaves**: Transições e animações para melhor experiência
- **Ícones Intuitivos**: Uso de emojis e ícones para melhor identificação visual

### 📱 Componentes Otimizados
- **CalendarPanel**: Layout horizontal compacto com calendário e formulário lado a lado
- **TaskListPanel**: Cards visuais com informações detalhadas e ações rápidas
- **FilterPanel**: Interface moderna com campos de busca e filtros
- **EditorPanel**: Modo de edição com cards organizados

## 🚀 Funcionalidades Principais

### 📋 Gerenciamento de Tarefas
- Criar, editar e excluir tarefas
- Definir prioridades (Muito Importante, Importante, Média, Simples)
- Marcar tarefas como concluídas
- Agendar tarefas para datas específicas

### 📅 Sistema de Eventos
- Criar eventos recorrentes
- Definir dias da semana para eventos
- Gerenciar eventos ativos

### 🔔 Sistema de Alertas
- Alertas para agendamentos próximos
- Filtros por urgência e tipo
- Notificações automáticas

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Tkinter**: Interface gráfica
- **SQLite**: Banco de dados
- **tkcalendar**: Widget de calendário
- **threading**: Processamento assíncrono

## 📁 Estrutura do Projeto

```
Agenda-virtual/
├── main.py                 # Ponto de entrada da aplicação
├── controller/             # Controladores da aplicação
├── model/                  # Modelos de dados
│   ├── agenda.py          # Modelo principal da agenda
│   ├── task.py            # Modelo de tarefa
│   ├── evento.py          # Modelo de evento
│   └── db/                # Camada de banco de dados
├── view/                   # Interface do usuário
│   ├── gui.py             # Interface principal
│   └── components/        # Componentes da interface
├── services/              # Serviços da aplicação
│   └── notification_service.py # Sistema de notificações
└── docs/                  # Documentação
```

## 🚀 Como Executar

1. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar a aplicação**:
   ```bash
   python main.py
   ```

## 🎯 Melhorias Implementadas

### Interface Central
- **Sistema de Abas**: Organização clara entre Tarefas e Dashboard
- **Layout Horizontal**: Melhor aproveitamento do espaço da tela
- **Responsividade**: Interface que se adapta ao tamanho da janela

### TaskListPanel
- **Visualização em Cards**: Cards visuais com informações detalhadas
- **Alternância de Visualização**: Cards ↔ Lista tradicional
- **Ações Rápidas**: Botões para completar, editar e excluir
- **Estatísticas Visuais**: Contadores com ícones

### CalendarPanel
- **Layout Compacto**: Calendário e formulário lado a lado
- **Campos Inteligentes**: Placeholders e validação
- **Botões Modernos**: Ícones e estilos consistentes

### FilterPanel
- **Filtros Avançados**: Busca, status, tipo e prioridade
- **Interface Limpa**: Layout em grid organizado
- **Feedback Visual**: Contador de resultados

### EditorPanel
- **Cards de Edição**: Interface visual para edição
- **Ações Contextuais**: Botões específicos para cada ação
- **Animações**: Transições suaves

## 📊 Funcionalidades Avançadas

### Dashboard
- Visão geral das tarefas
- Estatísticas e gráficos
- Resumo de atividades

### Backup e Exportação
- Backup automático dos dados
- Exportação para JSON
- Restauração de dados

### Notificações
- Sistema de notificações automáticas
- Alertas para tarefas próximas
- Configuração de intervalos

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆕 Changelog

### v2.0.0 - Interface Modernizada
- ✨ Nova interface com cards visuais
- 📱 Layout responsivo
- 🔍 Filtros avançados
- 📊 Dashboard integrado
- 🎯 Melhorias de UX/UI

### v1.0.0 - Versão Inicial
- 📋 Gerenciamento básico de tarefas
- 📅 Sistema de eventos
- 🔔 Alertas simples
- 💾 Persistência de dados

---

**Desenvolvido com ❤️ para melhorar sua produtividade!**