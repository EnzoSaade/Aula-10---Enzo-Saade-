import streamlit as st
import random

# --- Funções de Lógica do Quiz ---

def generate_question():
    """Gera uma única questão de matemática aleatória."""
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['+', '-', '*'])
    
    if operation == '+':
        problem = f"{num1} + {num2}"
        answer = num1 + num2
    elif operation == '-':
        # Garante que o resultado não seja negativo
        if num1 < num2:
            num1, num2 = num2, num1
        problem = f"{num1} - {num2}"
        answer = num1 - num2
    else: # '*'
        problem = f"{num1} x {num2}"
        answer = num1 * num2
        
    return {"problem": problem, "answer": answer}

def start_quiz(num_questions=10):
    """Inicia um novo quiz, redefinindo o estado da sessão."""
    st.session_state.quiz_generated = True
    st.session_state.current_score = 0
    st.session_state.question_index = 0
    st.session_state.questions = [generate_question() for _ in range(num_questions)]

def submit_answer():
    """Verifica a resposta do usuário e avança para a próxima pergunta."""
    if 'questions' not in st.session_state or st.session_state.question_index >= len(st.session_state.questions):
        return # Sai se o quiz não estiver ativo

    current_q = st.session_state.questions[st.session_state.question_index]
    
    try:
        user_answer = int(st.session_state.input_answer)
        if user_answer == current_q["answer"]:
            st.session_state.current_score += 1
            st.success("Correto!", icon="✅")
        else:
            st.error(f"Errado! A resposta correta era {current_q['answer']}.", icon="❌")
    except ValueError:
        st.warning("Por favor, insira um número válido.", icon="⚠️")
        return # Não avança se a resposta não for um número
        
    # Avança para a próxima pergunta
    if st.session_state.question_index < len(st.session_state.questions) - 1:
        st.session_state.question_index += 1
        st.session_state.input_answer = "" # Limpa o campo de entrada
    else:
        st.session_state.quiz_generated = False # Termina o quiz

# --- Configurações Iniciais do Streamlit ---

st.title("Quiz de Matemática Simples")

# Inicializa o estado da sessão
if 'quiz_generated' not in st.session_state:
    st.session_state.quiz_generated = False
    st.session_state.current_score = 0
    st.session_state.question_index = 0
    st.session_state.questions = []
    
# --- Estrutura da Interface do Usuário (UI) ---

if not st.session_state.quiz_generated:
    # Tela de Resultado / Início
    if st.session_state.questions:
        st.balloons()
        st.subheader("Quiz Finalizado!")
        st.markdown(f"Sua pontuação final é: **{st.session_state.current_score} / {len(st.session_state.questions)}**")
        
    if st.button("Iniciar Novo Quiz"):
        start_quiz(num_questions=10)
        st.rerun()
else:
    # Tela do Quiz em Andamento
    
    # Mostra a pontuação e o progresso
    col1, col2 = st.columns([1, 2])
    col1.metric(label="Pontuação", value=f"{st.session_state.current_score} / 10")
    col2.progress(
        (st.session_state.question_index) / len(st.session_state.questions), 
        text=f"Progresso: Pergunta {st.session_state.question_index + 1} de {len(st.session_state.questions)}"
    )

    # Mostra a pergunta atual
    current_q = st.session_state.questions[st.session_state.question_index]
    st.header(f"Pergunta {st.session_state.question_index + 1}:")
    st.subheader(f"Qual é o resultado de **{current_q['problem']}**?")

    # Campo de resposta e botão de envio
    st.text_input("Sua Resposta:", key="input_answer", on_change=submit_answer)
    st.button("Enviar Resposta", on_click=submit_answer)

    # Botão para recomeçar
    st.markdown("---")
    if st.button("Recomeçar o Quiz"):
        start_quiz(num_questions=10)
        st.rerun()
