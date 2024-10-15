import sqlite3
import random
from datetime import datetime, timedelta

def generate_sales_data(num_records=500):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    products = list(range(101, 111))  # 10 produtos
    regions = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
    
    sales_data = []
    for _ in range(num_records):
        sale_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        product_id = random.choice(products)
        customer_id = random.randint(1001, 2000)
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(10.0, 100.0), 2)
        total_value = round(quantity * unit_price, 2)
        seller_id = random.randint(1, 20)
        region = random.choice(regions)
        
        # Criar a tupla sem o 'id', que será gerado automaticamente
        sale = (sale_date.strftime('%Y-%m-%d'), product_id, customer_id, quantity, unit_price, total_value, seller_id, region)
        sales_data.append(sale)
    return sales_data

# Conexão com o SQLite/Criar tabela vendas
conn = sqlite3.connect('data/vendas.db')
cursor = conn.cursor()
cursor.execute(''' 
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_venda DATE NOT NULL,
    id_produto INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_unitario DECIMAL(10, 2) NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    id_vendedor INTEGER NOT NULL,
    regiao VARCHAR(50) NOT NULL)
               ''')

# Gera 500 Registros e insere no banco de dados padronizado
sales_data  = generate_sales_data(500) 

cursor.executemany(''' 
INSERT INTO vendas (data_venda,id_produto, id_cliente, quantidade, valor_unitario, valor_total, id_vendedor, regiao)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', sales_data)

conn.commit()
print(f'{len(sales_data)} registros incluídos no SQLite')
conn.close()