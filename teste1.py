import streamlit as st
import random
import operator
import math 
import time

# Mapeamento de operadores para facilitar o cálculo
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

# --- Lista de Frases de Dicas/Motivação (Nova Adição) ---
MOTIVATIONAL_TIPS = [
    "Dica: Multiplicação e Divisão vêm antes de Soma e Subtração! 📐",
    "Não confie na calculadora! Confie no seu cérebro. 🧠",
    "Lembre-se: Tudo dentro dos parênteses tem prioridade máxima. 😉",
    "A Dificuldade é Exponencial! Foco total nos números grandes. 🚀",
    "Matemática é paciência. Não tenha pressa! ⏳",
    "Um pequeno erro faz toda a diferença. Revise seu cálculo. ✔️",
    "Se você chegou até aqui, você já é um gênio! Prossiga. ✨",
]

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
        st.session_state.level_max_value = 10 
    if 'user_input' not in st.session_state:
        st.session_state.user_input = 0
    # Novo estado para armazenar a dica atual
    if 'current_tip' not in st.session_state:
        st.session_state.current_tip = random.choice(MOTIVATIONAL_TIPS)

def reset_game():
    """Reinicia a pontuação e a dificuldade do jogo, e gera a primeira questão."""
    st.session_state.score = 0
    st.session_state.level_max_value = 10
    st.session_state.last_attempt_correct = None
    st.session_state.user_input = 0 
    # Gera a primeira questão e uma nova dica
    st.session_state.current_tip = random.choice(MOTIVATIONAL_TIPS)
    generate_new_question()

def generate_new_question():
    """Gera uma nova questão com regras de precedência e parênteses."""
    
    score = st.session_state.score
    
    st.session_state.level_max_value = int(10 * (4.0 ** score))
    
    max_val = st.session_state.level_max_value
    limit = min(max_val, 10000)
    
    available_ops = ['+', '+'] 
    if score >= 3:
        available_ops.append('-') 
    if score >= 5:
        available_ops.append('*') 
    if score >= 7:
        available_ops.append('/') 
    
    
    if score >= 6:
        op1 = random.choice(available_ops)
        op2 = random.choice([op for op in available_ops if op != '/'])
        
        num1 = random.randint(10, limit)
        num2 = random.randint(1, limit)
        num3 = random.randint(1, int(limit / 10)) 
        
        if op1 == '-':
            if num1 < num2: num1, num2 = num2, num1
            result_part_1 = ops[op1](num1, num2)
            
        elif op1 == '/':
            divisor = random.choice([n for n in range(2, int(math.sqrt(limit)) + 1) if num1 % n == 0])
            num2 = divisor
            result_part_1 = int(ops[op1](num1, num2))
            
        else: # '+' ou '*'
            result_part_1 = ops[op1](num1, num2)

        question_text = f"({num1} {op1} {num2}) {op2} {num3}"
        
        if op2 == '+':
            answer = result_part_1 + num3
        elif op2 == '-':
            answer = result_part_1 - num3
        else: # op2 == '*'
            answer = result_part_1 * num3
            
        if abs(answer) > 1000000:
            return generate_new_question() 
            
    else:
        op1 = random.choice(available_ops)
        
        num1 = random.randint(1, limit)
        num2 = random.randint(1, limit)
        
        if op1 == '-':
            if num1 < num2: num1, num2 = num2, num1
            answer = ops[op1](num1, num2)
            
        elif op1 == '/':
            divisor = random.choice([n for n in range(2, int(math.sqrt(limit)) + 1) if limit % n == 0])
            num2 = divisor
            num1 = random.randint(1, int(limit / divisor)) * divisor
            answer = int(ops[op1](num1, num2))
            
        else: # '+' ou '*'
            answer = ops[op1](num1, num2)
        
        question_text = f"{num1} {op1} {num2}"

    st.session_state.question = (question_text, answer)
    
    # NOVO: Sorteia uma nova dica para a próxima tela
    st.session_state.current_tip = random.choice(MOTIVATIONAL_TIPS)


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
            
            st.balloons()
            
            if st.session_state.score < 10:
                st.success(f"Excelente, {st.session_state.name}! Resposta correta!")
                
                st.session_state.user_input = 0 
                
                time.sleep(0.5) 
                generate_new_question() # Esta função gera a nova pergunta e a nova dica
                
            else:
                pass 
            
        else:
            st.error(f"Resposta incorreta, {st.session_state.name} 😔. A resposta correta era **{correct_answer}**.")
            st.session_state.last_attempt_correct = False
            st.session_state.game_started = False 
            
    except ValueError:
        st.warning("Por favor, digite apenas um número inteiro.")


