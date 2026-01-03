"""
Configuração de Banco de Dados
"""

import os
from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    """
    Retorna URL de conexão do banco de dados
    """
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'sales_db')
    
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
