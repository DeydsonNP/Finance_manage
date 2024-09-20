import streamlit as st
import pandas as pd
import duckdb

# Conectar ao banco de dados DuckDB (pode ser um arquivo ou um banco em memória)
db_connection = duckdb.connect('financeiro.db')  # Substitua pelo caminho do seu arquivo .db se necessário

def processar_csv_e_inserir_no_duckdb(uploaded_file, table_name="transacoes_financeiras"):
    # Lê o arquivo CSV para um DataFrame
    df = pd.read_csv(uploaded_file)

    # Seleciona as colunas de acordo com o schema
    df = df[['data', 'tipo', 'descricao', 'categoria', 'valor', 'forma_pagamento', 'obs']]

    # Verifica se a tabela já existe
    table_exists = db_connection.execute(f"SELECT count(*) FROM information_schema.tables WHERE table_name = '{table_name}'").fetchone()[0]

    if table_exists == 0:
        # Se a tabela não existe, cria a tabela com o schema especificado
        db_connection.execute(f"""
            CREATE TABLE {table_name} (
                data DATE,
                tipo VARCHAR,
                descricao VARCHAR,
                categoria VARCHAR,
                valor DOUBLE,
                forma_pagamento VARCHAR,
                obs VARCHAR
            )
        """)
        st.write(f"Tabela '{table_name}' criada.")

    # Faz o INSERT no DuckDB
    db_connection.execute(f"INSERT INTO {table_name} SELECT * FROM df")
    st.write(f"Dados inseridos na tabela '{table_name}'.")

    # Exibe os dados armazenados no DuckDB para confirmação
    consulta_df = db_connection.execute(f"SELECT * FROM {table_name}").fetch_df()
    st.write("Dados armazenados no DuckDB:")
    st.dataframe(consulta_df)

# Título do App
st.title('App de Gestão Financeira')

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Envie seu arquivo CSV", type=["csv"])

# Verifica se um arquivo foi enviado
if uploaded_file is not None:
    processar_csv_e_inserir_no_duckdb(uploaded_file)
else:
    st.write("Por favor, envie um arquivo CSV para visualizar os dados e gravá-los no DuckDB.")
