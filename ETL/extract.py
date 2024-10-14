import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

# Script para conectar-se ao banco de dados SQLite e extrair registros da tabela vendas
def extrair_dados_vendas(caminho_banco='data/vendas.db'):
    conn = None
    vendas = []
    try: # Conecta ao banco e realiza a consulta
        conn = sqlite3.connect(caminho_banco)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vendas')
        vendas = cursor.fetchall()
        logging.info(f'{len(vendas)} Dados extraídos com sucesso.')
    except Exception:
        logging.error(f'Erro ao extrair dados: {Exception}')
    finally: # Finaliza a conexão
        if conn:
            conn.close()
    return vendas

if __name__ == "__main__":
    vendas = extrair_dados_vendas()
    for venda in vendas:
        print(f'Venda: {venda}')
    
    logging.info('Processo de extração concluído.')