import os
import pandas as pd
import logging
from transform import transformar_dados
from extract import extrair_dados_vendas 

logging.basicConfig(level=logging.INFO)

# Script para carregar os dados simulando o carregamento para S3 em CSV
def carregar_para_s3(df):
    from datetime import datetime

    # Diretório local
    bucket_s3_path = 'bucket_S3/'
    os.makedirs(bucket_s3_path, exist_ok=True)
    
    # Partições por ano/mês/dia
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    df['ano'] = df['data_venda'].dt.year
    df['mes'] = df['data_venda'].dt.month
    df['dia'] = df['data_venda'].dt.day

    # Agrupar os dados por ano, mês e dia para otimizar o processo de gravação
    grouped = df.groupby(['ano', 'mes', 'dia'])

    # Caminho para a pasta
    for (ano, mes, dia), grupo in grouped:
        path = os.path.join(bucket_s3_path, f'{ano}/{mes:02d}/{dia:02d}')
        os.makedirs(path, exist_ok=True)

        # Salva os arquivos em CSV
        for _, row in grupo.iterrows():
            file_name = f'vendas_{row["id"]}_{row["data_venda"].strftime("%Y%m%d")}.csv'
            row_data = grupo[grupo['id'] == row['id']].drop(columns=['ano', 'mes', 'dia'])
            row_data.to_csv(os.path.join(path, file_name), index=False)

    logging.info(f'Carregado com sucesso para o bucket S3.')

if __name__ == "__main__":
    vendas = extrair_dados_vendas() 
    df, contagem_duplicados = transformar_dados(vendas)

    logging.info(f'Número de duplicatas encontradas: {contagem_duplicados}')
    logging.info(f'DataFrame transformado:')
    print(df)

    carregar_para_s3(df)