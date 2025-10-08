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
        # Se ocorrer qualquer erro (divisão por zero, etc.), tente novamente
        return generate_new_question()


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
                st.success(f"Excelente, **{st.session_state.name}**! Resposta correta!")
                st.session_state.user_input = 0 
                time.sleep(0.5) 
                generate_new_question()
            else:
                pass # Vai para a tela de vitória
            
        else:
            st.error(f"Resposta incorreta, **{st.session_state.name}** 😔. A resposta correta era **{correct_answer}**.")
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
        # Fim de jogo por tempo esgotado
        st.error(f"⏰ **TEMPO ESGOTADO!** **{st.session_state.name}**, você não conseguiu responder a tempo.")
        st.session_state.last_attempt_correct = False
        st.session_state.game_started = False
        st.rerun() # Força a ir para a tela de derrota
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

st.set_page_config(
    page_title="DESAFIO DA MATEMÁTICA",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Título Principal com Estilo Aprimorado
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #1E90FF; /* Azul forte */
            text-shadow: 3px 3px 6px #000000; /* Sombra mais escura */
            font-size: 3em;
            margin-bottom: 0.5em;
            font-weight: 900;
        }
        .timer-box {
            background-color: #DC143C; /* Vermelho escuro */
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            font-weight: bold;
            color: white;
            font-size: 1.8em;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.5);
        }
    </style>
    <h1 class="main-title">DESAFIO DA MATEMÁTICA</h1>
    """, unsafe_allow_html=True)
st.markdown("---")

# Área de Entrada do Nome do Usuário
if not st.session_state.name:
    st.header("Modo de Dificuldade Extrema!")
    
    # Banner Principal com Gradiente e Cores Fortes (Aprimorado)
    st.markdown("""
    <div style='
        padding: 30px; 
        border-radius: 15px; 
        background: linear-gradient(135deg, #FF4B4B 0%, #FFD700 100%);
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 6px 6px 15px rgba(0,0,0,0.4);
        color: white;
        border: 2px solid white;
    '>
        <h2 style='color: white; margin: 0; text-shadow: 2px 2px 5px rgba(0,0,0,0.6); font-size: 2em;'>🧠 ULTIMATE CHALLENGE ATIVADO 🚀</h2>
        <p style='margin: 15px 0 0 0; font-size: 20px; font-weight: bold;'>
            Prove ser o Mestre da Ordem de Operações. Cada acerto dobra a dificuldade!
        </p>
    </div>
    """, unsafe_allow_html=True) 

    with st.form(key='name_form'):
        name_input = st.text_input("Qual é o seu nome, Gênio?", key="input_name_widget")
        submit_button = st.form_submit_button("Começar o ULTIMATE CHALLENGE")
        
        if submit_button and name_input:
            st.session_state.name = name_input.title().strip()
            st.success(f"Impressionante coragem, **{st.session_state.name}**! Preparado para a Ordem de Operações?")
            st.session_state.game_started = True
            
            reset_game() 
            # O Streamlit lida com a re-renderização após o form.
            
        elif submit_button and not name_input:
            st.warning("Por favor, digite seu nome para começar.")

# --- Lógica do Jogo ---

elif st.session_state.game_started and st.session_state.score < 10:
    # ----------------------------------------
    # CHAMADA PRINCIPAL DO TEMPORIZADOR
    start_timer()
    # ----------------------------------------
    
    st.markdown("---")
    
    # Novo Layout com Cronômetro, Score e Dificuldade
    col_timer, col_score, col_difficulty = st.columns([1.5, 1, 1])

    # 1. Cronômetro (Design Aprimorado)
    col_timer.markdown(f"<div class='timer-box'>⏰ {st.session_state.time_remaining}s</div>", unsafe_allow_html=True)
    
    # 2. Score
    col_score.markdown(f"<div style='background-color: #4CAF50; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; color: white; box-shadow: 2px 2px 5px rgba(0,0,0,0.5);'>SCORE: {st.session_state.score} 🥇</div>", unsafe_allow_html=True)
    
    # 3. Dificuldade
    col_difficulty.markdown(f"<div style='background-color: #FFA500; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; color: white; box-shadow: 2px 2px 5px rgba(0,0,0,0.5);'>DIFICULDADE: {min(st.session_state.level_max_value, 10000)} ⚙️</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    get_progress_bar(st.session_state.score)

    st.warning(f"**LEMBRE-SE:** Priorize os parênteses `()`. A dificuldade é extrema! Boa sorte, Mestre **{st.session_state.name}**.")
    
    st.markdown("---")
    st.markdown("<h4 style='text-align: center; color: #DC143C;'>🎯 O Desafio da Vez é...</h4>", unsafe_allow_html=True)
    
    if st.session_state.question:
        question_text, _ = st.session_state.question
        
        # Pergunta em Destaque (Design Aprimorado)
        st.markdown(f"""
        <div style='
            background-color: #F8F8FF; /* Ghost White */
            padding: 30px; 
            border-radius: 15px; 
            text-align: center; 
            border: 4px solid #1E90FF; /* Azul Destaque */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        '>
            <h1 style='margin: 0; font-size: 2.5em; color: #333333;'>**{question_text}** = ?</h1>
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
            
    # Mensagem de Citação Histórica Colorida (Design Aprimorado)
    st.markdown("---")
    st.markdown(f"""
    <div style='
        padding: 15px; 
        border-radius: 10px; 
        background-color: #E6E6FA; /* Lavander */
        color: #483D8B; /* Dark Slate Blue */
        font-weight: bold;
        text-align: center;
        font-style: italic;
        border-left: 5px solid #1E90FF;
    '>
        📜 CITAÇÃO: {st.session_state.current_tip}
    </div>
    """, unsafe_allow_html=True)

# --- Fim de Jogo (Vitória ou Derrota) ---

elif st.session_state.score == 10:
    st.balloons()
    st.success(f"## 🏆 CAMPEÃO INCONTESTÁVEL! **{st.session_state.name}**, você DOMINOU a Matemática!")
    st.markdown("Você acertou **10 questões seguidas** e venceu o Desafio ULTIMATE! Seu nome entra para a história.")
    
    if st.button("Tentar Novamente (Recomeçar Desafio)"):
        st.session_state.game_started = True
        reset_game()
        st.rerun()

elif st.session_state.name and st.session_state.last_attempt_correct == False:
    st.error(f"## 💔 Falha Crítica, **{st.session_state.name}**.")
    st.markdown(f"Você errou a última questão ou o **Tempo Esgotou**. Sua pontuação final foi de **{st.session_state.score} acertos**.")
    st.markdown("O desafio é real. A Ordem de Operações exige precisão sob pressão. Clique para tentar de novo e superar seu recorde!")
    
    if st.button("Tentar Novamente (Recomeçar Desafio)"):
        st.session_state.game_started = True
        reset_game()
        st.rerun()

elif st.session_state.name and not st.session_state.game_started:
    st.markdown("---")
    st.markdown(f"### Olá, **{st.session_state.name}**!")
    st.info("Você está no lobby. Quando estiver pronto, aperte o botão para receber a primeira questão com o temporizador ativado.")
    if st.button("Iniciar Desafio da Matemática"):
        st.session_state.game_started = True
        reset_game()
        st.rerun()
