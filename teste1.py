import streamlit as st
import random
import os

# --- Configurações do App ---
st.set_page_config(
    page_title="Adivinhe o Personagem Anime!",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Variáveis do Jogo ---
IMAGE_DIR = "data" # Pasta onde as imagens dos personagens estão
LIVES = 7 # Número de chances que o usuário tem
WIN_SCORE = 3 # Pontos necessários para ganhar
POSSIBLE_NAMES = {
    "naruto": ["naruto", "naruto uzumaki"],
    "luffy": ["luffy", "monkey d luffy"],
    "goku": ["goku", "son goku"],
    "eren": ["eren", "eren yeager"],
    "levi": ["levi", "levi ackerman"],
    "light": ["light", "light yagami"],
    "saitama": ["saitama", "one punch man"],
    "pikachu": ["pikachu"], # Exemplo para personagens não humanos se quiser
    # ADICIONE MAIS PERSONAGENS AQUI!
    # A chave deve ser o nome base do arquivo (ex: "killua" para killua.jpg)
    # A lista de valores são as variações de nomes aceitáveis
    "zoro": ["zoro", "roronoa zoro"],
    "sanji": ["sanji", "vinsmoke sanji"],
    "sakura": ["sakura", "sakura haruno"],
    "sasuke": ["sasuke", "sasuke uchiha"],
    "kakashi": ["kakashi", "kakashi hatake"],
}

# --- Inicialização do Estado da Sessão ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'lives' not in st.session_state:
    st.session_state.lives = LIVES
if 'current_character' not in st.session_state:
    st.session_state.current_character = None
if 'answered_characters' not in st.session_state:
    st.session_state.answered_characters = [] # Para evitar repetições na mesma rodada
if 'available_characters' not in st.session_state:
    st.session_state.available_characters = []

# --- Funções do Jogo ---

def load_character_images():
    """Carrega os nomes dos arquivos de imagem da pasta 'data'."""
    if not os.path.exists(IMAGE_DIR):
        st.error(f"Erro: A pasta '{IMAGE_DIR}' não foi encontrada. Crie-a e adicione as imagens!")
        return []
    
    images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    # Filtra apenas personagens que têm nomes definidos em POSSIBLE_NAMES
    valid_characters = []
    for img_name in images:
        base_name = os.path.splitext(img_name)[0].lower() # Pega "naruto" de "naruto.jpg"
        if base_name in POSSIBLE_NAMES:
            valid_characters.append(base_name)
        else:
            st.sidebar.warning(f"Atenção: Imagem '{img_name}' na pasta 'data' não tem um nome correspondente em POSSIBLE_NAMES. Ela será ignorada.")
            
    if not valid_characters:
        st.error("Nenhum personagem válido encontrado na pasta 'data' com nomes definidos. Por favor, verifique.")
    
    return valid_characters


def start_new_game():
    """Reinicia o jogo."""
    st.session_state.game_started = True
    st.session_state.score = 0
    st.session_state.lives = LIVES
    st.session_state.answered_characters = []
    
    st.session_state.available_characters = load_character_images()
    if st.session_state.available_characters:
        select_new_character()
    else:
        st.session_state.game_started = False # Não iniciar se não houver personagens

def select_new_character():
    """Seleciona um novo personagem aleatório que ainda não foi respondido."""
    
    remaining_characters = [char for char in st.session_state.available_characters if char not in st.session_state.answered_characters]
    
    if not remaining_characters:
        if st.session_state.score >= WIN_SCORE:
             # Se o usuário já venceu, mesmo sem mais perguntas, podemos encerrar como vitória
            pass # A lógica de vitória já trata isso
        else:
            # Caso não tenha mais perguntas mas não atingiu a vitória
            st.session_state.current_character = "game_over_no_questions"
            st.warning("Você respondeu a todos os personagens disponíveis! Não há mais perguntas.")
        return

    st.session_state.current_character = random.choice(remaining_characters)
    st.session_state.guess_input = "" # Limpa o input do usuário
    st.session_state.feedback = "" # Limpa o feedback anterior
    
def check_guess():
    """Verifica a tentativa do usuário."""
    if st.session_state.guess_input and st.session_state.current_character:
        user_guess = st.session_state.guess_input.strip().lower()
        correct_names = POSSIBLE_NAMES.get(st.session_state.current_character)

        if correct_names and user_guess in correct_names:
            st.session_state.score += 1
            st.session_state.feedback = f"🎉 Acertou! É o(a) {st.session_state.current_character.title()}!"
            st.session_state.answered_characters.append(st.session_state.current_character) # Adiciona aos respondidos
            select_new_character() # Próximo personagem
        else:
            st.session_state.lives -= 1
            st.session_state.feedback = f"❌ Errado! Não é '{user_guess.title()}'. Tente novamente!"
        
        st.session_state.guess_input = "" # Limpa o input para a próxima tentativa

# --- Interface do Streamlit ---

st.title("Adivinhe o Personagem de Anime!")
st.markdown("---")

if not st.session_state.game_started:
    st.header("Bem-vindo(a) ao Desafio Anime!")
    st.markdown(f"Você terá **{LIVES} chances** para acertar o nome de **{WIN_SCORE} personagens** e provar que é um(a) verdadeiro(a) fã!")
    st.image("https://i.imgur.com/2s4P6tZ.png", width=300) # Imagem genérica de animes

    if st.button("Começar Desafio!", use_container_width=True, type="primary"):
        start_new_game()
        st.rerun() # Inicia o jogo e recarrega a página

else:
    # --- Jogo em Andamento ---

    # --- Sidebar com Status do Jogo ---
    st.sidebar.header("Status do Jogo")
    st.sidebar.metric(label="Acertos ⭐", value=st.session_state.score)
    st.sidebar.metric(label="Chances Restantes ❤️", value=st.session_state.lives)
    
    # --- Lógica de Fim de Jogo ---
    if st.session_state.score >= WIN_SCORE:
        st.balloons()
        st.success("## 🎉 VITÓRIA! Você é um(a) mestre dos animes! 🎉")
        st.markdown(f"Você acertou **{st.session_state.score} personagens** e venceu o desafio!")
        st.image("https://i.imgur.com/e2o4Y9C.gif", caption="Parabéns!", use_column_width=True) # GIF de vitória
        if st.button("Jogar Novamente", use_container_width=True, type="primary"):
            start_new_game()
            st.rerun()
        st.stop() # Encerra a execução do script

    if st.session_state.lives <= 0:
        st.error("## 💀 FIM DE JOGO! Suas chances acabaram. 💀")
        st.markdown(f"Você conseguiu **{st.session_state.score} acertos**, mas não foi suficiente desta vez.")
        st.image("https://i.imgur.com/D4sXm7N.gif", caption="Tente de novo!", use_column_width=True) # GIF de derrota
        if st.button("Tentar Novamente", use_container_width=True, type="primary"):
            start_new_game()
            st.rerun()
        st.stop() # Encerra a execução do script
        
    # --- Exibir Personagem e Campo de Adivinhação ---
    if st.session_state.current_character and st.session_state.current_character != "game_over_no_questions":
        character_name_for_image = st.session_state.current_character # Ex: "naruto"
        image_path = os.path.join(IMAGE_DIR, f"{character_name_for_image}.jpg") # Assumindo .jpg, ajuste se usar .png
        
        # Tenta encontrar a imagem com diferentes extensões
        found_image_path = None
        for ext in ['.jpg', '.jpeg', '.png', '.gif']:
            potential_path = os.path.join(IMAGE_DIR, f"{character_name_for_image}{ext}")
            if os.path.exists(potential_path):
                found_image_path = potential_path
                break
        
        if found_image_path:
            st.image(found_image_path, caption="Quem é este personagem?", use_column_width=True)
            st.markdown("---")
            
            # Campo de input para a adivinhação
            st.text_input(
                "Qual o nome deste personagem?",
                key="guess_input",
                on_change=check_guess, # Chama check_guess quando o usuário pressiona Enter
                placeholder="Ex: Naruto ou Monkey D Luffy"
            )
            
            # Botão para verificar (caso o usuário não use Enter)
            if st.button("Verificar Nome", use_container_width=True):
                check_guess()

            # Exibe feedback
            if st.session_state.feedback:
                st.markdown(st.session_state.feedback)
        else:
            st.error(f"Erro: Imagem para '{st.session_state.current_character}' não encontrada em '{IMAGE_DIR}'. Verifique o nome do arquivo e a extensão.")
            st.button("Próximo Personagem (Erro na Imagem)", on_click=select_new_character)

    elif st.session_state.current_character == "game_over_no_questions":
        st.warning("Não há mais personagens disponíveis para adivinhar. Recomece o jogo!")
        if st.button("Recomeçar o Desafio", use_container_width=True, type="primary"):
            start_new_game()
            st.rerun()

    else:
        # Se por algum motivo não carregou personagens no início, ou erro inesperado
        st.error("Ocorreu um erro ao carregar os personagens. Por favor, tente novamente.")
        if st.button("Reiniciar Jogo", use_container_width=True, type="primary"):
            start_new_game()
            st.rerun()
