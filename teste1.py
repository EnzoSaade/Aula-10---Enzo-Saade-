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

def calculate_bg_color(score):
    """Calcula a cor de fundo com base na pontuação (transição Azul -> Vermelho)."""
    # Escala de 0 a 10
    intensity = min(score / 10.0, 1.0) 
    
    # Azul (fácil, R=0, G=150, B=255) para Vermelho (difícil, R=255, G=0, B=0)
    # Aumenta o R e diminui G e B
    red = int(255 * intensity)
    green = int(150 * (1 - intensity))
    blue = int(255 * (1 - intensity))
    
    return f'rgb({red},{green},{blue})'

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
    if 'current_tip' not in st.session_state: st.session_state.current_tip = get_random_quote()
    
    # VARIÁVEIS PARA O TEMPORIZADOR
    if 'time_limit' not in st.session_state: st.session_state.time_limit = 30 # Segundos por questão
    if 'time_remaining' not in st.session_state: st.session_state.time_remaining = 30
    if 'question_start_time' not in st.session_state: st.session_state.question_start_time = time.time()

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
    
    st.session_state.level_max_value = int(10 * (4.0 ** score))
    
    max_val = st.session_state.level_max_value
    limit = min(max_val, 10000)
    
    available_ops = ['+', '+'] 
    if score >= 3: available_ops.append('-') 
    if score >= 5: available_ops.append('*') 
    if score >= 7: available_ops.append('/') 
    
    
    if score >= 6:
        op1 = random.choice(available_ops)
        op2 = random.choice([op for op in available_ops if op != '/'])
        
        num1 = random.randint(10, limit)
        num2 = random.randint(1, limit)
        num3 = random.randint(1, int(limit / 10)) 
        
        try:
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
        except:
            return generate_new_question() 

        if abs(answer) > 1000000:
            return generate_new_question() 
            
    else:
        op1 = random.choice(available_ops)
        
        num1 = random.randint(1, limit)
        num2 = random.randint(1, limit)
        
        try:
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
        except:
            return generate_new_question()

        question_text = f"{num1} {op1} {num2}"

    st.session_state.question = (question_text, answer)
    
    st.session_state.current_tip = get_random_quote()
    
    # REINICIA O TEMPORIZADOR A CADA NOVA QUESTÃO
    st.session_state.time_remaining = st.session_state.time_limit
    st.session_state.question_start_time = time.time()


def check_answer():
    """Verifica a resposta do usuário. Chamada pelo botão de submissão."""
    
    if st.session_state.question is None: 
        return
        
    # Garante que o tempo restante seja calculado antes da verificação
    elapsed_time = time.time() - st.session_state.question_start_time
    st.session_state.time_remaining = st.session_state.time_limit - math.floor(elapsed_time)

    if st.session_state.time_remaining <= 0:
        # Se o tempo acabou antes de submeter, trata como falha
        st.session_state.last_attempt_correct = False
        st.session_state.game_started = False 
        return
        
    user_input = st.session_state.user_input
    
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
                pass # Vai para a tela de vitória
            
        else:
            st.error(f"Resposta incorreta, {st.session_state.name} 😔. A resposta correta era **{correct_answer}**.")
            st.session_state.last_attempt_correct = False
            st.session_state.game_started = False 
            
    except ValueError:
        st.warning("Por favor, digite apenas um número inteiro.")


# A função principal do temporizador que força a atualização da página
def start_timer():
    if not st.session_state.game_started or st.session_state.score == 10:
        return

    # Calcula o tempo decorrido e o restante
    elapsed_time = time.time() - st.session_state.question_start_time
    time_left = st.session_state.time_limit - math.floor(elapsed_time)
    
    # Atualiza o estado da sessão
    st.session_state.time_remaining = time_left

    if time_left <= 0:
        # CORRIGIDO: Mensagem completa de f-string
        st.error(f"⏰ **TEMPO ESGOTADO!** {st.session_state.name}, você não conseguiu responder a tempo.")
        st.session_state.last_attempt_correct = False
        st.session_state.game_started = False
        st.rerun()
    else:
        # Se ainda há tempo, força a reexecução do script após 1 segundo
        time.sleep(1)
        st.rerun()


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

