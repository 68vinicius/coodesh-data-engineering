import sqlite3
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def transformar_dados(vendas): # Converte em DataFrame
    df = pd.DataFrame(vendas, columns=[
        'id', 'data_venda', 'id_produto', 'id_cliente', 
        'quantidade', 'valor_unitario', 'valor_total', 
        'id_vendedor', 'regiao'
    ])

    # Converte as datas para o formato ISO
    df['data_venda'] = pd.to_datetime(df['data_venda']).dt.strftime('%Y-%m-%d')

    # Verifica dados duplicados *IGNORA O ID*
    contagem_duplicados = df.duplicated(subset=[
        'data_venda', 'id_produto', 'id_cliente', 
        'quantidade', 'valor_unitario', 'valor_total', 
        'id_vendedor', 'regiao'
    ]).sum()

    # Remove dados duplicados
    df.drop_duplicates(subset=[
        'data_venda', 'id_produto', 'id_cliente', 
        'quantidade', 'valor_unitario', 'valor_total', 
        'id_vendedor', 'regiao'
    ], inplace=True)

    # Cálculo do total de vendas por dia
    df['total_vendas'] = df['valor_total'] * df['quantidade']
    vendas_por_dia = df.groupby('data_venda')['total_vendas'].sum().reset_index()
    logging.info(f'Total de vendas por dia:')
    logging.info(vendas_por_dia)

    return df, contagem_duplicados # Df transformado 

if __name__ == "__main__": # Conexão com o banco de dados
    conn = sqlite3.connect('data/vendas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vendas')
    vendas = cursor.fetchall()
    
    df, duplicates_count = transformar_dados(vendas)

    logging.info('DataFrame transformado:')
    print(df)

    logging.info(f'Processo de transformação concluído com {duplicates_count} duplicatas encontradas.')
    conn.close()