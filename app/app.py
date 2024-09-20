import streamlit as st
import logging
from charts import consultar_tabela, criar_grafico_despesas_receita, criar_grafico_categoria, calcular_metricas
from manage_finance_ia import obter_sugestao_financeira

# Configurar o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Função principal para executar o aplicativo Streamlit.
    """
    st.set_page_config(page_title='Visualização Financeira', layout='wide')
    st.title('Visualização de Dados Financeiros')

    # Consultar os dados e configurar o filtro de data
    df_inicial = consultar_tabela()
    
    if df_inicial.empty:
        st.error("A tabela de dados está vazia. Verifique o banco de dados.")
        logging.error("Tabela de dados vazia")
        return

    data_opcoes = ["Todas as datas"] + sorted(df_inicial['data'].unique().tolist())
    data_selecionada = st.selectbox("Selecione uma data:", data_opcoes)

    # Aplicar filtro de data
    data_filtro = None if data_selecionada == "Todas as datas" else data_selecionada
    df = consultar_tabela(data_filtro)

    # Exibir tabela de dados
    if not df.empty:
        st.write("Dados da tabela 'finanças':")
        st.dataframe(df)
        
    else:
        st.warning("Nenhum dado disponível para a data selecionada.")
        logging.warning(f"Nenhum dado disponível para a data: {data_filtro}")
        return

    # Exibir gráficos
    try:


        # Calcular métricas
        metricas = calcular_metricas(df)

        # Exibir as métricas
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("DESPESA FIXA", f"R$ {metricas['despesa_fixa']:.2f}")
        col2.metric("DESPESA VARIAVEL", f"R$ {metricas['despesa_variavel']:.2f}")
        col3.metric("Receita", f"R$ {metricas['receita']:.2f}")
        col4.metric("Receita Líquida", f"R$ {metricas['receita_liquida']:.2f}")

        fig_despesas_receita = criar_grafico_despesas_receita(df)
        st.plotly_chart(fig_despesas_receita)

        st.subheader('Despesas por Categoria')
        fig_categoria = criar_grafico_categoria(df)
        st.plotly_chart(fig_categoria)

        obter_sugestao_financeira(df_inicial)

    except Exception as e:
        st.error("Ocorreu um erro ao exibir os gráficos.")
        logging.error(f"Erro ao gerar os gráficos: {e}")

if __name__ == "__main__":
    main()
