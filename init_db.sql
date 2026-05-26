-- Script para inicializar o banco de dados do Cache Semântico no PostgreSQL
-- Execute este script no DBeaver conectado ao seu banco PostgreSQL.

-- Habilita a extensão de vetores (pgvector)
CREATE EXTENSION IF NOT EXISTS vector;

-- Cria a tabela de cache de ataques
CREATE TABLE IF NOT EXISTS cache_ataques (
    id SERIAL PRIMARY KEY,
    categoria VARCHAR(50) NOT NULL,
    prompt_texto TEXT NOT NULL,
    embedding vector(768), -- Assumindo que usaremos o Google Embeddings que tem 768 dimensões
    origem VARCHAR(50) DEFAULT 'manual',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cria um índice HNSW para busca semântica super rápida (Opcional, mas recomendado para produção)
CREATE INDEX ON cache_ataques USING hnsw (embedding vector_cosine_ops);
