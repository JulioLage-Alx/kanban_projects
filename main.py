"""
Gerenciador de Projetos Kanban
Aplicação principal que inicializa o sistema
"""
import os
import sys
from tkinter import messagebox
import customtkinter as ctk
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Adiciona o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import Database, DatabaseError
from gui import KanbanGUI
import mysql.connector


def criar_database_script():
    """Cria o arquivo SQL do banco de dados se não existir"""
    sql_content = """CREATE DATABASE IF NOT EXISTS kanban_projects CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE kanban_projects;

CREATE TABLE IF NOT EXISTS etapas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ordem INT NOT NULL,
    UNIQUE KEY unique_ordem (ordem),
    INDEX idx_ordem (ordem)
);

INSERT INTO etapas (nome, ordem) VALUES 
    ('Backlog', 1),
    ('Em Andamento', 2),
    ('Em Revisão', 3),
    ('Concluído', 4)
ON DUPLICATE KEY UPDATE nome = VALUES(nome);

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

CREATE OR REPLACE VIEW view_receita_projetos AS
SELECT 
    p.id,
    p.nome,
    COALESCE(SUM(f.valor), 0) as receita_total
FROM projetos p
LEFT JOIN faturamentos f ON p.id = f.projeto_id
GROUP BY p.id, p.nome;"""
    
    # Salva o script SQL
    with open("database_setup.sql", "w", encoding="utf-8") as f:
        f.write(sql_content)
    
    return "database_setup.sql"


def setup_database():
    """Configura o banco de dados inicial"""
    # Como você já criou o banco e as tabelas manualmente,
    # vamos apenas verificar se a conexão funciona
    try:
        db_config = get_database_config()
        print("Testando conexão com o banco de dados...")
        
        # Testa a conexão
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Verifica se as tabelas existem
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        expected_tables = ['etapas', 'projetos', 'faturamentos']
        missing_tables = [table for table in expected_tables if table not in tables]
        
        if missing_tables:
            print(f"Aviso: Tabelas faltando: {missing_tables}")
            print("Execute o script SQL manualmente se necessário.")
        else:
            print("✓ Todas as tabelas encontradas!")
        
        cursor.close()
        connection.close()
        print("✓ Conexão estabelecida com sucesso!")
        return True
        
    except mysql.connector.Error as e:
        print(f"Erro ao conectar com banco: {e}")
        return False


def get_database_config():
    """Solicita configurações do banco de dados do usuário"""
    # Por simplicidade, usar configurações padrão
    # Em uma aplicação real, você poderia usar um arquivo de configuração
    # ou solicitar ao usuário via interface gráfica
    
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'kanban_projects')
    }


def main():
    """Função principal da aplicação"""
    print("=== Kanban Projects Manager ===")
    print("Inicializando aplicação...")
    
    # Configura o database se necessário
    if not setup_database():
        print("Erro: Não foi possível configurar o banco de dados.")
        print("Verifique se o MySQL está rodando e as credenciais estão corretas.")
        return
    
    # Obtém configurações do banco
    db_config = get_database_config()
    
    try:
        # Cria conexão com o banco
        print("Conectando ao banco de dados...")
        database = Database(**db_config)
        
        # Cria e inicia a interface gráfica
        print("Iniciando interface gráfica...")
        app = KanbanGUI(database)
        
        print("✓ Aplicação iniciada com sucesso!")
        print("Pressione Ctrl+C para sair")
        
        # Inicia o loop principal
        app.run()
        
    except DatabaseError as e:
        print(f"Erro de banco de dados: {e}")
        messagebox.showerror("Erro de Database", str(e))
    except Exception as e:
        print(f"Erro inesperado: {e}")
        messagebox.showerror("Erro", f"Erro inesperado: {e}")
    finally:
        print("Aplicação encerrada.")


if __name__ == "__main__":
    main()