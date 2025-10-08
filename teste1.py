import streamlit as st
import random

def generate_question(level):
    """Gera uma pergunta de matemática com base no nível de dificuldade."""
    # Ajuste dos ranges para garantir que as perguntas se tornem progressivamente mais difíceis
    if level <= 2:  # Níveis 1 e 2: Adição e subtração simples
        num1 = random.randint(1, 10 + (level * 2))
        num2 = random.randint(1, 10 + (level * 2))
        operator = random.choice(['+', '-'])
        if operator == '-' and num1 < num2:
            num1, num2 = num2, num1  # Evitar resultados negativos
    elif level <= 5:  # Níveis 3 a 5: Adição, subtração e multiplicação
        num1 = random.randint(5, 20 + (level * 3))
        num2 = random.randint(2, 10 + level)
        operator = random.choice(['+', '-', '*'])
        if operator == '-' and num1 < num2:
            num1, num2 = num2, num1
    elif level <= 8:  # Níveis 6 a 8: Adição, subtração, multiplicação e divisão
        num2 = random.randint(2, 15 + (level - 5))
        num1 = num2 * random.randint(2, 10 + (level - 5)) # Garantir divisão exata
        operator = random.choice(['+', '-', '*', '/'])
        if operator == '-' and num1 < num2:
            num1, num2 = num2, num1
    else:  # Níveis 9 e 10: Operações mais desafiadoras
        num2 = random.randint(5, 25)
        num1 = num2 * random.randint(5, 20)
        operator = random.choice(['+', '-', '*', '/'])
        if operator == '-' and num1 < num2:
            num1, num2 = num2, num1

    question = f"Quanto é {num1} {operator} {num2}?"
    if operator == '+':
        answer = num1 + num2
    elif operator == '-':
        answer = num1 - num2
    elif operator == '*':
        answer = num1 * num2
    else:  # Divisão
        answer = num1 // num2
    return question, answer

# Inicialização do estado da sessão
def init_session_state():
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "current_answer" not in st.session_state:
        st.session_state.current_answer = None
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "feedback" not in st.session_state:
        st.session_state.feedback = ""

# Função para processar a resposta do usuário
def check_answer():
    user_answer = st.session_state.user_input_answer
    if user_answer == st.session_state.current_answer:
        st.session_state.score += 1
        st.session_state.feedback = "Correto!"
        if st.session_state.score < 10:
            question, answer = generate_question(st.session_state.score + 1)
            st.session_state.current_question = question
            st.session_state.current_answer = answer
    else:
        st.session_state.feedback = f"Incorreto! A resposta correta era {st.session_state.current_answer}. O jogo será reiniciado."
        st.session_state.score = 0
        question, answer = generate_question(st.session_state.score + 1) # Reinicia com pergunta fácil
        st.session_state.current_question = question
        st.session_state.current_answer = answer
    # Limpa o input do usuário para a próxima pergunta
    st.session_state.user_input_answer = None

# Função principal do aplicativo
def main():
    st.title("Desafio da Matemática")
    init_session_state()

    # 1. Perguntar o nome do usuário
    if not st.session_state.username:
        st.session_state.username = st.text_input("Digite seu nome para começar:", key="username_input")
        if st.session_state.username:
            st.experimental_rerun() # Reruns once name is entered
    
    # Se o nome foi inserido, mostrar o resto do jogo
    else:
        st.write(f"Olá, {st.session_state.username}! Boa sorte.")
        st.write(f"**Pontuação: {st.session_state.score}**")

        # Exibir feedback da última resposta
        if st.session_state.feedback:
            if "Correto" in st.session_state.feedback:
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
            st.session_state.feedback = "" # Limpa o feedback após exibição

        # Botão para iniciar ou reiniciar o jogo
        if not st.session_state.game_started:
            if st.button("Começar o Desafio!", key="start_button"):
                st.session_state.score = 0
                st.session_state.game_started = True
                question, answer = generate_question(st.session_state.score + 1)
                st.session_state.current_question = question
                st.session_state.current_answer = answer
                st.experimental_rerun()

        # Lógica do jogo em andamento
        if st.session_state.game_started:
            if st.session_state.score >= 10:
                st.success("Parabéns! Você venceu o Desafio da Matemática!")
                st.balloons()
                st.session_state.game_started = False # Termina o jogo
                if st.button("Jogar Novamente", key="play_again_button"):
                    st.session_state.score = 0
                    st.session_state.username = ""
                    st.session_state.current_question = None
                    st.session_state.current_answer = None
                    st.experimental_rerun()

            else:
                # Apresentar a pergunta
                st.write(st.session_state.current_question)
                
                # Campo de entrada para a resposta do usuário e botão de envio
                st.number_input("Sua resposta:", format="%d", step=1, key="user_input_answer", on_change=check_answer)
                st.button("Enviar Resposta", on_click=check_answer, key="submit_answer_button")

if __name__ == "__main__":
    main()
