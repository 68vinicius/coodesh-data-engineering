import sqlite3
import pandas as pd
import logging
from extract import extrair_dados_vendas 

logging.basicConfig(level=logging.INFO)

# Script para transformar os dados extraídos do SQLite em DataFrame
def transformar_dados(vendas):
    df = pd.DataFrame(vendas, columns=[
        'id', 'data_venda', 'id_produto', 'id_cliente',
        'quantidade', 'valor_unitario', 'valor_total',
        'id_vendedor', 'regiao'
    ])

    # Converte as datas para o formato ISO
    df['data_venda'] = pd.to_datetime(df['data_venda']).dt.strftime('%Y-%m-%d')

    # Verifica dados duplicados *IGNORA O ID*
    # (ID deve ser considerado pois é um identificador único gerado pelo script para cada registro)
    contagem_duplicados = df.duplicated(subset=[
        'data_venda', 'id_produto', 'id_cliente', 'quantidade', 
        'valor_unitario', 'valor_total', 'id_vendedor', 'regiao'
    ]).sum()

    df.drop_duplicates(subset=[ # Remove dados duplicados *IGNORA O ID*
        'data_venda', 'id_produto', 'id_cliente', 'quantidade',
        'valor_unitario', 'valor_total', 'id_vendedor', 'regiao'
    ], inplace=True)

    # Cálculo do total de vendas por dia
    vendas_por_dia = df.groupby('data_venda')['valor_total'].sum().reset_index(name='total_vendas')

    logging.info(f'Total de vendas por dia:')
    logging.info(vendas_por_dia)

    return df, contagem_duplicados

if __name__ == "__main__":
    try:
        vendas = extrair_dados_vendas() # Função para extrair dados de vendas do SQLite
        if not vendas: 
            logging.warning('Nenhum dado de vendas foi extraído.')
        else: # Transforma os dados extraidos em um DataFrame
            df, contagem_duplicados = transformar_dados(vendas)

            logging.info(f'Número de duplicatas encontradas: {contagem_duplicados}')
            logging.info('DataFrame transformado:')

            print(df)
    except Exception:
        logging.error(f'Ocorreu um erro ao extrair os dados: {Exception}')