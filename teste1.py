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
        st.session_state.show_next = True # Habilita o botão 'Próxima Pergunta'
    else:
        st.warning("Já verificamos esta resposta, Ttebayo!")

def next_question():
    """Avança para a próxima pergunta."""
    st.session_state.question_index += 1
    st.session_state.show_next = False # Esconde o botão 'Próxima Pergunta'
    st.session_state.answered_q = -1 # Reseta o controle de resposta

def start_quiz():
    """Inicia o quiz e reseta o estado."""
    st.session_state.quiz_started = True
    st.session_state.score = 0
    st.session_state.question_index = 0
    st.session_state.show_next = False
    st.session_state.answered_q = -1
    random.shuffle(QUIZ_QUESTIONS) # Embaralha as perguntas

# --- Interface do Streamlit ---

st.title("Missão 🚀 Rumo a Hokage! (Quiz Naruto)")

if not st.session_state.quiz_started:
    # Tela Inicial
    st.header("Ei! Eu sou Naruto Uzumaki, e meu sonho é ser Hokage! Dattebayo!")
    st.markdown("Para provar sua força e inteligência e se tornar um verdadeiro Ninja, você precisa passar neste quiz de **Verdadeiro ou Falso**.")
    st.warning(f"Você precisa de **{HOKAGE_GOAL}** acertos para se tornar o próximo Hokage!")
    
    st.image("https://i.imgur.com/vH1NqXg.png", width=200) # Imagem simples de Naruto (link externo)

    if st.button("Começar Missão!", use_container_width=True, type="primary"):
        start_quiz()
        st.experimental_rerun()
else:
    # --- Jogo em Andamento ---

    current_score = st.session_state.score

    # Verifica se o usuário atingiu o objetivo
    if current_score >= HOKAGE_GOAL:
        st.balloons()
        st.success("## 🎉 MISSÃO CUMPRIDA! DATTEBAYO! 🎉")
        st.markdown(f"**Parabéns!** Com **{current_score}** acertos, você provou ser digno e se tornou o novo **Hokage** de Konoha! Acredite!")
        st.image("https://i.imgur.com/G3P2w2I.png", width=300) # Imagem de Hokage (link externo)
        if st.button("Recomeçar o Caminho Ninja", use_container_width=True):
            start_quiz()
            st.experimental_rerun()
        st.stop() # Interrompe a execução do quiz

    # Exibe a pontuação e progresso
    st.sidebar.markdown(f"## 🍥 Sua Pontuação (Hokage Meter):")
    st.sidebar.metric(label="Acertos", value=current_score)
    st.sidebar.progress(current_score / HOKAGE_GOAL)
    st.sidebar.markdown(f"**Faltam {HOKAGE_GOAL - current_score} para a glória!**")

    # Verifica se ainda há perguntas
    if st.session_state.question_index < len(QUIZ_QUESTIONS):
        
        # Pergunta atual
        q_data = QUIZ_QUESTIONS[st.session_state.question_index]
        question_text = q_data["pergunta"]
        correct_answer = q_data["resposta"]
        explanation = q_data["explicação"]

        st.markdown("---")
        
        # Diálogo de Naruto
        st.markdown(f"**Naruto diz:** _{random.choice(NARUTO_DIALOGUE)}_")
        
        st.header(f"Pergunta {st.session_state.question_index + 1}:")
        st.subheader(f"🤔 {question_text}")

        col1, col2 = st.columns(2)

        # Botões de Verdadeiro/Falso
        # Os botões ativam a função check_answer e passam a resposta do usuário
        
        # O argumento 'key' é essencial para que o Streamlit saiba qual botão foi clicado
        if col1.button("Verdadeiro", use_container_width=True, key=f"v_{st.session_state.question_index}", type="primary"):
            check_answer(True, correct_answer, explanation)

        if col2.button("Falso", use_container_width=True, key=f"f_{st.session_state.question_index}", type="secondary"):
            check_answer(False, correct_answer, explanation)

        st.markdown("---")
        
        # Botão para avançar (aparece apenas após responder)
        if st.session_state.get('show_next', False):
            if st.button("Próxima Pergunta, Dattebayo!", use_container_width=True):
                next_question()
                st.experimental_rerun()

    else:
        # Fim do Quiz (sem atingir o objetivo)
        st.warning("## Missão Hokage Falhada (Por enquanto...)")
        st.markdown(f"Você completou o quiz, mas conseguiu apenas **{current_score}** acertos. Você precisa treinar mais, Ttebayo!")
        if st.button("Tentar Novamente (Não desista!)", use_container_width=True, type="primary"):
            start_quiz()
            st.experimental_rerun()
