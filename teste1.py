import streamlit as st
import random

# --- Configuração Inicial e Variáveis de Estado ---

def init_session_state():
    """Inicializa as variáveis de estado da sessão."""
    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'current_answer' not in st.session_state:
        st.session_state.current_answer = None
    if 'last_attempt_correct' not in st.session_state:
        st.session_state.last_attempt_correct = None
    if 'question' not in st.session_state:
        st.session_state.question = None
    if 'level_max_value' not in st.session_state:
        # Valor inicial para a dificuldade (limite máximo para os números da soma)
        st.session_state.level_max_value = 10 

def reset_game():
    """Reinicia a pontuação e a dificuldade do jogo."""
    st.session_state.score = 0
    st.session_state.level_max_value = 10
    st.session_state.last_attempt_correct = None
    generate_new_question()

def generate_new_question():
    """Gera uma nova questão com base no nível de dificuldade atual."""
    # O máximo é 10 (nível 1) até 1000 (nível 10)
    max_val = st.session_state.level_max_value 
    
    # Gera dois números aleatórios entre 1 e o valor máximo
    num1 = random.randint(1, max_val)
    num2 = random.randint(1, max_val)
    
    question = f"{num1} + {num2}"
    answer = num1 + num2
    
    st.session_state.question = (question, answer)
    st.session_state.current_answer = None # Limpa a resposta anterior
    
    # Aumenta a dificuldade para a próxima rodada (ex: 10, 20, 40, 80, 160...)
    # O aumento é progressivo.
    if st.session_state.score < 10:
        st.session_state.level_max_value = int(10 * (1.5 ** st.session_state.score))
    
    # Garante que o valor máximo não seja absurdamente grande
    if st.session_state.level_max_value > 1000:
        st.session_state.level_max_value = 1000
    
    # FORÇANDO O RE-RUN: CORREÇÃO APLICADA AQUI
    st.rerun()


def check_answer():
    """Verifica a resposta do usuário."""
    # O valor digitado pelo usuário está em st.session_state.user_input, 
    # pois o widget tem a 'key="user_input"'
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

# Inicializa o estado da sessão
init_session_state()

st.set_page_config(
    page_title="Desafio de Matemática com Streamlit",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🧠 Desafio da Matemática com Streamlit")

# Área de Entrada do Nome do Usuário
# Esta seção só aparece se o nome ainda não foi definido
if not st.session_state.name:
    st.header("Seja Bem-Vindo(a)!")
    
    with st.form(key='name_form'):
        name_input = st.text_input("Qual é o seu nome?", key="input_name_widget")
        submit_button = st.form_submit_button("Começar Desafio")
        
        if submit_button and name_input:
            st.session_state.name = name_input.title().strip()
            st.session_state.game_started = True
            st.success(f"Olá, {st.session_state.name}! Preparado(a) para o Desafio?")
            generate_new_question()
        elif submit_button and not name_input:
            st.warning("Por favor, digite seu nome para começar.")

# --- Lógica do Jogo ---

elif st.session_state.game_started and st.session_state.score < 10:
    # Jogo em andamento

    st.markdown(f"### Olá, **{st.session_state.name}**!")
    st.info("O objetivo é acertar **10 questões** seguidas. Se errar, o desafio termina e você terá que começar novamente!")
    
    # Exibe a pontuação e o nível de dificuldade
    col1, col2 = st.columns(2)
    col1.metric("Pontuação Atual", st.session_state.score)
    col2.metric("Nível de Dificuldade (Máx)", st.session_state.level_max_value)
    
    st.markdown("---")
    
    # Exibe a Pergunta
    if st.session_state.question:
        question_text, _ = st.session_state.question
        st.header(f"Questão {st.session_state.score + 1}:")
        st.markdown(f"## Qual é o resultado de: **{question_text}**?")
        
        # Formulário para a resposta (para melhor controle do estado)
        with st.form(key='quiz_form'):
            answer_input = st.number_input(
                "Sua Resposta:", 
                min_value=0, 
                step=1, 
                key="user_input", 
                help="Digite sua resposta e clique em 'Enviar'."
            )
            submit_answer = st.form_submit_button("Enviar Resposta", on_click=check_answer)
            

# --- Fim de Jogo (Vitória ou Derrota) ---

elif st.session_state.score == 10:
    # Vitória
    st.balloons()
    st.success(f"## 🏆 VITÓRIA! Parabéns, {st.session_state.name}!")
    st.markdown("Você acertou **10 questões seguidas** e completou o Desafio de Matemática!")
    
    if st.button("Tentar Novamente (Recomeçar)"):
        reset_game()

elif st.session_state.name and st.session_state.last_attempt_correct == False:
    # Derrota
    st.error(f"## ❌ Fim de Jogo, {st.session_state.name}.")
    st.markdown(f"Você errou a última questão. Sua pontuação final foi de **{st.session_state.score} acertos**.")
    st.markdown("Mas não desanime! Que tal tentar novamente para completar o desafio?")
    
    if st.button("Tentar Novamente (Recomeçar)"):
        reset_game()

elif st.session_state.name and not st.session_state.game_started:
    # Tela de espera após digitar o nome, antes de iniciar o jogo ou após um erro (com nome preenchido)
    st.markdown(f"### Olá, **{st.session_state.name}**!")
    st.info("Clique abaixo para começar a primeira questão.")
    if st.button("Iniciar Desafio de Matemática"):
        st.session_state.game_started = True
        reset_game() # Começa o jogo no nível 1
