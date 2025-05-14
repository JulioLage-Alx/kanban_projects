"""
Arquivo de configuração do sistema Kanban.
Configuração baseada na conexão Local_db do MySQL Workbench.
"""

import os
from pathlib import Path

# Configurações do banco de dados
class DatabaseConfig:
    # Configurações baseadas na conexão Local_db (localhost:3306)
    HOST = 'localhost'  # ou '127.0.0.1'
    PORT = 3306
    DATABASE = 'kanban_projects'
    USER = 'root'
    PASSWORD = 'Julio1975'  # Deixe vazio se não tiver senha, ou coloque sua senha
    CHARSET = 'utf8mb4'
    
    # Timeout de conexão (em segundos)
    CONNECTION_TIMEOUT = 10
    
    # Pool de conexões
    POOL_NAME = 'kanban_pool'
    POOL_SIZE = 5
    POOL_RESET_SESSION = True

# Configurações da aplicação
class AppConfig:
    # Nome da aplicação
    APP_NAME = "Sistema Kanban"
    APP_VERSION = "1.0.0"
    
    # Diretórios
    BASE_DIR = Path(__file__).parent
    LOG_DIR = BASE_DIR / "logs"
    BACKUP_DIR = BASE_DIR / "backups"
    
    # Auto-refresh da interface (em milissegundos)
    REFRESH_INTERVAL = 30000  # 30 segundos
    
    # Configurações de log
    LOG_LEVEL = "INFO"
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5

# Configurações de interface
class UIConfig:
    # Dimensões da janela principal
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 800
    
    # Dimensões dos cartões
    CARD_WIDTH = 280
    CARD_MAX_HEIGHT = 200
    
    # Cores (em hex)
    PRIMARY_COLOR = "#4CAF50"
    SECONDARY_COLOR = "#2196F3"
    WARNING_COLOR = "#FF9800"
    ERROR_COLOR = "#F44336"
    SUCCESS_COLOR = "#27AE60"
    
    # Estilos CSS
    CARD_STYLE = """
        QFrame {
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            background-color: white;
            margin: 5px;
        }
        QFrame:hover {
            border-color: #4CAF50;
            background-color: #f0f8ff;
        }
    """
    
    BUTTON_PRIMARY_STYLE = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
    """