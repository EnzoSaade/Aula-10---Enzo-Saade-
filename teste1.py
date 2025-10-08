import streamlit as st

# --- Configurações Iniciais ---
st.set_page_config(
    page_title="Invenção do Laboratório do Futuro",
    page_icon="🔬"
)

# Definição do Título e Saudação
st.title("Invenção do Laboratório do Futuro (Meu Programa)")
st.markdown("---")
st.write("### Olá, Recruta! Seja bem-vindo ao meu domínio!")

# 1. Entrada de Nome
nome = st.text_input("Digite o seu nome de companheiro de laboratório:")
if nome:
    # A saudação inicial usa um toque de HOUOUIN KYOUMA!
    st.markdown(f"**Eu sou Hououin Kyouma!** Saudações, {nome.upper()}! O destino da humanidade depende do seu próximo passo.")
    st.markdown("---")

# 2. Diálogo Criativo (Chat)
# Inicializa o histórico de chat na sessão, se ainda não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

st.header("Terminal de Comunicação com a Base (Chat)")

# Exibe as mensagens históricas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Processa a entrada do usuário
if prompt := st.chat_input("Diga algo ao Hououin Kyouma..."):
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibe a mensagem do usuário imediatamente
    with st.chat_message("user"):
        st.markdown(prompt)

    # Lógica de Resposta do "Cientista Maluco" (Mock LLM/Personagem)
    # Em uma aplicação real, você faria uma chamada para a API Gemini aqui.
    
    response = ""
    lower_prompt = prompt.lower()
    
    if any(keyword in lower_prompt for keyword in ["olá", "oi", "bom dia"]):
        response = "Mwahaha! Eu sou Hououin Kyouma! O que o trouxe ao epicentro da conspiração neste momento?"
    elif any(keyword in lower_prompt for keyword in ["site", "programa", "o que é"]):
        response = "Isto é um Dispositivo de Observação do Mundo, disfarçado de site! Uma arma contra a Organização. Não toque em nada!"
    elif any(keyword in lower_prompt for keyword in ["tempo", "viagem"]):
        response = "A viagem no tempo... uma fronteira perigosa, mas necessária! Nossas invenções estão perto da perfeição, recruta!"
    elif any(keyword in lower_prompt for keyword in ["agência", "organização", "sern"]):
        response = "A Organização está observando! Seja cauteloso com suas palavras, pois até as borboletas podem causar tsunamis dimensionais! (El Psy Congroo)"
    else:
        # Resposta padrão
        import random
        dramatic_phrases = [
            "Não me subestime! Essa é a Escolha de Steins;Gate!",
            "Eu já previ isso. É o curso natural das coisas. Não há escapatória!",
            "O mundo está prestes a mudar. Prepare-se para o caos que está por vir!",
            "Pff... parece que terei que usar o telefone micro-ondas! Espere o D-Mail!"
        ]
        response = random.choice(dramatic_phrases)

    # Exibe e adiciona a resposta do "Assistente" (Personagem)
    with st.chat_message("assistant"):
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# 3. Imagem do Personagem
st.markdown("---")
st.header("O Líder do Laboratório")
st.write("O grande gênio e cientista louco, Hououin Kyouma, também conhecido como **Okabe Rintarou**!")

# Use uma URL de imagem de Okabe Rintarou. Substitua pela sua imagem preferida.
# Usando um placeholder de imagem para Okabe Rintarou com um fundo preto para estilo.
okabe_image_url = "https://placehold.co/600x400/000000/ffffff?text=OKABE%20RINTAROU%20%7C%20El%20Psy%20Congroo"

# Adicione um fallback para imagens reais do Steins;Gate
# Se o link acima não funcionar ou você quiser um visual melhor:
# okabe_image_url = "https://i.pinimg.com/originals/9f/8e/3c/9f8e3c5a6d71b7f0f63b20e0f8f8b8a5.jpg"

st.image(
    okabe_image_url,
    caption="El Psy Congroo!",
    width=None
)
st.markdown(
    """
    <style>
    /* Estilizando o contêiner de imagem para um melhor visual */
    .stImage {
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    </style>
    """,
    unsafe_allow_html=True
)
