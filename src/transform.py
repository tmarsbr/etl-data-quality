"""
Módulo de Transformação de Dados
"""

from typing import List
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def transform_data(valid_records: List[dict]) -> pd.DataFrame:
    """
    Aplica transformações de negócio nos dados validados
    
    Args:
        valid_records: Lista de registros válidos
        
    Returns:
        DataFrame transformado
    """
    df = pd.DataFrame(valid_records)
    
    # Calcular valor total da venda
    df['total_amount'] = df['quantity'] * df['unit_price']
    
    # Converter data para datetime
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Extrair componentes da data
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month
    df['day'] = df['order_date'].dt.day
    df['day_of_week'] = df['order_date'].dt.day_name()
    
    # Normalizar nomes de produtos
    df['product_name'] = df['product_name'].str.strip().str.title()
    
    # Normalizar emails
    df['customer_email'] = df['customer_email'].str.lower()
    
    # Adicionar timestamp de processamento
    df['processed_at'] = pd.Timestamp.now()
    
    logger.info("Transformações aplicadas com sucesso")
    
    return df
