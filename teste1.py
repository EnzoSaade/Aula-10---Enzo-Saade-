import streamlit as st
import time

# --- Tema e Configurações Iniciais ---
st.set_page_config(
    page_title="37 Anos de Constituição Cidadã",
    page_icon="🇧🇷",
    layout="centered"
)

# Estilos Temáticos do Brasil (Verde, Amarelo, Azul)
# Adiciona estilos para cabeçalhos e botões de chat para dar um toque brasileiro
st.markdown("""
<style>
/* Fundo da aplicação */
.stApp {
    background-color: #f0f8ff; /* Azul claro/branco para neutralidade */
    color: #002776; /* Azul Escuro */
}
/* Título Principal */
h1 {
    color: #009246; /* Verde Bandeira */
    text-align: center;
    border-bottom: 3px solid #FFDE00; /* Amarelo Ouro */
    padding-bottom: 10px;
}
/* Subtítulos */
h2 {
    color: #002776; /* Azul Escuro */
}
/* Botão de Chat (Input) */
[data-testid="stFormSubmitButton"] {
    background-color: #009246; /* Verde */
    color: white;
    border-radius: 8px;
    transition: background-color 0.3s;
}
[data-testid="stFormSubmitButton"]:hover {
    background-color: #FFDE00; /* Amarelo no hover */
    color: #002776;
    border: 1px solid #002776;
}
/* Mensagens do Assistente (Para o Diálogo parecer oficial/constitucional) */
.stChatMessage [data-testid="stMarkdownContainer"] {
    background-color: #E6F3FF; /* Azul Bebê para assistente */
    padding: 10px;
    border-radius: 10px;
    border-left: 5px solid #002776; /* Linha Azul Escura */
}
</style>
""", unsafe_allow_html=True)


# --- Dados e Imagens ---
ANIVERSARIO_ANOS = 37
CONSTITUICAO_ANO = 1988
# Imagem placeholder do livro da Constituição
CONSTITUICAO_IMAGE_URL = "https://placehold.co/600x200/002776/ffffff?text=CONSTITUI%C3%87%C3%83O%201988%20|%2037%20ANOS"

# Diálogo pré-definido para simular a interação
DIALOGO = [
    {
        "pergunta": f"Olá! Eu sou o Guardião da Lei. Antes de iniciarmos nossa celebração dos **{ANIVERSARIO_ANOS} anos** da nossa Constituição, qual é o seu nome, Cidadão?",
        "estado": "aguardando_nome"
    },
    {
        "pergunta": "Excelente, {nome}! Nossa Constituição é carinhosamente apelidada de **'Constituição Cidadã'**. Você sabe qual é o principal motivo para este apelido?",
        "estado": "aguardando_apelido",
        "resposta_correta": ["direitos sociais", "democratização", "cidadania"],
        "dica": "Pense no que ela restaurou para o povo brasileiro após o período militar."
    },
    {
        "pergunta": "Perfeito! A ênfase nos **Direitos Sociais** foi um marco. Agora, me diga, o que a Constituição de 88 estabeleceu como **Fundamentos** da República Federativa do Brasil? (Dica: Pense no famoso 'S O C I D I V A P L U'!)",
        "estado": "aguardando_fundamentos",
        "resposta_correta": ["soberania", "cidadania", "dignidade da pessoa humana", "valores sociais do trabalho e da livre iniciativa", "pluralismo político"],
        "dica": "O Artigo 1º é a chave! Um dos fundamentos é a **Dignidade da Pessoa Humana**."
    },
    {
        "pergunta": "Magnífico! A **Dignidade Humana** é o pilar. Por último: Qual foi a grande inovação de 88 na área da **Seguridade Social**? (Saúde, Previdência e Assistência)",
        "estado": "aguardando_seguridade",
        "resposta_correta": ["saúde como direito de todos", "sistema único de saúde", "sus"],
        "dica": "Começa com a sigla S U S..."
    }
]

# --- Inicialização da Sessão ---
if "nome" not in st.session_state:
    st.session_state.nome = None
if "dialogo_step" not in st.session_state:
    st.session_state.dialogo_step = 0
if "messages" not in st.session_state:
    st.session_state.messages = []


# --- Funções de Diálogo ---

