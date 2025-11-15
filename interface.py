# agente_processamento.py
import speech_recognition as sr
import streamlit as st
import datetime
import random
import pandas as pd
import numpy as np


def responder_pedido(pedido: str) -> str:
    pedido = pedido.lower()
    
    if "tarefas" in pedido:
        return " Tarefas de hoje:\n- Estudar IACD às 10h\n- Almoço às 12h30\n- Revisão de projeto às 16h."
    elif "bem-estar" in pedido or "emoção" in pedido:
        estado = random.choice(["feliz 😊", "motivado 💪", "cansado 😴", "stressado 😬"])
        return f"Hoje pareces estar {estado}. Lembra-te de fazer pausas!"
    elif "data" in pedido:
        return f"Hoje é {datetime.date.today().strftime('%d/%m/%Y')}"
    else:
        return " Não entendi bem. Podes tentar reformular o teu pedido?"
def escolher_forma_utilizador():
    """
    Permite ao utilizador selecionar a sua forma/estado emocional na interface.
    Retorna o estado escolhido como string.
    """
    st.subheader("Como te sentes hoje?")
    
    # Opções pré-definidas
    opcoes = ["Feliz ", "Motivado ", "Cansado ", "Stressado ", "Neutro "]
    
    # Selector
    forma = st.selectbox("Escolhe o teu estado atual:", opcoes)
    
    # Botão para submeter
    if st.button("Enviar forma"):
        st.success(f"Forma registada: {forma}")
        return forma
    return None

# app.py
import streamlit as st
from agente_processamento import responder_pedido
import pandas as pd
import numpy as np

# Configurações gerais
st.set_page_config(page_title="Assistente Inteligente - IACD UC", page_icon="🤖", layout="wide")

# Barra lateral (menu)
menu = st.sidebar.radio("📁 Menu", ["Início", "Chat", "Relatórios", "Sobre"])

# ---- Página Inicial ----
if menu == "Início":
    st.title(" Sistema Multiagente de Gestão de Tempo e Bem-Estar")
    st.write("""
    Bem-vindo ao teu assistente pessoal inteligente!  
    Este sistema multiagente ajuda-te a organizar tarefas, acompanhar o teu bem-estar e otimizar a produtividade.
    """)
    st.image("https://cdn.pixabay.com/photo/2025/09/07/22/40/anime-girl-9821145_1280.png", width=200)
    st.markdown("---")

# ---- Chat com o Agente ----
if menu == "Chat":
    st.title(" Conversa com o teu Agente Inteligente (agora com voz 🎙️)")

    if "historico" not in st.session_state:
        st.session_state.historico = []

    # Botão de gravação de voz
    st.subheader("🎤 Fala com o teu assistente")
    if st.button("🎙️ Falar"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("A ouvir... fala agora! 🎧")
            audio = recognizer.listen(source)
        
        try:
            pedido = recognizer.recognize_google(audio, language="pt-PT")
            st.success(f"Tu disseste: {pedido}")
        except sr.UnknownValueError:
            st.error(" Não percebi o que disseste.")
            pedido = ""
        except sr.RequestError:
            st.error("Erro na ligação com o serviço de voz.")
            pedido = ""
    else:
        pedido = st.text_input("Ou escreve o teu pedido aqui:")

    # Botão de envio manual
    if st.button("Enviar"):
        if pedido.strip():
            resposta = responder_pedido(pedido)
            st.session_state.historico.append(("👤 Tu", pedido))
            st.session_state.historico.append(("🤖 Agente", resposta))
        else:
            st.warning("Por favor, fala ou escreve algo antes de enviar.")

    st.markdown("---")

# Chama a função
    forma_utilizador = escolher_forma_utilizador()

    if forma_utilizador:
    # Aqui podes enviar para o agente, gerar recomendações, ou atualizar o histórico
      st.write(f"O agente recebeu a tua forma: {forma_utilizador}")

    # Mostrar histórico
    for autor, texto in st.session_state.historico:
        st.markdown(f"**{autor}:** {texto}")

# ---- Relatórios ----
elif menu == "Relatórios":
    st.title(" Relatórios de Bem-Estar e Produtividade")

    dias = ["Seg", "Ter", "Qua", "Qui", "Sex"]
    produtividade = np.random.randint(50, 100, len(dias))
    humor = np.random.randint(1, 10, len(dias))

    df = pd.DataFrame({"Produtividade (%)": produtividade, "Humor (1-10)": humor}, index=dias)

    st.line_chart(df)
    st.dataframe(df)

# ---- Sobre ----
elif menu == "Sobre":
    st.title("Sobre o Projeto")
    st.write("""""Este web site foi criado no âmbito da disciplina de Inteligência Artificial e Resilução de Problemas , do curso de LIACD (Universidade de Coimbra),
             a Inteligência Artificial pode conter falhas ou erros qualquer problema consulte ajuda psicológica adquada.
             Muito obrigada pela comprenção

             Beatriz e Inês!!
              """)