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
    "“Deus fez os números inteiros, todo o resto é obra do homem.” — Leopold Kronecker",
    "“Existe geometria em todo o resplendor. Existe música em todas as esferas.” — Pitágoras",
    "“Sem a paixão, não há gênio.” — Theodor Svedberg",
    "“A ciência mais digna de ser estudada é a Matemática.” — Roger Bacon",
    "“Se soubesse que o mundo acabaria amanhã, eu, hoje, plantaria uma macieira.” — Martinho Lutero",
    "“Tudo é número.” — Pitágoras",
    "“A ciência começa na Matemática.” — James Clerk Maxwell",
]

# --- Funções de Ajuda e Variáveis de Estado ---

def get_random_quote():
    """Retorna uma citação aleatória, evitando repetição da última usada."""
    last_index = st.session_state.get('last_quote_index', -1)
    available_indices = [i for i in range(len(HISTORICAL_MATH_QUOTES)) if i != last_index]
    
    if available_indices:
        new_index = random.choice(available_indices)
    else:
        new_index = random.randint(0, len(HISTORICAL_MATH_QUOTES) - 1)
    
    st.session_state.last_quote_index = new_index
    return HISTORICAL_MATH_QUOTES[new_index]

def init_session_state():
    """Inicializa as variáveis de estado da sessão."""
    if 'name' not in st.session_state: st.session_state.name = ""
    if 'score' not in st.session_state: st.session_state.score = 0
    if 'game_started' not in st.session_state: st.session_state.game_started = False
    if 'last_attempt_correct' not in st.session_state: st.session_state.last_attempt_correct = None
    if 'question' not in st.session_state: st.session_state.question = None
    if 'level_max_value' not in st.session_state: st.session_state.level_max_value = 10 
    if 'user_input' not in st.session_state: st.session_state.user_input = 0
    if 'last_quote_index' not in st.session_state: st.session_state.last_quote_index = -1
    
    # VARIÁVEIS PARA O TEMPORIZADOR
    if 'time_limit' not in st.session_state: st.session_state.time_limit = 30 # Segundos por questão
    if 'time_remaining' not in st.session_state: st.session_state.time_remaining = 30
    if 'question_start_time' not in st.session_state: st.session_state.question_start_time = time.time()
    
    if 'current_tip' not in st.session_state: st.session_state.current_tip = "Prepare-se para o desafio!" 

def reset_game():
    """Reinicia a pontuação, a dificuldade e o temporizador."""
    st.session_state.score = 0
    st.session_state.level_max_value = 10
    st.session_state.last_attempt_correct = None
    st.session_state.user_input = 0 
    
    st.session_state.current_tip = get_random_quote()
    
    # RESET DO TEMPORIZADOR
    st.session_state.time_remaining = st.session_state.time_limit
    st.session_state.question_start_time = time.time()
    
    generate_new_question()

def generate_new_question():
    """Gera uma nova questão e reinicia o temporizador para esta questão."""
    
    score = st.session_state.score
    
    # Lógica de Dificuldade
    st.session_state.level_max_value = int(10 * (4.0 ** score))
    max_val = st.session_state.level_max_value
    limit = min(max_val, 10000)
    
    available_ops = ['+', '+'] 
    if score >= 3: available_ops.append('-') 
    if score >= 5: available_ops.append('*') 
    if score >= 7: available_ops.append('/') 
    
    # Tenta gerar a questão (segurança contra erros de cálculo)
    try:
        if score >= 6:
            # Questões com parênteses e duas operações
            op1 = random.choice(available_ops)
            op2 = random.choice([op for op in available_ops if op != '/'])
            
            num1 = random.randint(10, limit)
            num2 = random.randint(1, limit)
            num3 = random.randint(1, int(limit / 10)) 
            
            if op1 == '-':
                if num1 < num2: num1, num2 = num2, num1
                result_part_1 = ops[op1](num1, num2)
            elif op1 == '/':
                # Garante que num1 seja divisível por um divisor razoável
                divisor = random.choice([n for n in range(2, int(math.sqrt(limit)) + 1) if num1 % n == 0] or [2])
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
            # Questões simples (uma operação)
            op1 = random.choice(available_ops)
            
            num1 = random.randint(1, limit)
            num2 = random.randint(1, limit)
            
            if op1 == '-':
                if num1 < num2: num1, num2 = num2, num1
                answer = ops[op1](num1, num2)
                
            elif op1 == '/':
                divisor = random.choice([n for n in range(2, int(math.sqrt(limit)) + 1) if limit % n == 0] or [2])
                num2 = divisor
                num1 = random.randint(1, int(limit / divisor)) * divisor
                answer = int(ops[op1](num1, num2))
                
            else: # '+' ou '*'
                answer = ops[op1](num1, num2)
            
            question_text = f"{num1} {op1} {num2}"

        st.session_state.question = (question_text, int(answer))
        
        st.session_state.current_tip = get_random_quote()
        
        # REINICIA O TEMPORIZADOR A CADA NOVA QUESTÃO
        st.session_state.time_remaining = st.session_state.time_limit
        st.session_state.question_start_time = time.time()
        
    except Exception:
        # Se ocorrer qualquer erro, tente novamente
        return generate_new_question()


def check_answer():
    """Verifica a resposta do usuário. Chamada pelo botão de submissão."""
    
    if st.session_state.question is None: 
        return
        
    # Garante que o tempo restante seja calculado antes da verificação
    elapsed_time = time.time() - st.session_state.question_start_time
    st.session_state.time_remaining = st.session_state.
    
