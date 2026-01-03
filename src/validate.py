"""
Módulo de Validação de Dados com Pydantic
"""

from typing import List, Tuple
from pydantic import BaseModel, validator, EmailStr, constr
from datetime import datetime
import pandas as pd
import logging
import json

logger = logging.getLogger(__name__)


class SalesRecord(BaseModel):
    """
    Schema de validação para registros de vendas
    """
    order_id: constr(min_length=1, max_length=50)
    customer_email: EmailStr
    product_name: constr(min_length=1, max_length=200)
    quantity: int
    unit_price: float
    order_date: str
    
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantidade deve ser maior que zero')
        return v
    
    @validator('unit_price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v
    
    @validator('order_date')
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Data deve estar no formato YYYY-MM-DD')
        return v


def validate_data(df: pd.DataFrame) -> Tuple[List[dict], List[dict]]:
    """
    Valida dados usando schema Pydantic
    
    Args:
        df: DataFrame com dados brutos
        
    Returns:
        Tupla com (dados_válidos, dados_inválidos)
    """
    valid_records = []
    invalid_records = []
    
    for idx, row in df.iterrows():
        try:
            # Tentar validar o registro
            record = SalesRecord(**row.to_dict())
            valid_records.append(record.dict())
        except Exception as e:
            # Registrar erro de validação
            invalid_record = row.to_dict()
            invalid_record['validation_error'] = str(e)
            invalid_record['row_number'] = idx + 1
            invalid_records.append(invalid_record)
            logger.warning(f"Registro {idx + 1} inválido: {str(e)}")
    
    # Salvar registros inválidos para análise
    if invalid_records:
        with open('logs/invalid_records.json', 'w') as f:
            json.dump(invalid_records, f, indent=2, default=str)
    
    return valid_records, invalid_records
