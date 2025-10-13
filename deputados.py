import pandas as pd 
import streamlit as st
import plotly.express as px 

st.set_page_config(layout="centered", page_title="Deputados Federais") 
st.title("🏛️ Distribuição de Deputados Federais por Partido Político")

# Carregar os dados
@st.cache_data
def load_data(url):
    """Carrega os dados de um CSV e retorna um DataFrame."""
    try:
        # Tenta carregar o arquivo
        data = pd.read_csv(url)
        # Converte nomes de colunas para minúsculas (mantendo a consistência)
        data.columns = data.columns.str.lower()
        return data
    except Exception as e:
        st.error(f"Erro ao carregar os dados. Verifique a URL ou o formato do arquivo: {e}")
        return pd.DataFrame() 

DATA_URL = 'https://www.irdx.com.br/media/uploads/deputados_2022.csv'
df = load_data(DATA_URL)

if not df.empty:
    
    # --- CORREÇÃO APLICADA AQUI ---
    # Usando o nome correto da coluna, conforme as colunas disponíveis no seu DataFrame.
    NOME_COLUNA_PARTIDO = 'partido' 
    # ------------------------------
    
    # Confirma se a coluna existe após a conversão para minúsculas
    if NOME_COLUNA_PARTIDO not in df.columns:
        st.error(f"Coluna '{NOME_COLUNA_PARTIDO}' ainda não encontrada. Por favor, verifique o nome exato.")
    else:
        # --- Preparação dos Dados para o Gráfico ---
        
        # 1. Contar a frequência de cada partido
        contagem_partidos = df[NOME_COLUNA_PARTIDO].value_counts().reset_index()
        contagem_partidos.columns = ['Partido', 'Número de Deputados']

        # 2. Criar o Gráfico de Barras Interativo com Plotly Express
        fig = px.bar(
            contagem_partidos,
            x='Número de Deputados', 
            y='Partido',             
            orientation='h',         
            title='Contagem de Deputados por Partido Político',
            color='Número de Deputados', 
            color_continuous_scale=px.colors.sequential.Plotly3,
            text='Número de Deputados'
        )

        # 3. Otimização visual do layout
        fig.update_layout(
            xaxis_title="Número de Deputados",
            yaxis_title="Partido Político",
            yaxis={'categoryorder':'total ascending'}, # Ordena as barras da menor para a maior
            uniformtext_minsize=8, # Adiciona texto com valor nas barras
            uniformtext_mode='hide'
        )

        # --- Exibir o Gráfico no Streamlit ---
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Tabela de Contagem")
        st.dataframe(contagem_partidos, hide_index=True)

        st.caption("Fonte dos dados: IRDX (Deputados 2022).")
