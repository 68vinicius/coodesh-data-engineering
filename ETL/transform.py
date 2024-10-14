import sqlite3
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def transformar_dados(vendas):
    df = pd.DataFrame(vendas, columns=[
        'id', 'data_venda', 'id_produto', 'id_cliente', 
        'quantidade', 'valor_unitario', 'valor_total', 
        'id_vendedor', 'regiao'
    ])

    # Converte as datas para o formato ISO
    df['data_venda'] = pd.to_datetime(df['data_venda']).dt.strftime('%Y-%m-%d')

    # Verifica dados duplicados
    contagem_duplicados = df.duplicated(subset=[
        'id', 'data_venda', 'id_produto', 'id_cliente', 
        'quantidade', 'valor_unitario', 'valor_total', 
        'id_vendedor', 'regiao'
    ]).sum()

    # Total de vendas por dia
    df['total_vendas'] = df['valor_total'] * df['quantidade']
    vendas_por_dia = df.groupby('data_venda')['total_vendas'].sum().reset_index()

    # Identifica e remove quaisquer dados duplicados
    duplicados = df[df.duplicated(subset=['data_venda', 'id_produto', 'id_cliente'], keep=False)]
    if not duplicados.empty:
        logging.info(f'Duplicatas encontradas: {duplicados}')
    df.drop_duplicates(subset=['data_venda', 'id_produto', 'id_cliente'], inplace=True)  # Remove duplicatas

    return df, vendas_por_dia, contagem_duplicados

if __name__ == "__main__":
    conn = sqlite3.connect('data/vendas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vendas')
    vendas = cursor.fetchall()
    
    df, vendas_por_dia, duplicates_count = transformar_dados(vendas)
    print(vendas_por_dia)

    logging.info(f'Processo de transformação concluído com {duplicates_count} duplicatas encontradas.')

    conn.close()