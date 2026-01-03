"""
Módulo de Extração de Dados
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)


def extract_data(file_path: str) -> pd.DataFrame:
    """
    Extrai dados de arquivo CSV
    
    Args:
        file_path: Caminho do arquivo CSV
        
    Returns:
        DataFrame com os dados extraídos
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Dados extraídos de {file_path}")
        return df
    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Erro ao extrair dados: {str(e)}")
        raise
