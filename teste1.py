import streamlit as st
import random

def generate_question(level):
    """Gera uma pergunta de matemática com base no nível de dificuldade."""
    if level <= 2:  # Níveis 1 e 2: Adição e subtração simples
        num1 = random.randint(1, 10 + (level * 5))
        num2 = random.randint(1, 10 + (level * 5))
        operator = random.choice(['+', '-'])
        if operator == '-' and num1 < num2:
            num1, num2 = num2, num1  # Evitar resultados negativos
    elif level <= 5:  # Níveis 3 a 5: Adição, subtração e multiplicação
        num1 = random.randint(5, 20 + (level * 5))
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

# Função principal do aplicativo
def main():
    st.title("Desafio da Matemática")
    init_session_state()

    # 1. Perguntar o nome do usuário
    if not st.session_state.username:
        st.session_state.username = st.text_input("Digite seu nome para começar:")
        if st.session_state.username:
            st.experimental_rerun()
    
    # Se o nome foi inserido, mostrar o resto do jogo
    else:
        st.write(f"Olá, {st.session_state.username}! Boa sorte.")
        st.write(f"**Pontuação: {st.session_state.score}**")

        # Botão para iniciar ou reiniciar o jogo
        if not st.session_state.game_started:
            if st.button("Começar o Desafio!"):
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
                if st.button("Jogar Novamente"):
                    st.session_state.score = 0
                    st.session_state.username = ""
                    st.experimental_rerun()

            else:
                # Apresentar a pergunta
                st.write(st.session_state.current_question)
                
                # Usar um formulário para a resposta
                with st.form(key="answer_form"):
                    user_answer = st.number_input("Sua resposta:", format="%d", step=1)
                    submit_button = st.form_submit_button(label='Enviar')

                if submit_button:
                    if user_answer == st.session_state.current_answer:
                        st.session_state.score += 1
                        st.success("Resposta correta!")
                        if st.session_state.score < 10:
                            # Gera a próxima pergunta
                            question, answer = generate_question(st.session_state.score + 1)
                            st.session_state.current_question = question
                            st.session_state.current_answer = answer
                        st.experimental_rerun()
                    else:
                        st.error(f"Resposta errada! O jogo será reiniciado. A resposta correta era {st.session_state.current_answer}.")
                        st.session_state.score = 0
                        # Gera uma nova pergunta fácil
                        question, answer = generate_question(st.session_state.score + 1)
                        st.session_state.current_question = question
                        st.session_state.current_answer = answer
                        st.experimental_rerun()

if __name__ == "__main__":
    main()
