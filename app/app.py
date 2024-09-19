import streamlit as st
import duckdb
import pandas as pd

# Função para conectar ao banco de dados DuckDB e consultar a tabela
def consultar_tabela():
    # Crie uma conexão com DuckDB
    conn = duckdb.connect('dev.duckdb')
    
    # Execute a consulta SQL
    df = conn.execute('SELECT * FROM financas').fetchdf()
    
    # Feche a conexão
    conn.close()
    
    return df

# Configuração da página do Streamlit
st.set_page_config(page_title='Visualização de Tabela DuckDB', layout='wide')

# Título da aplicação
st.title('Visualização da Tabela Funcionários')

# Consulte os dados da tabela
df = consultar_tabela()

# Exiba a tabela no Streamlit
st.write("Dados da tabela 'funcionarios':")
st.dataframe(df)
