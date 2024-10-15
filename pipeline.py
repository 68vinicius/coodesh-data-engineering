import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'ETL'))

from extract import extrair_dados_vendas
from transform import transformar_dados
from loading import carregar_para_s3

logging.basicConfig(level=logging.INFO)

# Script para executar o pipeline
def executar_pipeline():
    logging.info('Iniciando o pipeline de ETL..')
    
    # 1. Extração de Dados
    logging.info('Iniciando a extração dos dados.')
    vendas = extrair_dados_vendas()
    if not vendas:
        logging.error('Nenhum dado foi extraído.')
        return
    
    # 2. Transformação
    logging.info('Iniciando a transformação dos dados.')
    df, contagem_duplicados = transformar_dados(vendas)
    logging.info(f'Número de duplicatas removidas: {contagem_duplicados}')
    
    # 3. Carregamento
    logging.info('Iniciando o carregamento dos dados.')
    carregar_para_s3(df)
    
    logging.info('Pipeline executado com sucesso.')

if __name__ == "__main__":
    executar_pipeline()
