-- Migração: criar schema tutor e tabela documento_vetor com pgvector
-- Executar no database 'bayarea' do RDS (bigdata.dataiesb.com)

-- 1. Criar a extensão vector (se ainda não existir)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Criar o schema tutor
CREATE SCHEMA IF NOT EXISTS tutor;

-- 3. Criar a tabela de documentos vetorizados
CREATE TABLE IF NOT EXISTS tutor.documento_vetor (
    id VARCHAR(36) PRIMARY KEY,
    arquivo_id VARCHAR(36) NOT NULL,
    titulo VARCHAR(512),
    professor_id VARCHAR(36),
    vinculos TEXT,
    tipo VARCHAR(50),
    data_upload TIMESTAMP,
    conteudo TEXT NOT NULL,
    embedding vector(384) NOT NULL
);

-- 4. Índices
CREATE INDEX IF NOT EXISTS ix_documento_vetor_arquivo_id
    ON tutor.documento_vetor (arquivo_id);

-- Índice IVFFlat para busca vetorial eficiente (cosseno)
-- Nota: precisa de pelo menos ~100 linhas na tabela para o IVFFlat funcionar bem.
-- Para tabelas pequenas, remova este índice e use busca brute-force (que é o fallback).
-- CREATE INDEX ix_documento_vetor_embedding
--     ON tutor.documento_vetor
--     USING ivfflat (embedding vector_cosine_ops)
--     WITH (lists = 100);
