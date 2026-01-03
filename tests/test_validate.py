"""
Testes para módulo de validação
"""

import pytest
import pandas as pd
from src.validate import validate_data, SalesRecord


def test_valid_sales_record():
    """Testa validação de registro válido"""
    valid_record = {
        'order_id': 'ORD-12345',
        'customer_email': 'cliente@email.com',
        'product_name': 'Notebook Dell',
        'quantity': 2,
        'unit_price': 2500.00,
        'order_date': '2024-01-15'
    }
    
    record = SalesRecord(**valid_record)
    assert record.order_id == 'ORD-12345'
    assert record.quantity == 2


def test_invalid_quantity():
    """Testa rejeição de quantidade inválida"""
    invalid_record = {
        'order_id': 'ORD-12345',
        'customer_email': 'cliente@email.com',
        'product_name': 'Notebook Dell',
        'quantity': -1,  # Quantidade negativa
        'unit_price': 2500.00,
        'order_date': '2024-01-15'
    }
    
    with pytest.raises(ValueError):
        SalesRecord(**invalid_record)


def test_invalid_email():
    """Testa rejeição de email inválido"""
    invalid_record = {
        'order_id': 'ORD-12345',
        'customer_email': 'email_invalido',  # Email sem @
        'product_name': 'Notebook Dell',
        'quantity': 2,
        'unit_price': 2500.00,
        'order_date': '2024-01-15'
    }
    
    with pytest.raises(ValueError):
        SalesRecord(**invalid_record)


def test_validate_data_function():
    """Testa função de validação completa"""
    df = pd.DataFrame([
        {
            'order_id': 'ORD-001',
            'customer_email': 'valid@email.com',
            'product_name': 'Produto A',
            'quantity': 1,
            'unit_price': 100.0,
            'order_date': '2024-01-01'
        },
        {
            'order_id': 'ORD-002',
            'customer_email': 'invalid_email',  # Email inválido
            'product_name': 'Produto B',
            'quantity': 2,
            'unit_price': 200.0,
            'order_date': '2024-01-02'
        }
    ])
    
    valid, invalid = validate_data(df)
    
    assert len(valid) == 1
    assert len(invalid) == 1
    assert valid[0]['order_id'] == 'ORD-001'
