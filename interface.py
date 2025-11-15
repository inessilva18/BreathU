import streamlit as st
import datetime
import random
import pandas as pd
import numpy as np

# =========================
# Funções de processamento
# =========================

def responder_pedido(pedido: str) -> str:
    pedido = pedido.lower().strip()

    if not pedido:
        return " Por favor, escreve algo antes de enviar."

    if "tarefas" in pedido:
        return "**Tarefas de hoje:**\n- Estudar IACD às 10h\n- Almoço às 12h30\n- Revisão de projeto às 16h."

    elif any(x in pedido for x in ["bem-estar", "emoção", "sentir", "humor"]):
        estado = random.choice(["feliz ", "motivado ", "cansado ", "stressado "])
        return f"Hoje pareces estar **{estado}**. Lembra-te de fazer pausas!"

    elif any(x in pedido for x in ["data", "dia", "hoje"]):
        return f" Hoje é **{datetime.date.today().strftime('%d/%m/%Y')}**."

    else:
        return " Não entendi bem. Podes tentar reformular o teu pedido?"

def escolher_forma_utilizador():
    st.subheader(" Como te sentes hoje?")
    opcoes = ["Feliz ", "Motivado ", "Cansado ", "Stressado ", "Neutro "]
    forma = st.selectbox("Escolhe o teu estado atual:", opcoes, index=4)

    if st.button(" Enviar forma"):
        st.success(f"Forma registada: {forma}")
        return forma
    return None

# =========================
# Início da App
# =========================

st.set_page_config(page_title="Assistente Inteligente - IACD UC", layout="wide")

if "historico" not in st.session_state:
    st.session_state.historico = []
if "calendario" not in st.session_state:
    st.session_state.calendario = []

st.sidebar.title(" Menu Principal")
menu = st.sidebar.radio("Navegação", ["Início", "Chat", "Calendário", "Relatórios", "Sobre"])

# =========================
# Página Inicial
# =========================

if menu == "Início":
    st.title(" Sistema Multiagente de Gestão de Tempo e Bem-Estar")
    st.write("""
Bem-vindo ao teu **assistente pessoal inteligente**!
Este sistema ajuda-te a:
- Organizar tarefas 
- Acompanhar o teu bem-estar 
- Otimizar a produtividade �
""")
    st.image("https://cdn.pixabay.com/photo/2025/09/07/22/40/anime-girl-9821145_1280.png", width=200)
    st.markdown("---")

# =========================
# Chat
# =========================

elif menu == "Chat":
    st.title(" Conversa com o teu assistente")
    st.markdown("Podes **escrever o teu pedido** abaixo!")

    pedido_texto = st.text_input(" Escreve o teu pedido:")

    if st.button(" Enviar pedido"):
        resposta = responder_pedido(pedido_texto)
        st.session_state.historico.append(("Tu", pedido_texto))
        st.session_state.historico.append(("Agente", resposta))

    st.markdown("---")

    # Placeholder para chat por voz (desativado)
    st.subheader(" Chat por voz (em breve)")
    st.info("A funcionalidade de gravação de voz não está disponível nesta versão da aplicação.")

    st.markdown("---")

    forma_utilizador = escolher_forma_utilizador()
    if forma_utilizador:
        st.session_state.historico.append(("Estado emocional", forma_utilizador))
        st.info(f"O agente registou o teu estado: {forma_utilizador}")

    st.markdown("---")

    st.subheader(" Histórico de Conversas")
    if len(st.session_state.historico) == 0:
        st.info("Ainda não há conversas registadas.")
    else:
        for autor, texto in st.session_state.historico:
            if autor == "Tu":
                st.markdown(
                    f"<div style='text-align:right;color:#1f77b4'><b>{autor}:</b> {texto}</div>",
                    unsafe_allow_html=True
                )
            elif autor == "Agente":
                st.markdown(
                    f"<div style='text-align:left;color:#2ca02c'><b>{autor}:</b> {texto}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='color:#9467bd'><b>{autor}:</b> {texto}</div>",
                    unsafe_allow_html=True
                )

# =========================
# Calendário
# =========================

elif menu == "Calendário":
    st.title(" Calendário Pessoal")

    st.markdown("###  Adicionar Novo Evento")
    titulo = st.text_input("Título do evento")
    data = st.date_input("Data", datetime.date.today())
    hora = st.time_input("Hora", datetime.time(9, 0))
    descricao = st.text_area("Descrição (opcional)")

    if st.button("Adicionar evento"):
        if titulo.strip():
            evento = {
                "Título": titulo,
                "Data": data.strftime("%d/%m/%Y"),
                "Hora": hora.strftime("%H:%M"),
                "Descrição": descricao
            }
            st.session_state.calendario.append(evento)
            st.success("Evento adicionado com sucesso!")
        else:
            st.warning("O título do evento é obrigatório!")

    st.markdown("---")
    st.markdown("### Eventos registados")

    if len(st.session_state.calendario) == 0:
        st.info("Ainda não existem eventos no calendário.")
    else:
        for i, ev in enumerate(st.session_state.calendario):
            with st.expander(f"{ev['Título']} — {ev['Data']} às {ev['Hora']}"):
                st.write(f"**Descrição:** {ev['Descrição'] or 'Sem descrição'}")
                if st.button(f" Eliminar evento {i+1}", key=f"del_{i}"):
                    st.session_state.calendario.pop(i)
                    st.rerun()

# =========================
# Relatórios
# =========================

elif menu == "Relatórios":
    st.title(" Relatórios de Bem-Estar e Produtividade")

    dias = ["Seg", "Ter", "Qua", "Qui", "Sex"]
    produtividade = np.random.randint(50, 100, len(dias))
    humor = np.random.randint(1, 10, len(dias))
    df = pd.DataFrame({"Produtividade (%)": produtividade, "Humor (1-10)": humor}, index=dias)

    st.line_chart(df)
    st.dataframe(df)
    st.success("Relatório gerado automaticamente!")

# =========================
# Sobre
# =========================

elif menu == "Sobre":
    st.title("ℹ️ Sobre o Projeto")
    st.write("""
Este website foi criado no âmbito da disciplina de **Inteligência Artificial e Resolução de Problemas**
do curso de **LIACD (Universidade de Coimbra)**.

 Nota: Este assistente é experimental.  
Caso sintas necessidade, procura sempre apoio psicológico adequado.
Obrigada:
 Beatriz e Inês 

""")
