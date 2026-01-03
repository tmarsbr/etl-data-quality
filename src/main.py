"""
Pipeline ETL com Validação de Qualidade de Dados
Autor: Tiago da Silva E. Santo
"""

import logging
from pathlib import Path
from extract import extract_data
from validate import validate_data
from transform import transform_data
from load import load_data

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def run_pipeline():
    """
    Executa o pipeline ETL completo com validação de qualidade
    """
    try:
        logger.info("=" * 50)
        logger.info("Iniciando Pipeline ETL com Data Quality")
        logger.info("=" * 50)
        
        # Etapa 1: Extração
        logger.info("Etapa 1/4: Extraindo dados...")
        raw_data = extract_data('data/sample_data.csv')
        logger.info(f"✓ {len(raw_data)} registros extraídos")
        
        # Etapa 2: Validação
        logger.info("Etapa 2/4: Validando qualidade dos dados...")
        valid_data, invalid_data = validate_data(raw_data)
        logger.info(f"✓ {len(valid_data)} registros válidos")
        logger.info(f"✗ {len(invalid_data)} registros rejeitados")
        
        if invalid_data:
            logger.warning(f"Registros inválidos salvos em: logs/invalid_records.json")
        
        # Etapa 3: Transformação
        logger.info("Etapa 3/4: Transformando dados...")
        transformed_data = transform_data(valid_data)
        logger.info(f"✓ {len(transformed_data)} registros transformados")
        
        # Etapa 4: Carga
        logger.info("Etapa 4/4: Carregando dados no banco...")
        rows_loaded = load_data(transformed_data)
        logger.info(f"✓ {rows_loaded} registros carregados no PostgreSQL")
        
        # Relatório final
        logger.info("=" * 50)
        logger.info("Pipeline ETL concluído com sucesso!")
        logger.info(f"Taxa de sucesso: {(len(valid_data)/len(raw_data)*100):.2f}%")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"Erro no pipeline: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    # Criar diretório de logs se não existir
    Path('logs').mkdir(exist_ok=True)
    
    # Executar pipeline
    run_pipeline()
