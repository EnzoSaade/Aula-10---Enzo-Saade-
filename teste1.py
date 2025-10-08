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
    # NOVO: A chave do input é usada para controlar o valor inicial (limpeza)
    if 'user_input' not in st.session_state:
        st.session_state.user_input = 0

def reset_game():
    """Reinicia a pontuação e a dificuldade do jogo."""
    st.session_state.score = 0
    st.session_state.level_max_value = 10
    st.session_state.last_attempt_correct = None
    st.session_state.user_input = 0 # Limpa o campo na reinicialização
    generate_new_question()

def generate_new_question():
    """Gera uma nova questão com regras de precedência e parênteses."""
    
    score = st.session_state.score
    
    # 1. Aumento EXTREMO da Dificuldade (base 4.0!)
    st.session_state.level_max_value = int(10 * (4.0 ** score))
    
    max_val = st.session_state.level_max_value
    
    # Define os limites para os números: mínimo 1, máximo 10000 
    limit = min(max_val, 10000)
    
    # Define as operações disponíveis
    available_ops = ['+', '+'] 
    if score >= 3:
        available_ops.append('-') 
    if score >= 5:
        available_ops.append('*') 
    if score >= 7:
        available_ops.append('/') 
    
    
    # Lógica para a questão de 3 termos com PARÊNTESES (Ultimate Test)
    if score >= 6:
        op1 = random.choice(available_ops)
        op2 = random.choice([op for op in available_ops if op != '/'])
        
        # Gera os números
        num1 = random.randint(10, limit)
        num2 = random.randint(1, limit)
        num3 = random.randint(1, int(limit / 10)) 
        
        # 1. Garante que (num1 op1 num2) seja um resultado limpo e positivo (para simplificar)
        if op1 == '-':
            if num1 < num2: num1, num2 = num2, num1
            result_part_1 = ops[op1](num1, num2)
            
        elif op1 == '/':
            # Garante Divisão com resultado INTEIRO e positivo
            divisor = random.choice([n for n in range(2, int(math.sqrt(limit)) + 1) if num1 % n == 0])
            num2 = divisor
            result_part_1 = int(ops[op1](num1, num2))
            
        else: # '+' ou '*'
            result_part_1 = ops[op1](num1, num2)

        # 2. Monta a questão com parênteses, forçando a ordem
        question_text = f"({num1} {op1} {num2}) {op2} {num3}"
        
        # 3. Calcula o resultado final (o eval garante o cálculo de fora dos parênteses)
        if op2 == '+':
            answer = result_part_1 + num3
        elif op2 == '-':
            answer = result_part_1 - num3
        else: # op2 == '*'
            answer = result_part_1 * num3
            
        # Filtro de segurança
        if abs(answer) > 1000000:
            return generate_new_question() 
            
    else:
        # Lógica de duas variáveis (Níveis 1-5) - Já é bem difícil por causa do fator 4.0x
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
    
    # Forçando o re-run
    st.rerun()


def check_answer():
    """Verifica a resposta do usuário."""
    # O valor digitado pelo usuário é lido de st.session_state.user_input
    user_input = st.session_state.user_input
    
    if st.session_state.question is None:
        return

    _, correct_answer = st.session_state.question

    try:
        user_answer_num = int(user_input)
        
        if user_answer_num == correct_answer:
            st.session_state.score += 1
            st.session_state.last_attempt_correct = True
            
            # EFEITOS ESPECIAIS AO ACERTAR
            st.balloons()
            st.snow()
            
            if st.session_state.score < 10:
                st.success(f"Excelente, {st.session_state.name}! Resposta correta!")
                
                # CORREÇÃO DA LIMPEZA: Define o valor da CHAVE de volta para 0
                # O st.rerun() redesenhará o campo com este valor.
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


# --- Layout do Aplicativo Streamlit ---

init_session_state()

# TÍTULO SIMPLES
st.set_page_config(
    page_title="desafio da matemática",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# TÍTULO SIMPLES
st.title("desafio da matemática")
st.markdown("---")

# Área de Entrada do Nome do Usuário
if not st.session_state.name:
    st.header("Modo de Dificuldade Extrema!")
    
    with st.form(key='name_form'):
        name_input = st.text_input("Qual é o seu nome, Gênio?", key="input_name_widget")
        submit_button = st.form_submit_button("Começar o ULTIMATE CHALLENGE V2")
        
        if submit_button and name_input:
            st.session_state.name = name_input.title().strip()
            st.session_state.game_started = True
            st.success(f"Impressionante coragem, {st.session_state.name}! Preparado para a Ordem de Operações?")
            generate_new_question()
        elif submit_button and not name_input:
            st.warning("Por favor, digite seu nome para começar.")

# --- Lógica do Jogo ---

elif st.session_state.game_started and st.session_state.score < 10:
    # Jogo em andamento

    st.markdown(f"### Mãos à obra, **{st.session_state.name}**!")
    st.warning("**LEMBRE-SE:** Priorize as operações dentro dos parênteses `()`. A dificuldade é exponencial!")
    
    # Exibe a pontuação e o nível de dificuldade
    col1, col2 = st.columns(2)
    col1.metric("Pontuação Atual", st.session_state.score)
    col2.metric("Dificuldade (Máx. Valor)", min(st.session_state.level_max_value, 10000))
    
    st.markdown("---")
    
    # Exibe a Pergunta
    if st.session_state.question:
        question_text, _ = st.session_state.question
        st.header(f"Questão {st.session_state.score + 1}:")
        st.markdown(f"## **{question_text}** = ?")
        
        # Formulário para a resposta
        with st.form(key='quiz_form'):
            # CORREÇÃO DA LIMPEZA APLICADA AQUI
            answer_input = st.number_input(
                "Sua Resposta (Inteiro):", 
                min_value=-99999999, 
                step=1, 
                key="user_input", # A chave armazena o valor submetido
                value=st.session_state.user_input, # O valor inicial é pego da CHAVE
                help="Digite sua resposta e clique em 'Enviar'."
            )
            submit_answer = st.form_submit_button("Enviar Resposta", on_click=check_answer)
            

# --- Fim de Jogo (Vitória ou Derrota) ---

elif st.session_state.score == 10:
    # Vitória
    st.balloons()
    st.snow()
    st.success(f"## 🏆 CAMPEÃO INCONTESTÁVEL! {st.session_state.name}, você DOMINOU a Matemática!")
    st.markdown("Você acertou **10 questões seguidas** e venceu o Desafio ULTIMATE V2!")
    
    if st.button("Tentar Novamente (Recomeçar)"):
        reset_game()

elif st.session_state.name and st.session_state.last_attempt_correct == False:
    # Derrota
    st.error(f"## 💔 Falha Crítica, {st.session_state.name}.")
    st.markdown(f"Você errou a última questão. Sua pontuação final foi de **{st.session_state.score} acertos**.")
    st.markdown("A dificuldade com parênteses e números gigantes é extrema! Clique para tentar de novo.")
    
    if st.button("Tentar Novamente (Recomeçar)"):
        reset_game()

elif st.session_state.name and not st.session_state.game_started:
    # Tela de espera
    st.markdown(f"### Olá, **{st.session_state.name}**!")
    st.info("Clique abaixo para começar a provar seu valor.")
    if st.button("Iniciar Desafio de Matemática"):
        st.session_state.game_started = True
        reset_game()
