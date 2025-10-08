import streamlit as st
import time # Para simular o "efeito digitando"

# --- Configuração da Página e "Efeitos Especiais" ---
st.set_page_config(
    page_title="Consultor Jurídico Criativo - LawUni",
    page_icon="⚖️",
    layout="wide", # Usa a largura total da tela
    initial_sidebar_state="expanded"
)

# Tema e Cores
st.markdown("""
<style>
.stApp {
    background-color: #f0f2f6; /* Cor de fundo suave */
}
/* Estilo para um banner/cabeçalho mais impactante */
.css-1avcm0c {
    background-color: #0e1117; /* Cor escura para o topo da sidebar (opcional) */
}
.big-font {
    font-size:30px !important;
    font-weight: bold;
    color: #4CAF50; /* Verde-Lei */
    text-shadow: 2px 2px 4px #000000; /* Efeito de sombra no texto */
}
</style>
""", unsafe_allow_html=True)

# --- Variáveis de Sessão para Diálogo (Mantém o Histórico) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Título e Cabeçalho Criativo ---
st.markdown('<p class="big-font">⚖️ Law-Bot: A Consulta Criativa com I.A. Jurídica</p>', unsafe_allow_html=True)
st.subheader("Simulação de Aplicação para a Universidade de Direito")
st.markdown("---")

# --- Função de Resposta do Bot (Onde a Criatividade Acontece) ---
def law_bot_response(prompt, area):
    """Gera uma resposta criativa e temática baseada na entrada e área."""
    
    # Simula o processamento
    with st.spinner('Pensando como um juiz... 🧑‍⚖️'):
        time.sleep(1.5) 
    
    # Respostas baseadas no tema e área
    if area == "Direito Penal":
        response = (
            f"Excelente questão em **{area}**! Seu desafio me faz pensar no princípio da _intervenção mínima_."
            " Seu caso gira em torno da **culpabilidade** ou da **ilicitude**? "
            "Para uma análise criativa, imagine: Se o réu fosse um personagem de ficção, qual seria seu dilema moral/legal?"
        )
    elif area == "Direito Civil/Contratos":
        response = (
            f"Uma disputa em **{area}** é um jogo de equilíbrio. O cerne aqui é a **boa-fé objetiva** e o _pacta sunt servanda_."
            " Você está buscando o cumprimento do contrato ou uma resolução por **onerosidade excessiva**? "
            "Pense fora da caixa: Que cláusula 'invisível' a equidade sugere neste caso?"
        )
    elif area == "Direito Constitucional":
        response = (
            f"Ah, **Direito Constitucional**, a base de tudo! Estamos tratando de um conflito de **direitos fundamentais** ou de uma questão de **separação de Poderes**?"
            " A chave criativa é a _ponderação_."
            " Se você fosse o constituinte, qual emenda proporia para resolver este impasse?"
        )
    else:
        response = (
            "Compreendido. Sua questão é complexa e exige uma abordagem **multidisciplinar**."
            " Como um exercício criativo, proponho: Qual seria a solução mais **justa**, mesmo que não fosse a estritamente legal? "
            "O Direito, afinal, é uma arte de conciliação."
        )

    # Efeito de texto "digitando"
    with st.chat_message("assistant", avatar="🤖"):
        full_response = ""
        message_placeholder = st.empty()
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
    return response

# --- Sidebar com Opções Interativas (Efeito de Filtro) ---
with st.sidebar:
    st.title("🗂️ Filtro de Caso")
    selected_area = st.selectbox(
        "Selecione a Área do Direito para Focar a Análise Criativa:",
        ("Direito Penal", "Direito Civil/Contratos", "Direito Constitucional", "Outras Áreas/Geral"),
        index=0,
        help="O Law-Bot ajustará a linguagem e os conceitos."
    )
    st.markdown("---")
    st.info("Este é um projeto acadêmico de simulação. Não substitui a consulta a um advogado real.")
    
# --- Diálogo Interativo (Aplicações de LLM/Chat) ---

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

# Mensagem inicial, se for a primeira vez
if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": "Olá! Sou o Law-Bot ⚖️ da sua universidade. Descreva seu dilema jurídico para iniciarmos uma análise criativa baseada em princípios.", "avatar": "🤖"})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(st.session_state.messages[-1]["content"])


# Campo de entrada do usuário
if prompt := st.chat_input("Descreva seu dilema legal..."):
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "🧑‍🎓"})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    # Obtém e exibe a resposta do Law-Bot
    law_bot_response(prompt, selected_area)
