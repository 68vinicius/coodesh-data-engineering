# **Teste Prático para Engenheiro e Analista de Dados**

### Cenário

Uma empresa está migrando dados de um sistema legado (representado por um banco de dados SQL) para sua nova arquitetura baseada em AWS. Você precisa criar um pipeline de dados que extraia informações do banco de dados, transforme-as e as carregue no Data Lake (S3).

## **Tópicos**
1. [Introdução](#1-introdução)
2. [Visão Geral do Projeto](#2-visão-geral-do-projeto)
3. [Arquitetura do Pipeline](#3-arquitetura-do-pipeline)
    - [Extração de Dados](#extração-de-dados)
    - [Transformação de Dados](#transformação-de-dados)
    - [Carregamento de Dados](#carregamento-de-dados)
4. [Visualização de Dados](#4-visualização-de-dados)
5. [Consultas SQL para Análise de Vendas](#5-consultas-sql-para-análise-de-vendas)
6. [Modelo de Machine Learning](#6-modelo-de-machine-learning-tempo-não-permitiu)
7. [Escolha das Ferramentas e Tecnologias](#7-escolha-das-ferramentas-e-tecnologias)
8. [Possibilidades de Melhorias Futuras](#8-possibilidades-de-melhorias-futuras)
9. [Configuração Inicial](#9-configuração-inicial)
10. [LinkedIn](https://www.linkedin.com/in/viunicius/)

---

## **1. Introdução**

Este documento descreve o design e a implementação de um **pipeline de ETL** (Extração, Transformação e Carregamento) para a análise de dados de vendas. O pipeline é composto por três etapas principais: **extração**, **transformação** e **carregamento**. A partir de um banco de dados SQLite, o projeto visa mostrar como os dados podem ser processados, limpos e organizados de maneira eficiente para análise e visualização.

---

## **2. Visão Geral do Projeto**

O projeto segue a metodologia de pipeline de dados, onde as etapas são bem definidas e executadas sequencialmente. O processo de ETL implementado se baseia em três módulos principais:

- **Extração**: Os dados de vendas são extraídos de um banco de dados SQLite.
- **Transformação**: Os dados extraídos são transformados em um formato mais adequado para análise, incluindo a remoção de duplicatas e o cálculo de métricas adicionais.
- **Carregamento**: Os dados transformados são carregados em um formato de arquivo CSV organizado em diretórios simulando um "bucket" S3.

## Estrutura de Pastas

```plaintext
.
├── data
│   └── vendas.db              # Banco de dados SQLite contendo dados de vendas.
├── bucket_S3                  # Estrutura que simula um bucket S3.
│   └── 2023                   # Ano 
│       ├── 01                 # Mês
│           ├── 03             # Dia
│               └── vendas_01_20230101.csv
├── ETL
│   ├── consulta.sql           # Consulta SQL para análise de vendas.
│   ├── extract.py             # Script que extrai dados do banco de dados SQLite.
│   ├── transform.py           # Script que transforma os dados extraídos em um DataFrame.
│   └── loading.py             # Script que carrega os dados transformados simulando o carregamento para S3.
├── utils
│   └── generate_sales_data.py # Gera 500 registros de dados fictícios e os insere no banco de dados.
├── pipeline.py                # Script principal que orquestra a execução do pipeline ETL.
└── README.md                  # Documentação do projeto.
```

---

## **3. Arquitetura do Pipeline**
### **Diagrama do Projeto**
![Imagem do código](https://i.imgur.com/0rXZtrW.png)
A arquitetura desenvolvida neste projeto utiliza uma abordagem de armazenamento em camadas, dividindo os dados em três estágios principais: bruto, processamento e consulta. Essa estrutura visa otimizar custos e desempenho, permitindo uma gestão eficiente dos dados.

### **Extração de Dados**
Na primeira etapa, os dados de vendas são extraídos do banco de dados SQLite. 

![Imagem do código](https://i.imgur.com/l666uda.png)
A extração é realizada através de uma consulta simples que busca todos os registros da tabela `vendas`.

### **Transformação de Dados**
A transformação dos dados é feita usando **Pandas**, uma biblioteca popular de Python. As etapas de transformação incluem:

![Imagem do código](https://i.imgur.com/4TdMug4.png)
- **Remoção de Duplicatas**: Para garantir a qualidade dos dados, qualquer registro duplicado é identificado e removido.
- **Conversão de Datas**: As datas são convertidas para o formato ISO, facilitando as consultas e a análise temporal dos dados.
- **Cálculo de Métricas**: É calculado o total de vendas por dia, uma métrica importante para a análise de desempenho.

### **Carregamento de Dados**
Após a transformação, os dados são organizados em um formato que simula o carregamento para o S3. Os dados são particionados por **ano**, **mês** e **dia**, e armazenados como arquivos CSV. 

![Imagem do código](https://i.imgur.com/G28YuOj.png)
Cada venda é salva em um arquivo CSV por registro, e todos os arquivos são armazenados em uma estrutura de diretórios que simula um bucket S3.

#### Limitações e Melhorias Futuras:
Embora o formato CSV tenha sido escolhido por simplicidade, para um ambiente de produção, o uso de **Parquet** seria mais apropriado, pois ele oferece:

- **Compactação**: O Parquet compacta os dados de maneira mais eficiente, economizando espaço de armazenamento.
- **Desempenho**: Formatos como Parquet permitem consultas mais rápidas em grandes conjuntos de dados, pois os dados são armazenados em colunas e não em linhas, o que melhora o desempenho das consultas analíticas.

A estrutura em **Parquet** também oferece suporte a tipos de dados mais complexos e é compatível com plataformas de processamento distribuído como **Apache Spark** e **Amazon Redshift**.

---

## **4. Visualização de Dados**

![Imagem do DashBoard](https://i.imgur.com/etwUBwA.jpeg)

O dashboard proposto inclui os seguintes elementos para apresentar os insights chave dos dados de vendas:

- **Produtos Mais Vendidos**
- **Receita Total**
- **Ticket Médio**
- **Total de Vendas**
- **Clientes**
- **Vendas por Região**
- **Receita Mensal**
- **Top Vendedores**

---

## **5. Consultas SQL para Análise de Vendas**

Consulta para calcular o total de vendas por mês no Amazon Athena:

```sql
SELECT year(data_venda) AS ano,
       month(data_venda) AS mes,
       SUM(valor_total) AS vendas_totais
FROM vendas
GROUP BY year(data_venda), month(data_venda)
ORDER BY ano, mes;
```

---

## **6. Modelo de Machine Learning (Tempo Não Permitiu)**

Para prever vendas futuras, seria possível implementar um modelo utilizando scikit-learn no Amazon SageMaker. A ideia é prever o total de vendas com base em características como data da venda, quantidade vendida, preço unitário, e outros fatores relevantes.

Após a preparação, os dados seriam divididos em conjuntos de treinamento e teste. Diferentes algoritmos de regressão, como Regressão Linear e modelos mais complexos como Random Forest, seriam avaliados para encontrar a melhor adaptação aos dados. O modelo seria treinado com o conjunto de treinamento e validado com métricas como MAE (Erro Absoluto Médio) e R².

Uma vez validado, o modelo poderia ser implantado no Amazon SageMaker, permitindo previsões em tempo real. Isso ajudaria a empresa a ajustar seu estoque e estratégias de marketing de acordo com as previsões de vendas.

---

## **7. Escolha das Ferramentas e Tecnologias**

### **SQLite**
O banco de dados SQLite foi escolhido como fonte de dados para o projeto. Ele oferece uma solução simples e eficaz para armazenar e consultar os dados, além de ser fácil de configurar e usar em ambientes de desenvolvimento e testes.

### **Pandas**
A biblioteca **Pandas** foi utilizada para a transformação dos dados. Ela permite a manipulação e análise de grandes volumes de dados de forma eficiente e flexível.

### **Uso de Arquivos Estruturados para ETL**
A decisão de dividir o processo de ETL em três arquivos distintos (`extract.py`, `transform.py`, `loading.py`) foi intencional para garantir uma melhor organização e manutenibilidade do código. Cada arquivo tem uma responsabilidade clara, seguindo o princípio de separação de preocupações:
- **`extract.py`**: Responsável pela extração de dados do banco de dados.
- **`transform.py`**: Focado na transformação e limpeza dos dados.
- **`loading.py`**: Encarga-se do carregamento dos dados em um formato apropriado.

Essa estrutura modular facilita alterações futuras, melhora a manutenibilidade ao permitir identificação rápida de problemas, favorece a escalabilidade com adaptações independentes, e promove a colaboração, testabilidade e reusabilidade do código.

### **Armazenamento de Dados: CSV Simulado para S3**
A escolha de usar arquivos CSV para simular o carregamento em um **bucket S3** foi uma decisão prática para facilitar a implementação e a validação do pipeline. Embora o CSV seja amplamente utilizado e fácil de entender, ele apresenta limitações, como o tamanho do arquivo e a falta de suporte a tipos de dados complexos.

### **Escalabilidade**
Embora o pipeline atual funcione bem com um pequeno volume de dados, a escalabilidade será um fator crítico se o volume de dados aumentar. O uso de AWS S3 e Parquet, juntamente com a biblioteca **Boto3** para interações com a AWS, permitiria que o pipeline escalasse para lidar com dados massivos e complexos, com maior eficiência.

---

## **8. Possibilidades de Melhorias Futuras**

- **Governança de Dados:** Implementar controle de acesso e garantir conformidade com regulamentações como GDPR e LGPD para proteger dados sensíveis.
  
- **Integração de CI/CD:** Adotar práticas DevOps para automação de testes, monitoramento e deploy automático, melhorando agilidade e segurança no desenvolvimento.

- **Testes no Pipeline:** Implementar testes unitários e de integração com **pytest** para assegurar a qualidade e integridade dos dados.

- **Automatização e Orquestração:** Integrar ferramentas como **Apache Airflow** ou **AWS Step Functions** para automatizar a execução do pipeline e gerenciar falhas.

---

## **9. Configuração Inicial**

1. Clone o repositório:

```
git clone https://github.com/68vinicius/coodesh-data-engineering.git
cd coodesh-data-engineering
```

2. Instale as dependências do projeto:
```
poetry install
```

3. Execute o ambiente virtual:
```
poetry shell
```

4. Execute o pipeline:
```
python pipeline.py
```

---

## **10. Conecte-se comigo no [LinkedIn](https://www.linkedin.com/in/viunicius/)**