# INJEÇÃO DO CSS PARA A TRANSIÇÃO DE COR DE FUNDO
current_bg_color = calculate_bg_color(st.session_state.score)

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {current_bg_color};
        transition: background-color 1s ease; /* Transição suave */
    }}
    </style>
    """, unsafe_allow_html=True)


st.set_page_config(
    page_title="DESAFIO DA MATEMÁTICA",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Título Colorido
st.markdown("<h1 style='text-align: center; color: #FFFFFF; text-shadow: 2px 2px 4px #000000;'>DESAFIO DA MATEMÁTICA</h1>", unsafe_allow_html=True)
st.markdown("---")

# Área de Entrada do Nome do Usuário
if not st.session_state.name:
    st.header("Modo de Dificuldade Extrema!")
    
    # Banner Principal com Gradiente e Cores Fortes
    st.markdown("""
    <div style='
        padding: 20px; 
        border-radius: 12px; 
        background: linear-gradient(135deg, #FF4B4B 0%, #FFD700 100%);
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3);
        color: white;
    '>
        <h2 style='color: white; margin: 0; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);'>🧠 ULTIMATE CHALLENGE ATIVADO 🚀</h2>
        <p style='margin: 10px 0 0 0; font-size: 18px; font-weight: bold;'>
            Prove ser o Mestre da Ordem de Operações.
        </p>
    </div>
    """, unsafe_allow_html=True) 

    with st.form(key='name_form'):
        name_input = st.text_input("Qual é o seu nome, Gênio?", key="input_name_widget")
        submit_button = st.form_submit_button("Começar o ULTIMATE CHALLENGE")
        
        if submit_button and name_input:
            st.session_state.name = name_input.title().strip()
            st.success(f"Impressionante coragem, {st.session_state.name}! Preparado para a Ordem de Operações?")
            st.session_state.game_started = True
            
            reset_game() 
            
        elif submit_button and not name_input:
            st.warning("Por favor, digite seu nome para começar.")

# --- Lógica do Jogo ---

elif st.session_state.game_started and st.session_state.score < 10:
    # ----------------------------------------
    # CHAMADA PRINCIPAL DO TEMPORIZADOR
    start_timer()
    # ----------------------------------------

    st.markdown("---")
    st.markdown(f"### Mãos à obra, **{st.session_state.name}**! 🔢")
    
    get_progress_bar(st.session_state.score)
    
    # Exibe o cronômetro
    timer_placeholder = st.empty()
    timer_placeholder.markdown(f"<div style='background-color: #DC143C; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; color: white; font-size: 20px;'>⏰ TEMPO RESTANTE: {st.session_state.time_remaining} segundos</div>", unsafe_allow_html=True)

    
    st.warning("**LEMBRE-SE:** Priorize as operações dentro dos parênteses `()`. A dificuldade é exponencial!")
    
    # Métricas Destacadas
    col1, col2 = st.columns(2)
    col1.markdown(f"<div style='background-color: #E6E6FA; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold;'>SCORE: {st.session_state.score} 🥇</div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold;'>DIFICULDADE: {min(st.session_state.level_max_value, 10000)} ⚙️</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h4 style='text-align: center; color: #DC143C;'>🎯 O Desafio da Vez é...</h4>", unsafe_allow_html=True)
    
    if st.session_state.question:
        question_text, _ = st.session_state.question
        
        # Pergunta em Destaque (Fundo)
        st.markdown(f"""
        <div style='
            background-color: #FFFACD; 
            padding: 25px; 
            border-radius: 10px; 
            text-align: center; 
            border: 3px dashed #FFD700;
        '>
            <h1 style='margin: 0;'>**{question_text}** = ?</h1>
        </div>
        """, unsafe_allow_html=True) 

        
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
            
    # Mensagem de Citação Histórica Colorida
    st.markdown("---")
    st.markdown(f"""
    <div style='
        padding: 10px; 
        border-radius: 8px; 
        background-color: #F0F8FF; 
        color: #4682B4; 
        font-weight: bold;
        text-align: center;
        font-style: italic;
    '>
        📜 CITAÇÃO: {st.session_state.current_tip}
    </div>
    """, unsafe_allow_html=True)

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
    st.markdown("Clique para tentar de novo.")
    
    if st.button("Tentar Novamente (Recomeçar)"):
        reset_game()

elif st.session_state.name and not st.session_state.game_started:
    st.markdown("---")
    st.markdown(f"### Olá, **{st.session_state.name}**!")
    st.info("Clique abaixo para começar a provar seu valor.")
    if st.button("Iniciar Desafio da Matemática"):
        st.session_state.game_started = True
        reset_game()