def get_progress_bar(score):
    """Cria uma barra de progresso visual baseada na pontuação."""
    total_goals = 10
    
    if score >= 7:
        level_emoji = "🔥"
    elif score >= 4:
        level_emoji = "🧠"
    else:
        level_emoji = "💡"
    
    filled_emojis = "✅" * score
    empty_emojis = "⬜" * (total_goals - score)
    
    st.markdown(f"**Progresso até o Título:** {level_emoji} {filled_emojis}{empty_emojis}")
    st.progress(score / total_goals)


# --- Layout do Aplicativo Streamlit ---

init_session_state()

st.set_page_config(
    page_title="DESAFIO DA MATEMÁTICA",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("DESAFIO DA MATEMÁTICA")

# Área de Entrada do Nome do Usuário
if not st.session_state.name:
    st.markdown("---")
    st.header("Modo de Dificuldade Extrema!")
    
    # BLOCO DE DECORAÇÃO 
    st.markdown("""
    <div style='
        padding: 15px; 
        border-radius: 10px; 
        border: 3px solid #FF4B4B; 
        background-color: #f0f2f6; 
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    '>
        <h3 style='color: #FF4B4B; margin: 0;'>🧠 ULTIMATE CHALLENGE ATIVADO 🚀</h3>
        <p style='margin: 8px 0 0 0; font-size: 16px; font-weight: bold;'>
            Conquiste 10 acertos consecutivos para provar seu valor.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form(key='name_form'):
        name_input = st.text_input("Qual é o seu nome, Gênio?", key="input_name_widget")
        submit_button = st.form_submit_button("Começar o ULTIMATE CHALLENGE")
        
        if submit_button and name_input:
            st.session_state.name = name_input.title().strip()
            st.session_state.game_started = True
            st.success(f"Impressionante coragem, {st.session_state.name}! Preparado para a Ordem de Operações?")
            
            reset_game() 
            
        elif submit_button and not name_input:
            st.warning("Por favor, digite seu nome para começar.")

# --- Lógica do Jogo ---

elif st.session_state.game_started and st.session_state.score < 10:
    # Jogo em andamento

    st.markdown("---")
    st.markdown(f"### Mãos à obra, **{st.session_state.name}**! 🔢")
    
    get_progress_bar(st.session_state.score)
    
    st.warning("**LEMBRE-SE:** Priorize as operações dentro dos parênteses `()`. A dificuldade é exponencial!")
    
    col1, col2 = st.columns(2)
    col1.metric("Pontuação Atual", st.session_state.score)
    col2.metric("Dificuldade (Máx. Valor)", min(st.session_state.level_max_value, 10000))
    
    st.markdown("---")
    st.markdown("<h4 style='color: #808080;'>O Desafio da Vez é...</h4>", unsafe_allow_html=True)
    
    if st.session_state.question:
        question_text, _ = st.session_state.question
        st.header(f"Questão {st.session_state.score + 1}:")
        st.markdown(f"## **{question_text}** = ?")
        
        st.markdown("---")
        
        with st.form(key='quiz_form'):
            answer_input = st.number_input(
                "Sua Resposta (Inteiro):", 
                min_value=-99999999, 
                step=1, 
                key="user_input", 
                value=st.session_state.user_input, 
                help="Digite sua resposta e clique em 'Enviar'."
            )
            submit_answer = st.form_submit_button("Enviar Resposta", on_click=check_answer)
            
    # --- NOVO: Mensagem de Dica Aleatória na Parte de Baixo ---
    st.markdown("---")
    st.caption(f"**Dica Secreta:** {st.session_state.current_tip}")
    # -----------------------------------------------------------

# --- Fim de Jogo (Vitória ou Derrota) ---

elif st.session_state.score == 10:
    st.balloons()
    st.success(f"## 🏆 CAMPEÃO INCONTESTÁVEL! {st.session_state.name}, você DOMINOU a Matemática!")
    st.markdown("Você acertou **10 questões seguidas** e venceu o Desafio ULTIMATE!")
    
    if st.button("Tentar Novamente (Recomeçar)"):
        reset_game()

elif st.session_state.name and st.session_state.last_attempt_correct == False:
    st.error(f"## 💔 Falha Crítica, {st.session_state.name}.")
    st.markdown(f"Você errou a última questão. Sua pontuação final foi de **{st.session_state.score} acertos**.")
    st.markdown("A dificuldade com parênteses e números gigantes é extrema! Clique para tentar de novo.")
    
    if st.button("Tentar Novamente (Recomeçar)"):
        reset_game()

elif st.session_state.name and not st.session_state.game_started:
    st.markdown("---")
    st.markdown(f"### Olá, **{st.session_state.name}**!")
    st.info("Clique abaixo para começar a provar seu valor.")
    if st.button("Iniciar Desafio da Matemática"):
        st.session_state.game_started = True
        reset_game()
    
