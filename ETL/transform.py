import sqlite3
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

# Script para transformar os dados extraidos do SQLite em DataFrame
def transformar_dados(vendas):
    df = pd.DataFrame(vendas, columns=[
        'id', 'data_venda', 'id_produto', 'id_cliente',
        'quantidade', 'valor_unitario', 'valor_total',
        'id_vendedor', 'regiao'
    ])

    # Converte as datas para o formato ISO
    df['data_venda'] = pd.to_datetime(df['data_venda']).dt.strftime('%Y-%m-%d')

    # Verifica e remove dados duplicados *IGNORA O ID*
    contagem_duplicados = df.duplicated(subset=[
        'data_venda', 'id_produto', 'id_cliente', 'quantidade', 
        'valor_unitario', 'valor_total', 'id_vendedor', 'regiao'
    ]).sum()

    df.drop_duplicates(subset=[
        'data_venda', 'id_produto', 'id_cliente', 'quantidade',
        'valor_unitario', 'valor_total', 'id_vendedor', 'regiao'
    ], inplace=True)

    # Cálculo do total de vendas por dia
    df['total_vendas'] = df['valor_total'] * df['quantidade']
    vendas_por_dia = df.groupby('data_venda')['total_vendas'].sum().reset_index()

    logging.info(f'Total de vendas por dia:')
    logging.info(vendas_por_dia)

    return df, contagem_duplicados

def obter_dados_do_banco():
    conexao = sqlite3.connect('data/vendas.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM vendas')
    vendas = cursor.fetchall()
    conexao.close()
    return vendas

if __name__ == "__main__": # Conexão com o banco de dados
    vendas = obter_dados_do_banco()
    df, contagem_duplicados = transformar_dados(vendas)

    logging.info(f'Número de duplicatas encontradas: {contagem_duplicados}')
    logging.info(f'DataFrame transformado:')
    print(df)