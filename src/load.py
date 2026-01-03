"""
Módulo de Carga de Dados
"""

import pandas as pd
import logging
from sqlalchemy import create_engine
from config.database import get_database_url

logger = logging.getLogger(__name__)


def load_data(df: pd.DataFrame) -> int:
    """
    Carrega dados transformados no PostgreSQL
    
    Args:
        df: DataFrame com dados transformados
        
    Returns:
        Número de registros carregados
    """
    try:
        # Conectar ao banco de dados
        engine = create_engine(get_database_url())
        
        # Carregar dados
        df.to_sql(
            'sales',
            engine,
            if_exists='append',
            index=False,
            method='multi'
        )
        
        rows_loaded = len(df)
        logger.info(f"{rows_loaded} registros carregados no banco de dados")
        
        return rows_loaded
        
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {str(e)}")
        raise