def get_dialogo_message(step):
    """Retorna a pergunta ou encerramento do diálogo no passo atual."""
    if step < len(DIALOGO):
        return DIALOGO[step]["pergunta"]
    else:
        return f"Parabéns, {st.session_state.nome}! Sua dedicação aos fundamentos da nossa República é inquestionável. A celebração dos {ANIVERSARIO_ANOS} anos da Constituição de 1988 é um momento de reafirmar a nossa **Democracia** e a **Cidadania** plena. Obrigado por participar! **VIVA O BRASIL!**"

def handle_user_input(user_prompt):
    """Processa a resposta do usuário e avança o diálogo."""
    current_step = st.session_state.dialogo_step
    
    if current_step == 0:
        # Passo 0: Coleta o nome
        st.session_state.nome = user_prompt.strip().title()
        st.session_state.dialogo_step = 1
        return get_dialogo_message(st.session_state.dialogo_step)
        
    elif current_step > 0 and current_step < len(DIALOGO):
        # Passos 1 a 3: Validação de respostas
        # CORREÇÃO: Usar current_step diretamente, pois ele indica o índice da pergunta sendo respondida.
        estado_atual = DIALOGO[current_step]
        respostas_validas = estado_atual["resposta_correta"]
        
        # Normaliza a entrada do usuário para comparação
        prompt_normalizado = user_prompt.strip().lower()
        
        # Verifica se alguma palavra-chave correta está na resposta
        if any(key in prompt_normalizado for key in respostas_validas):
            st.session_state.dialogo_step += 1
            feedback = "Correto! Isso mostra seu conhecimento da Carta Magna."
        else:
            feedback = f"Sua resposta está incompleta. Uma dica: **{estado_atual['dica']}**. Tente novamente!"
            # Não avança o passo, repete a pergunta
            return feedback + "\n\n" + get_dialogo_message(current_step)

        # Se a resposta foi correta, avança para a próxima pergunta
        if st.session_state.dialogo_step < len(DIALOGO):
            return feedback + "\n\n" + get_dialogo_message(st.session_state.dialogo_step)
        else:
            # Diálogo final
            st.session_state.dialogo_step = len(DIALOGO)
            return feedback + "\n\n" + get_dialogo_message(st.session_state.dialogo_step)
            
    else:
        # Diálogo concluído
        return "Nossa celebração está encerrada! Sinta-se à vontade para refletir sobre a importância da nossa Constituição."


# --- Interface do Usuário ---

st.title(f"🎉 {ANIVERSARIO_ANOS} Anos da Constituição Cidadã! 🎉")

# Exibe a imagem temática
st.image(
    CONSTITUICAO_IMAGE_URL,
    caption=f"Constituição Federal de {CONSTITUICAO_ANO} - O Pilar da Democracia Brasileira"
)

st.markdown("---")
st.header("Diálogo com o Guardião da Lei")

# --- Lógica do Chat ---

# Mensagem inicial do assistente (se for o primeiro acesso)
if st.session_state.dialogo_step == 0 and not st.session_state.messages:
    initial_message = get_dialogo_message(0)
    st.session_state.messages.append({"role": "assistant", "content": initial_message})

# Exibe as mensagens históricas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if st.session_state.dialogo_step < len(DIALOGO):
    user_prompt = st.chat_input("Escreva sua resposta aqui...")
    if user_prompt:
        # Adiciona a mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # Exibe a mensagem do usuário imediatamente
        with st.chat_message("user"):
            st.markdown(user_prompt)
        
        # Processa a resposta
        response = handle_user_input(user_prompt)
        
        # Exibe a resposta do assistente (com um pequeno delay para efeito de digitação)
        with st.chat_message("assistant"):
            st_response = st.empty()
            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                st_response.markdown(full_response)
                time.sleep(0.05) # Pequeno delay para efeito
            
            # Adiciona a resposta final ao histórico
            st.session_state.messages.append({"role": "assistant", "content": response})

else:
    # Quando o diálogo termina, exibe o encerramento no chat
    # Garantir que a mensagem final seja exibida apenas uma vez
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != get_dialogo_message(len(DIALOGO)):
        final_message = get_dialogo_message(len(DIALOGO))
        st.session_state.messages.append({"role": "assistant", "content": final_message})
        st.chat_message("assistant").markdown(final_message)
    
    st.markdown(f"### 🎉 **Parabéns, {st.session_state.nome}! Diálogo Concluído.** 🎉")

