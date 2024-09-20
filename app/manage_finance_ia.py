import os
import json
import pandas as pd
import streamlit as st
from groq import Groq

def obter_sugestao_financeira(df):
    """
    Função que envia as métricas financeiras para o Llama 3.1 e retorna sugestões de melhorias financeiras.
    """

    # Carregar a chave da API
    working_dir = os.path.dirname(os.path.abspath(__file__))
    config_data = json.load(open(f"{working_dir}/config.json"))

    GROQ_API_KEY = config_data["GROQ_API_KEY"]
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

    # Inicializar o cliente Groq
    client = Groq()

    # Inicializar o histórico de chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Exibir histórico de mensagens no Streamlit
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input do usuário para perguntar sobre finanças
    user_prompt = st.chat_input("Pergunte como melhorar suas finanças")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        # Criar a mensagem com as métricas
        messages = [
            {"role": "system", "content": "Você é um assistente financeiro altamente capacitado, especializado em identificar oportunidades de melhorar a gestão financeira pessoal. Sua tarefa é analisar os seguintes dados financeiros e fornecer críticas construtivas, bem como estratégias para aumentar a riqueza a longo prazo. Concentre-se em sugerir reduções de gastos desnecessários, melhorar a alocação de recursos e identificar oportunidades de investimento."},
            {"role": "user", "content": f"As métricas atuais são: {df}."},
            *st.session_state.chat_history
        ]

        # Enviar para o modelo Llama 3.1
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        # Obter a resposta do assistente
        assistant_response = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

        # Exibir a resposta no Streamlit
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
