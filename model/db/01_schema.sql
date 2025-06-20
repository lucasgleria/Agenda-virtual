-- model/db/01_schema.sql
-- Script de criação do schema do banco de dados para Agenda Virtual

-- Usuários (opcional, para multiusuário)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    senha_hash VARCHAR(255)
);

-- Eventos recorrentes
CREATE TABLE IF NOT EXISTS eventos (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    nome VARCHAR(100),
    dias_semana VARCHAR(3)[] NOT NULL, -- Ex: ['seg', 'qua']
    ativo BOOLEAN DEFAULT TRUE,
    data_encerramento DATE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Tarefas
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    priority VARCHAR(20), -- Enum: muito-importante, importante, média, simples
    nome VARCHAR(100),
    is_agendamento BOOLEAN DEFAULT FALSE,
    is_evento BOOLEAN DEFAULT FALSE,
    dias_evento VARCHAR(3)[],
    date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'pendente', -- Enum: pendente, concluída, cancelada
    evento_id INTEGER REFERENCES eventos(id) ON DELETE SET NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Estado da interface
CREATE TABLE IF NOT EXISTS interface_state (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    completed_tasks JSONB,
    filtros_ativos JSONB,
    outras_configs JSONB
);

-- Backups
CREATE TABLE IF NOT EXISTS backups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    data_backup TIMESTAMP DEFAULT NOW(),
    arquivo BYTEA
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_tasks_date ON tasks(date);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_is_agendamento ON tasks(is_agendamento);
CREATE INDEX IF NOT EXISTS idx_tasks_is_evento ON tasks(is_evento);
CREATE INDEX IF NOT EXISTS idx_eventos_dias_semana ON eventos USING GIN(dias_semana); 