import pandas as pd 
import streamlit as st
import plotly.express as px 

# Configurações iniciais do Streamlit
st.set_page_config(layout="centered") 
st.title("Distribuição de Deputados Federais por Partido Político")

# Carregar os dados
# O Streamlit tem um cache para carregar dados que não mudam, o que otimiza o desempenho
@st.cache_data
def load_data(url):
    """Carrega os dados de um CSV e retorna um DataFrame."""
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame() # Retorna um DataFrame vazio em caso de erro

DATA_URL = 'https://www.irdx.com.br/media/uploads/deputados_2022.csv'
df = load_data(DATA_URL)

if not df.empty:
    # --- Preparação dos Dados para o Gráfico ---

    # 1. Contar a frequência de cada partido político na coluna 'PARTIDO'
    # Esta operação conta quantos deputados cada partido tem.
    contagem_partidos = df['PARTIDO'].value_counts().reset_index()
    contagem_partidos.columns = ['Partido', 'Número de Deputados']

    # 2. Criar o Gráfico de Barras Interativo com Plotly Express
    # Usaremos um gráfico de barras para visualizar a contagem.
    fig = px.bar(
        contagem_partidos,
        x='Número de Deputados', # Eixo X: O número de deputados (valor)
        y='Partido',             # Eixo Y: O nome do partido (categoria)
        orientation='h',         # Gráfico de barras horizontal para melhor leitura dos nomes dos partidos
        title='Contagem de Deputados Federais por Partido Político',
        color='Número de Deputados', # Colore as barras pela quantidade
        color_continuous_scale=px.colors.sequential.Viridis, # Escolha de cores
        text='Número de Deputados' # Exibe o valor do número de deputados na barra
    )

    # Otimização visual do layout do gráfico
    fig.update_layout(
        xaxis_title="Número de Deputados",
        yaxis_title="Partido Político",
        yaxis={'categoryorder':'total ascending'} # Ordena as barras da menor para a maior contagem
    )

    # --- Exibir o Gráfico e a Tabela no Streamlit ---

    # Exibe o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

    # Exibe a tabela de dados brutos (opcional, para visualização)
    st.subheader("Dados Agregados")
    st.dataframe(contagem_partidos)

    st.caption("Fonte dos dados: IRDX (Deputados 2022)")
