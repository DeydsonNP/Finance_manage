import duckdb
import pandas as pd

def load_query_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Crie uma conexão com DuckDB
conn = duckdb.connect('data/dev.duckdb')

# Carregue o CSV local em um DataFrame do pandas
RECEITA_FIXA = pd.read_csv('/home/deydson/projects_data_engineer/finance_manager/data/Gestão - Receita_fixa.csv')
DESPESA_FIXA = pd.read_csv('/home/deydson/projects_data_engineer/finance_manager/data/Gestão - Despesas_fixas.csv')
DESPESA_VARIADA = pd.read_csv('/home/deydson/projects_data_engineer/finance_manager/data/Gestão - Despesas_variaveis.csv')
DESPESA_ATUAL = pd.read_csv('data/Extrato-01-09-2024-a-17-09-2024.csv', delimiter=';', skiprows=4)
POC = pd.read_csv('/home/deydson/projects_data_engineer/finance_manager/data/Gestão - poc.csv')

# Registre o DataFrame no DuckDB
conn.register('DESPESA_ATUAL', DESPESA_ATUAL)
conn.register('RECEITA_FIXA', RECEITA_FIXA)
conn.register('DESPESA_FIXA', DESPESA_FIXA)
conn.register('DESPESA_VARIADA', DESPESA_VARIADA)

sql_query = load_query_from_file('/home/deydson/projects_data_engineer/finance_manager/transform/sql/transform.sql')

# Execute uma consulta SQL para transformar os dados
resultado = conn.execute("CREATE OR REPLACE TABLE poc AS SELECT * FROM POC ").df()

# Exiba o resultado
print(resultado)

# Feche a conexão
conn.close()
