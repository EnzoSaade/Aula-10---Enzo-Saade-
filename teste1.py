import streamlit as st
import random

# --- Funções de Ajuda e Variáveis de Estado ---

def init_session_state():
    """Inicializa as variáveis de estado da sessão."""
    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'last_attempt_correct' not in st.session_state:
        st.session_state.last_attempt_correct = None
    if 'question' not in st.session_state:
        st.session_state.question = None
    if 'level_max_value' not in st.session_state:
        # Valor inicial para a dificuldade (começa fácil)
        st.session_state.level_max_value = 10 

def reset_game():
    """Reinicia a pontuação e a dificuldade do jogo."""
    st.session_state.score = 0
    st.session_state.level_max_value = 10
    st.session_state.last_attempt_correct = None
    generate_new_question()

def generate_new_question():
    """Gera uma nova questão com base no nível de dificuldade atual."""
    
    score = st.session_state.score
    
    # 1. Aumento Agressivo da Dificuldade (usando 2.0 como base)
    st.session_state.level_max_value = int(10 * (2.0 ** score))
    
    max_val = st.session_state.level_max_value
    
    # Define os limites para os números: mínimo 1, máximo 1000
    limit = min(max_val, 1000)
    
    # 2. Escolha de Operação Mista (incluindo Multiplicação e Subtração)
    operations = ['+', '+'] # Adição é mais comum no início
    if score >= 3:
        operations.append('-') # Adiciona Subtração após 3 acertos
    if score >= 6:
        operations.append('*') # Adiciona Multiplicação após 6 acertos
        
    op1 = random.choice(operations)
    
    # Gera os dois primeiros números
    num1 = random.randint(1, limit)
    num2 = random.randint(1, limit)
    
    # Garante que o resultado da subtração não seja negativo
    if op1 == '-' and num1 < num2:
        num1, num2 = num2, num1

    question_text = f"{num1} {op1} {num2}"
    
    # 3. Adiciona a Terceira Variável em Níveis Altos
    if score >= 7:
        op2 = random.choice(['+', '-'])
        num3 = random.randint(1, int(limit / 5)) # Terceiro número menor
        question_text += f" {op2} {num3}"
        
        # Calcula a resposta com base na ordem de operações (da esquerda para a direita)
        if op1 == '+':
            result = num1 + num2
        elif op1 == '-':
            result = num1 - num2
        else: # op1 == '*'
            result = num1 * num2
        
        if op2 == '+':
            answer = result + num3
        else: # op2 == '-'
            answer = result - num3
            
    else:
        # Calcula a resposta para duas variáveis
        if op1 == '+':
            answer = num1 + num2
        elif op1 == '-':
            answer = num1 - num2
        else: # op1 == '*'
            answer = num1 * num2
    
    st.session_state.question = (question_text, answer)
    
    # Forçando o re-run: CORREÇÃO DEVIDA AO ERRO
    st.rerun()


def check_answer():
    """Verifica a resposta do usuário."""
    user_input = st.session_state.user_input
    
    if st.session_state.question is None:
        return

    _, correct_answer = st.session_state.question

    try:
        user_answer_num = int(user_input)
        
        if user_answer_num == correct_answer:
            st.session_state.score += 1
            st.session_state.last_attempt_correct = True
            
            if st.session_state.score < 10:
                st.success(f"Parabéns, {st.session_state.name}! Resposta correta!")
                generate_new_question()
            else:
                # O jogo termina com 10 acertos
                pass 
            
        else:
            st.error(f"Resposta incorreta, {st.session_state.name} 😔. A resposta correta era **{correct_answer}**.")
            st.session_state.last_attempt_correct = False
            st.session_state.game_started = False # Fim do jogo por erro
            
    except ValueError:
        st.warning("Por favor, digite apenas um número inteiro.")


# --- Layout do Aplicativo Streamlit ---

init_session_state()

st.set_page_config(
    page_title="Desafio de Matemática Difícil",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🤯 Desafio da Matemática: HARD MODE")
st.markdown("---")

# Área de Entrada do Nome do Usuário
if not st.session_state.name:
    st.header("Seja Bem-Vindo(a) ao Modo Difícil!")
    
    with st.form(key='name_form'):
        name_input = st.text_input("Qual é o seu nome?", key="input_name_widget")
        submit_button = st.form_submit_button("Começar Desafio HARD")
        
        if submit_button and name_input:
            st.session_state.name = name_input.title().strip()
            st.session_state.game_started = True
            st.success(f"Coragem, {st.session_state.name}! Este será difícil!")
            generate_new_question()
        elif submit_button and not name_input:
            st.warning("Por favor, digite seu nome para começar.")

# --- Lógica do Jogo ---

elif st.session_state.game_started and st.session_state.score < 10:
    # Jogo em andamento

    st.markdown(f"### Olá, **{st.session_state.name}**!")
    st.info("Regras: 10 acertos seguidos para a vitória. Multiplicação e Subtração serão adicionadas à medida que você avança!")
    
    # Exibe a pontuação e o nível de dificuldade
    col1, col2 = st.columns(2)
    col1.metric("Pontuação Atual", st.session_state.score)
    # Exibe o limite máximo do número na questão
    col2.metric("Nível de Dificuldade (Máx. Valor)", min(st.session_state.level_max_value, 1000))
    
    st.markdown("---")
    
    # Exibe a Pergunta
    if st.session_state.question:
        question_text, _ = st.session_state.question
        st.header(f"Questão {st.session_state.score + 1}:")
        st.markdown(f"## **{question_text}** = ?")
        
        # Formulário para a resposta
        with st.form(key='quiz_form'):
            answer_input = st.number_input(
                "Sua Resposta:", 
                min_value=-999999, 
                step=1, 
                key="user_input", 
                help="Digite sua resposta e clique em 'Enviar'."
            )
            submit_answer = st.form_submit_button("Enviar Resposta", on_click=check_answer)
            

# --- Fim de Jogo (Vitória ou Derrota) ---

elif st.session_state.score == 10:
    # Vitória
    st.balloons()
    st.success(f"## 👑 MESTRE DA MATEMÁTICA! Parabéns, {st.session_state.name}!")
    st.markdown("Você acertou **10 questões seguidas** e venceu o Desafio HARD!")
    
    if st.button("Tentar Novamente (Recomeçar)"):
        reset_game()

elif st.session_state.name and st.session_state.last_attempt_correct == False:
    # Derrota
    st.error(f"## 💀 Você foi derrotado, {st.session_state.name}.")
    st.markdown(f"Você errou a última questão. Sua pontuação final foi de **{st.session_state.score} acertos**.")
    st.markdown("A dificuldade foi alta! Clique para tentar de novo e dominar o desafio.")
    
    if st.button("Tentar Novamente (Recomeçar)"):
        reset_game()

elif st.session_state.name and not st.session_state.game_started:
    # Tela de espera
    st.markdown(f"### Olá, **{st.session_state.name}**!")
    st.info("Clique abaixo para começar a provar seu valor.")
    if st.button("Iniciar Desafio de Matemática"):
        st.session_state.game_started = True
        reset_game()
