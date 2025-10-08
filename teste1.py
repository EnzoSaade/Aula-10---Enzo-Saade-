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

# --- Lista de Frases de Matemáticos Históricos ---
HISTORICAL_MATH_QUOTES = [
    "“A Matemática é o alfabeto com o qual Deus escreveu o universo.” — Galileu Galilei",
    "“Onde há matéria, há geometria.” — Johannes Kepler",
    "“Não se preocupe com suas dificuldades em Matemática. Posso garantir que as minhas são maiores.” — Albert Einstein",
    "“Os números governam o universo.” — Pitágoras",
    "“A essência da Matemática reside em sua liberdade.” — Georg Cantor",
    "“A Matemática é a rainha das ciências e a Aritmética é a rainha da Matemática.” — Carl Friedrich Gauss",
    "“Na Matemática não há caminhos reais.” — Euclides",
    "“A imaginação é mais importante que o conhecimento.” — Albert Einstein",
]

# --- Funções de Ajuda e Variáveis de Estado ---

def get_random_quote():
    """Retorna uma citação aleatória da lista."""
    return random.choice(HISTORICAL_MATH_QUOTES)

def init_session_state():
    """Inicializa as variáveis de estado da sessão."""
    # Garante que todas as chaves essenciais existam
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
    
    # Inicializa a citação (Só executa uma vez na inicialização completa)
    if 'current_tip' not in st.session_state:
        st.session_state.current_tip = get_random_quote()

def reset_game():
    """Reinicia a pontuação e a dificuldade do jogo, e gera a primeira questão."""
    st.session_state.score = 0
    st.session_state.level_max_value = 10
    st.session_state.last_attempt_correct = None
    st.session_state.user_input = 0 
    st.session_state.current_tip = get_random_quote() # Novo quote
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
    
    st.session_state.current_tip = get_random_quote()


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
                generate_new_question()
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

# ----------------------------------------------------------------
# CHAVE: Garante que o estado seja inicializado antes de qualquer widget ou lógica principal
init_session_state()
# ----------------------------------------------------------------

st.set_page_config(
    page_title="DESAFIO DA MATEMÁTICA",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Título Colorido
st.markdown("<h1 style='text-align: center; color: #1E90FF; text-shadow: 2px 2px 4px #87CEEB;'>DESAFIO DA MATEMÁTICA</h1>", unsafe_allow_html=True)
st.markdown("---")

# Área de Entrada do Nome do Usuário
if not st.session_state.name:
    st.header("Modo de Dificuldade Extrema!")
    
    # Banner Principal com Gradiente e Cores Fortes
    st.markdown("""
    <div style='
        padding: 20px; 
        border-radius: 12px; 
        background: linear-
