import streamlit as st
import random

# --- Configurações do App (Título e Layout) ---
st.set_page_config(
    page_title="Missão Hokage Quiz",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Variáveis do Quiz ---
# Diálogos no estilo Naruto
NARUTO_DIALOGUE = [
    "Acredite! Eu vou me tornar o Hokage!",
    "Eu não vou fugir, nem vou voltar atrás na minha palavra! Este é o meu jeito ninja!",
    "Se você não gosta do seu destino, não aceite. Em vez disso, tenha a coragem de mudá-lo!",
    "Dattebayo! Vamos lá, tente responder a mais uma!",
]

HOKAGE_GOAL = 3 # Pontos necessários para se tornar Hokage

# Perguntas do Quiz
QUIZ_QUESTIONS = [
    {
        "pergunta": "O jutsu secreto do Naruto é o Rasengan.",
        "resposta": False,
        "explicação": "O **Jutsu Secreto** (ou exclusivo) do Naruto é o **Jutsu Multiclones das Sombras** (Kage Bunshin no Jutsu), não o Rasengan. O Rasengan é um jutsu de Rank-A.",
    },
    {
        "pergunta": "Naruto Uzumaki se torna o Sétimo Hokage de Konoha.",
        "resposta": True,
        "explicação": "Correto! Naruto realiza seu sonho e se torna o **Sétimo Hokage** (Nanadaime Hokage).",
    },
    {
        "pergunta": "O nome do sensei do Time 7 é Jiraiya.",
        "resposta": False,
        "explicação": "Errado! O sensei original do Time 7 era **Kakashi Hatake**. Jiraiya era um dos lendários Sannin e tutor de Naruto.",
    },
    {
        "pergunta": "O demônio selado dentro de Naruto é o Nove-Caudas (Kurama).",
        "resposta": True,
        "explicação": "Exato! Kurama, a Raposa de Nove-Caudas, estava selado dentro do Naruto.",
    },
    {
        "pergunta": "O clã Uchiha é famoso por possuir o Byakugan.",
        "resposta": False,
        "explicação": "O clã Uchiha é famoso por possuir o **Sharingan**. O Byakugan pertence ao clã Hyūga.",
    },
]

# Inicializa o estado de sessão
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False

# --- Funções de Lógica ---

def check_answer(user_answer, correct_answer, explanation):
    """Verifica a resposta, atualiza a pontuação e exibe feedback."""
    current_index = st.session_state.question_index
    
    # Previne que o usuário responda a mesma pergunta várias vezes e ganhe pontos
    if 'answered_q' not in st.session_state or current_index != st.session_state.answered_q:
        
        st.session_state.answered_q = current_index

        if user_answer == correct_answer:
            st.session_state.score += 1
            st.success(f"**Certo!** 🎉 Você marcou um ponto, Dattebayo!")
        else:
            st.error(f"**Errado!** 😔 Ah, que pena! Mas não desista!")
        
        st.info(f"**Explicação:** {explanation}")
        st.session_state.show_next = True # Habilita o botão 'Pró
