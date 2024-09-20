import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional
import logging

# Configurar o logging para o módulo
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def consultar_tabela(data_filtro: Optional[str] = None) -> pd.DataFrame:
    """
    Consulta a tabela 'finanças' no banco de dados DuckDB.
    
    Args:
        data_filtro (Optional[str]): Filtro de data para consultar dados específicos.
    
    Returns:
        pd.DataFrame: DataFrame com os dados consultados.
    """
    conn = duckdb.connect('data/dev.duckdb')
    query = 'SELECT * FROM poc'
    if data_filtro:
        query += ' WHERE data = ?'
        df = conn.execute(query, (data_filtro,)).fetchdf()
    else:
        df = conn.execute(query).fetchdf()
    
    conn.close()
    
    logging.info(f"Dados consultados com sucesso. Linhas retornadas: {len(df)}")
    return df

def calcular_metricas(df: pd.DataFrame):
    """
    Calcula as métricas principais: despesas fixas, despesas variáveis, receita e receita líquida.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os dados financeiros.

    Returns:
        dict: Dicionário com os valores das métricas.
    """
    despesas_fixa = df[df["tipo"] == "DESPESA_FIXA"]["valor_final"].sum()
    despesas_variavel = df[df["tipo"] == "DESPESA_VARIAVEL"]["valor_final"].sum()
    receita = df[df["tipo"] == "RECEITA_FIXA"]["valor_final"].sum()
    receita_liquida = receita - (despesas_fixa + despesas_variavel)

    return {
        "despesa_fixa": despesas_fixa,
        "despesa_variavel": despesas_variavel,
        "receita": receita,
        "receita_liquida": receita_liquida
    }

def criar_grafico_despesas_receita(df: pd.DataFrame) -> go.Figure:
    """
    Cria um gráfico de barras empilhadas comparando despesas fixas e variáveis com uma linha para receita.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados financeiros.

    Returns:
        go.Figure: Gráfico de barras empilhadas com linha para receita.
    """
    df_grouped = df.groupby(['data', 'tipo'])['valor_final'].sum().reset_index()

    fig = go.Figure()

    # Adicionar barras para despesas
    for tipo, cor in {'DESPESA_FIXA': 'darkblue', 'DESPESA_VARIAVEL': 'lightblue'}.items():
        fig.add_trace(go.Bar(
            x=df_grouped[df_grouped['tipo'] == tipo]['data'],
            y=df_grouped[df_grouped['tipo'] == tipo]['valor_final'],
            name=tipo,
            marker_color=cor,
            text=[f'R$ {v:,.2f}' for v in df_grouped[df_grouped['tipo'] == tipo]['valor_final']],  # Valor formatado com 2 casas decimais
            textposition='auto'
        ))

    # Adicionar linha para receita
    fig.add_trace(go.Scatter(
        x=df_grouped[df_grouped['tipo'] == 'RECEITA_FIXA']['data'],
        y=df_grouped[df_grouped['tipo'] == 'RECEITA_FIXA']['valor_final'],
        name='Receita Fixa',
        mode='lines+markers',
        line=dict(color='gold', width=2),
        text=[f'R$ {v:,.2f}' for v in df_grouped[df_grouped['tipo'] == 'RECEITA_FIXA']['valor_final']],  # Valor formatado com 2 casas decimais
        textposition='top center'
    ))

    fig.update_layout(
        title='Comparação de Despesas e Receita por Mês',
        xaxis_title='Data',
        yaxis_title='Valores (R$)',
        barmode='stack'
    )

    logging.info("Gráfico de despesas e receita criado com sucesso.")
    return fig

def criar_grafico_categoria(df: pd.DataFrame) -> go.Figure:
    """
    Cria um gráfico de barras horizontal mostrando as despesas por categoria.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados financeiros.

    Returns:
        go.Figure: Gráfico de barras horizontal para despesas por categoria.
    """
    df_despesas = df[df['tipo'].isin(['DESPESA_FIXA', 'DESPESA_VARIAVEL'])]
    df_categoria = df_despesas.groupby('categoria')['valor_final'].sum().reset_index()

    fig_categoria = px.bar(df_categoria,
                           x='valor_final',
                           y='categoria',
                           title='Despesas por Categoria',
                           orientation='h',
                           text='valor_final',  # Adiciona o texto do valor sobre as barras
                           color='categoria',
                           color_discrete_map={
                               "DESPESA_FIXA": "darkblue",
                               "DESPESA_VARIAVEL": "lightblue"
                           })

    # Atualizar layout para formatar o texto com 2 casas decimais
    fig_categoria.update_traces(texttemplate='R$ %{text:,.2f}', textposition='auto')

    logging.info("Gráfico de despesas por categoria criado com sucesso.")
    return fig_categoria
