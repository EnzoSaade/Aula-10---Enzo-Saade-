import streamlit as st
import random
import operator
import math 
# import time # REMOVIDO: time.sleep(0.5) removido, então time não é mais estritamente necessário

# Mapeamento de operadores para facilitar o cálculo
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

# --- Lista de Frases de Matemáticos Históricos (AGORA COM MAIS OPÇÕES) ---
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
    "“Se soubesse que o mundo acabaria amanhã, eu, hoje, plantaria uma macieira.” — Martinho Lutero (Citação popularmente associada ao conceito de certeza e esperança na ciência)",
    "“Tudo é número.” — Pitágoras",
    "“A ciência começa na Matemática.” — James Clerk Maxwell",
]

# --- Funções de Ajuda e Variáveis de Estado ---

def get_random_quote():
    """Retorna uma citação aleatória, evitando repetição da última usada."""
    
    # 1. Obtém o índice da última citação usada
    last_index = st.session_state.get('last_quote_index', -1)
    
    # 2. Cria uma lista de índices que podem ser escolhidos (todos, exceto o último)
    available_indices = [i for i in range(len(HISTORICAL_MATH_QUOTES)) if i != last_index]
    
    # 3. Se houver índices disponíveis, escolhe um novo
    if available_indices:
        new_index = random.choice(available_indices)
    else:
        # Se for a primeira vez ou se só houver uma citação, escolhe qualquer uma
        new_index = random.randint(0, len(HISTORICAL_MATH_QUOTES) - 1)
    
    # 4. Salva o novo índice no estado da sessão
    st.session_state.last_quote_index = new_index
    
    # 5. Retorna a citação correspondente
    return HISTORICAL_MATH_QUOTES[new_index]


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
    # Nova variável para rastrear a última citação
    if 'last_quote_index' not in st.session_state:
        st.session_state.last_quote_index = -1
    
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
    """
    Gera uma nova questão com regras de precedência e parênteses.
    A dificuldade e os operadores disponíveis são baseados no score.
    A lógica de geração de divisão foi melhorada para robustez.
    """
    
    score = st.session_state.score
    
    # Lógica de dificuldade
    st.session_state.level_max_value = int(10 * (4.0 ** score))
    max_val = st.session_state.level_max_value
    limit = min(max_val, 10000)
    
    # Lógica de operadores disponíveis
    available_ops = ['+', '+'] 
    if score >= 3:
        available_ops.append('-') 
    if score >= 5:
        available_ops.append('*') 
    if score >= 7:
        available_ops.append('/') 
    
    
    if score >= 6:
        # Operações com parênteses (3 termos: (N1 op1 N2) op2 N3)
        op1 = random.choice(available_ops)
        # op2 não pode ser divisão para garantir resultado final inteiro e evitar float/int
        op2 = random.choice([op for op in available_ops if op != '/']) 
        
        # Tenta gerar números até 5 vezes para garantir que a divisão seja exata
        # e que os números não sejam absurdamente grandes.
        try_count = 0
        while try_count < 5: 
            try_count += 1
            
            num1 = random.randint(10, limit)
            num2 = random.randint(1, limit)
            # Garante num3 >= 1, mesmo para limites muito baixos (para evitar erro de divisão por zero na lógica 'or 1')
            num3 = random.randint(1, int(limit / 10) or 1) 
            
            result_part_1 = None
            
            if op1 == '-':
                if num1 < num2: num1, num2 = num2, num1
                result_part_1 = ops[op1](num1, num2)
                
            elif op1 == '/':
                # Geração mais robusta para (N1 / N2)
                if num2 == 0: continue
                
                # Escolhe um divisor seguro (num2)
                temp_num2 = random.randint(2, min(int(math.sqrt(limit)) + 1, 100) or 2)
                
                # Garante que num1 seja um múltiplo do divisor
                if num1 % temp_num2 != 0:
                    num1 = (num1 // temp_num2) * temp_num2
                
                # Verifica se num1 ainda é válido
                if num1 == 0 or num1 > limit: continue
                num2 = temp_num2
                result_part_1 = int(ops[op1](num1, num2))
                
            else: # '+' ou '*'
                result_part_1 = ops[op1](num1, num2)

            # Garante que a primeira parte é um inteiro antes de calcular o resultado final
            result_part_1 = int(result_part_1) 
            
            # Calcula a resposta final
            if op2 == '+':
                answer = result_part_1 + num3
            elif op2 == '-':
                answer = result_part_1 - num3
            else: # op2 == '*'
                answer = result_part_1 * num3
                
            # Evita números absurdamente grandes
            if abs(answer) <= 1000000:
                question_text = f"({num1} {op1} {num2}) {op2} {num3}"
                st.session_state.question = (question_text, answer)
                st.session_state.current_tip = get_random_quote()
                return # Questão gerada com sucesso

        # Se falhar após 5 tentativas, tenta novamente (recursão segura)
        return generate_new_question()

    else:
        # Operações de 2 termos
        op1 = random.choice(available_ops)
        
        # Tratamento especial para Divisão
        if op1 == '/':
            # Garantir divisão exata e num1 < limit
            
            # Escolhe o quociente (resposta) e divisor (num2)
            # Limite o quociente para que num1 não exceda 'limit' facilmente
            answer = random.randint(1, limit // 2 if limit > 1 else 1)
            num2 = random.randint(2, min(100, limit) or 2) # Divisor seguro
            num1 = answer * num2
            
            if num1 > limit: # Se o dividendo exceder o limite, recalcula
                return generate_new_question()
                
            answer = int(ops[op1](num1, num2))

        elif op1 == '-':
            num1 = random.randint(1, limit)
            num2 = random.randint(1, limit)
            if num1 < num2: num1, num2 = num2, num1
            answer = ops[op1](num1, num2)
            
        else: # '+' ou '*'
            num1 = random.randint(1, limit)
            num2 = random.randint(1, limit)
            answer = ops[op1](num1, num2)
            
        question_text = f"{num1} {op1} {num2}"

    st.session_state.question = (question_text, int(answer)) # Garante que a resposta seja INT
    
    st.session_state.current_tip = get_random_quote()


def check_answer():
    """Verifica a resposta do usuário. CORREÇÃO: Removido time.sleep e ajustada a lógica de vitória."""
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
            
            # Lógica corrigida: Se score < 10, gera próxima pergunta. Se score == 10, vai para o bloco de vitória no layout.
            if st.session_state.score < 10:
                st.success(f"Excelente, {st.session_state.name}! Resposta correta!")
                
                st.session_state.user_input = 0 
                
                # time.sleep(0.5) REMOVIDO: Evita problemas de re-renderização do Streamlit.
                
                generate_new_question()
            else:
                # Caso de vitória (score == 10). Permite que o Streamlit redesenhe para o bloco de vitória.
                st.session_state.user_input = 0
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
    # Jogo em andamento

    st.markdown("---")
    st.markdown(f"### Mãos à obra, **{st.session_state.name}**! 🔢")
    
    get_progress_bar(st.session_state.score)
    
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
