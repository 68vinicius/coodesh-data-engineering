import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

# Script para conectar-se ao banco de dados SQLite e extrair registros da tabela vendas
def extract_sales_data(db_path='data/vendas.db'):
    conn = None
    vendas = []
    try: # Conecta com o banco e realiza a consulta
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vendas')
        vendas = cursor.fetchall()
        logging.info(f"{len(vendas)} dados extraídos com sucesso.")
    except Exception:
        logging.error(f"Erro ao extrair dados: {Exception}")
    finally:
        if conn:
            conn.close()
    return vendas

if __name__ == "__main__":
    vendas = extract_sales_data()
    for venda in vendas:
        print(f"Venda: {venda}")
    
    logging.info("Processo de extração concluído.")
