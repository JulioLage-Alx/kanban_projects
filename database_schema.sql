-- Script de criação do banco de dados para o sistema Kanban
-- Execute este script no MySQL Workbench ou via linha de comando

CREATE DATABASE IF NOT EXISTS kanban_projects CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE kanban_projects;

-- Tabela de etapas (colunas do Kanban)
CREATE TABLE IF NOT EXISTS etapas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ordem INT NOT NULL,
    UNIQUE KEY unique_ordem (ordem),
    INDEX idx_ordem (ordem)
);

-- Inserir etapas padrão
INSERT INTO etapas (nome, ordem) VALUES 
    ('Backlog', 1),
    ('Em Andamento', 2),
    ('Em Revisão', 3),
    ('Concluído', 4)
ON DUPLICATE KEY UPDATE nome = VALUES(nome);

-- Tabela de projetos
CREATE TABLE IF NOT EXISTS projetos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    pasta_local VARCHAR(500),
    arquivo_principal VARCHAR(255),
    etapa_atual INT NOT NULL DEFAULT 1,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (etapa_atual) REFERENCES etapas(id),
    INDEX idx_etapa (etapa_atual),
    INDEX idx_nome (nome)
);

-- Tabela de histórico de faturamento
CREATE TABLE IF NOT EXISTS faturamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    projeto_id INT NOT NULL,
    valor DECIMAL(12, 2) NOT NULL,
    descricao VARCHAR(255),
    data_faturamento DATE NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE,
    INDEX idx_projeto_id (projeto_id),
    INDEX idx_data (data_faturamento)
);

-- View para receita total por projeto
CREATE OR REPLACE VIEW view_receita_projetos AS
SELECT 
    p.id,
    p.nome,
    COALESCE(SUM(f.valor), 0) as receita_total
FROM projetos p
LEFT JOIN faturamentos f ON p.id = f.projeto_id
GROUP BY p.id, p.nome;