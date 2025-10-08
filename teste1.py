import streamlit as st
import random
import operator
import math # Para a função sqrt (raiz quadrada)

# Mapeamento de operadores para facilitar o cálculo
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv, # Usaremos division, mas garantiremos que o resultado seja inteiro
}

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
    """Gera uma nova questão com regras de precedência."""
    
    score = st.session_state.score
    
    # 1. Aumento Ultra-Agressivo da Dificuldade (usando 2.5 como base)
    st.session_state.level_max_value = int(10 * (2.5 ** score))
    
    max_val = st.session_state.level_max_value
    
    # Define os limites para os números: mínimo 1, máximo 5000 (muito maior)
    limit = min(max_val, 5000)
    
    # Define as operações disponíveis
    available_ops = ['+', '+'] # Adição é mais comum no início
    if score >= 3:
        available_ops.append('-') # Subtração
    if score >= 5:
        available_ops.append('*') # Multiplicação
    if score >= 7:
        available_ops.append('/') # Divisão
    
    
    # Lógica para a questão de 3 termos (Ordem de Operações)
    if score >= 7:
        op1 = random.choice(available_ops)
        op2 = random.choice([op for op in available_ops if op != '/']) # Evita Divisão dupla complexa
        
        # Gera os números iniciais
        num1 = random.randint(10, limit)
        num2 = random.randint(1, limit)
        num3 = random.randint(1, int(limit / 10)) # Terceiro número menor
        
        # Se op1 ou op2 for '-', garante que o resultado não seja negativo na subtração
        if op1 == '-' and num1 < num2:
             num1, num2 = num2, num1
        
        # Lógica especial para garantir Divisão com resultado INTEIRO
        if '/' in [op1, op2]:
            # Simplificação: se houver divisão, garantimos que o divisor é um fator
            divisor = random.choice([n for n in range(2, 11) if limit % n == 0])
            
            if op1 == '/':
                # num1 será um múltiplo do divisor
                num2 = divisor 
                num1 = random.randint(1, int(limit / divisor)) * divisor
            elif op2 == '/':
                 # num2 será um múltiplo do divisor, num3 será o divisor
                num3 = divisor
                num2 = random.randint(1, int(limit / divisor)) * divisor

        question_text = f"{num1} {op1} {num2} {op2} {num3}"
        
        # O cálculo deve respeitar a ordem (PEMDAS/BODMAS)
        try:
            # Usando eval() com cautela para calcular a expressão, pois é a forma mais simples 
            # de aplicar a ordem de operações (Multiplicação/Divisão primeiro).
            # Como controlamos a entrada dos números e operadores, o risco é mínimo.
            answer = int(eval(question_text))
            
            # Filtro de segurança para evitar números absurdos
            if abs(answer) > 1000000:
                return generate_new_question() # Tenta gerar uma questão mais simples
            
        except ZeroDivisionError:
            # Em caso de divisão por zero (muito improvável, mas segurança), gera nova questão
            return generate_new_question()
            
    else:
        # Lógica de duas variáveis (Níveis 1-6)
        op1 = random.choice(available_ops)
        
        num1 = random.randint(1, limit)
        num2 = random.randint(1, limit)
        
        if op1 == '-':
            # Garante resultado não negativo para subtração simples
            if num1 < num2: num1, num2 = num2, num1
            answer = ops[op1](num1, num2)
            
        elif op1 == '/':
            # Garante Divisão com resultado INTEIRO
            divisor = random.choice([n for n in range(2, int(math.sqrt(limit)) + 1) if limit % n == 0])
            num2 = divisor
            num1 = random.randint(1, int(limit / divisor)) * divisor
            answer = int(ops[op1](num1, num2))
            
        else: # '+' ou '*'
            answer = ops[op1](num1, num2)
        
        question_text = f"{num1} {op1} {num2}"

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
                st.success(f"Excelente, {st.session_state.name}! Resposta correta!")
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
    page_title="Desafio de Matemática: ULTIMATE",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🔥 Desafio da Matemática: ULTIMATE CHALLENGE")
st.markdown("---")

# Área de Entrada do Nome do Usuário
if not st.session_state.name:
    st.header("Modo de Dificuldade Extrema!")
    
    with st.form(key='name_form'):
        name_input = st.text_input("Qual é o seu nome, Gênio?", key="input_name_widget")
        submit_button = st.form_submit_button("Começar o ULTIMATE CHALLENGE")
        
        if submit_button and name_input:
            st.session_state.name = name_input.title().strip()
            st.session_state.game_started = True
            st.success(f"Impressionante coragem, {st.session_state.name}! Siga as regras de precedência!")
            generate_new_question()
        elif submit_button and not name_input:
            st.warning("Por favor, digite seu nome para começar.")

# --- Lógica do Jogo ---

elif st.session_state.game_started and st.session_state.score < 10:
    # Jogo em andamento

    st.markdown(f"### Mãos à obra, **{st.session_state.name}**!")
    st.warning("**LEMBRE-SE:** Use a Ordem de Operações (Multiplicação/Divisão antes de Adição/Subtração).")
    
    # Exibe a pontuação e o nível de dificuldade
    col1, col2 = st.columns(2)
    col1.metric("Pontuação Atual", st.session_state.score)
    # Exibe o limite máximo do número na questão
    col2.metric("Nível de Dificuldade (Máx. Valor)", min(st.session_state.level_max_value, 5000))
    
    st.markdown("---")
    
    # Exibe a Pergunta
    if st.session_state.question:
        question_text, _ = st.session_state.question
        st.header(f"Questão {st.session_state.score + 1}:")
        st.markdown(f"## **{question_text}** = ?")
        
        # Formulário para a resposta
        with st.form(key='quiz_form'):
            answer_input = st.number_input(
                "Sua Resposta (Inteiro):", 
                min_value=-9999999, 
                step=1, 
                key="user_input", 
                help="Digite sua resposta e clique em 'Enviar'."
            )
            submit_answer = st.form_submit_button("Enviar Resposta", on_click=check_answer)
            

# --- Fim de Jogo (Vitória ou Derrota) ---

elif st.session_state.score == 10:
    # Vitória
    st.balloons()
    st.success(f"## 🚀 CONQUISTA ÉPICA! Você é um Mestre, {st.session_state.name}!")
    st.markdown("Você acertou **10 questões seguidas** e DOMINOU o Desafio ULTIMATE!")
    
    if st.button("Tentar Novamente (Recomeçar)"):
        reset_game()

elif st.session_state.name and st.session_state.last_attempt_correct == False:
    # Derrota
    st.error(f"## 💔 Falha Crítica, {st.session_state.name}.")
    st.markdown(f"Você errou a última questão. Sua pontuação final foi de **{st.session_state.score} acertos**.")
    st.markdown("As regras de precedência são traiçoeiras! Clique para tentar de novo e conquistar a vitória.")
    
    if st.button("Tentar Novamente (Recomeçar)"):
        reset_game()

elif st.session_state.name and not st.session_state.game_started:
    # Tela de espera
    st.markdown(f"### Olá, **{st.session_state.name}**!")
    st.info("Clique abaixo para começar a provar seu valor.")
    if st.button("Iniciar Desafio de Matemática"):
        st.session_state.game_started = True
        reset_game()
