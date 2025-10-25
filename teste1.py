import streamlit as st
import requests
import pandas as pd
from typing import List, Dict, Any, Optional

API_BASE = "https://dadosabertos.camara.leg.br/api/v2"

st.set_page_config(page_title="Deputados - Despesas e Comissões", layout="wide")


@st.cache_data(ttl=60 * 60)
def buscar_deputados(nome: str, itens: int = 50) -> List[Dict[str, Any]]:
    """Busca deputados por nome na API da Câmara"""
    url = f"{API_BASE}/deputados"
    params = {"nome": nome, "ordem": "ASC", "ordenarPor": "nome", "itens": itens}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("dados", [])
    except requests.RequestException as e:
        st.error(f"Erro na conexão ao buscar deputados: {e}")
        return []


@st.cache_data(ttl=60 * 60)
def obter_detalhes_deputado(id_deputado: int) -> Optional[Dict[str, Any]]:
    url = f"{API_BASE}/deputados/{id_deputado}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json().get("dados")
    except requests.RequestException as e:
        st.error(f"Erro ao buscar detalhes do deputado: {e}")
        return None


@st.cache_data(ttl=30 * 60)
def obter_despesas_deputado(id_deputado: int, ano: int = 2023, mes: Optional[int] = None, limite: int = 100) -> List[Dict[str, Any]]:
    url = f"{API_BASE}/deputados/{id_deputado}/despesas"
    params = {
        "ano": ano,
        "ordem": "DESC",
        "ordenarPor": "dataDocumento",
        "itens": limite
    }
    if mes:
        params["mes"] = mes
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json().get("dados", [])
    except requests.RequestException as e:
        st.error(f"Erro ao buscar despesas: {e}")
        return []


@st.cache_data(ttl=30 * 60)
def obter_comissoes_deputado(id_deputado: int, itens: int = 100) -> List[Dict[str, Any]]:
    url = f"{API_BASE}/deputados/{id_deputado}/orgaos"
    params = {"itens": itens}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("dados", [])
    except requests.RequestException as e:
        st.error(f"Erro ao buscar comissões: {e}")
        return []


def despesas_para_df(despesas: List[Dict[str, Any]]) -> pd.DataFrame:
    if not despesas:
        return pd.DataFrame()
    df = pd.DataFrame(despesas)
    # Normalizar valorDocumento para float
    if 'valorDocumento' in df.columns:
        df['valorDocumento'] = pd.to_numeric(df['valorDocumento'], errors='coerce').fillna(0.0)
    return df


def calcular_total_despesas(despesas: List[Dict[str, Any]]) -> float:
    if not despesas:
        return 0.0
    return sum(float(d.get('valorDocumento', 0) or 0) for d in despesas)


def mostrar_info_basica(deputado: Dict[str, Any], detalhes: Optional[Dict[str, Any]]):
    st.subheader(deputado.get("nome", "Nome não disponível"))
    cols = st.columns(3)
    cols[0].markdown(f"**Partido**: {deputado.get('siglaPartido','-')}")
    cols[1].markdown(f"**UF**: {deputado.get('siglaUf','-')}")
    cols[2].markdown(f"**ID**: {deputado.get('id','-')}")
    st.write("---")
    if detalhes:
        st.markdown(f"- **Email**: {detalhes.get('email', 'Não disponível')}")
        st.markdown(f"- **Situação**: {detalhes.get('situacao', 'Não disponível')}")
        st.markdown(f"- **Condição Eleitoral**: {detalhes.get('condicaoEleitoral', 'Não disponível')}")
        st.markdown(f"- **CPF**: {detalhes.get('cpf', 'Não disponível')}")
        st.markdown(f"- **Data de Nascimento**: {detalhes.get('dataNascimento', 'Não disponível')}")
        st.markdown(f"- **Escolaridade**: {detalhes.get('escolaridade', 'Não disponível')}")
        st.markdown(f"- **Município de Nascimento**: {detalhes.get('municipioNascimento', 'Não disponível')}")


def mostrar_despesas_ui(deputado_id: int, nome_deputado: str):
    st.header(f"Despesas — {nome_deputado}")
    col1, col2, col3 = st.columns([1, 1, 1])
    ano = col1.number_input("Ano", min_value=2000, max_value=2100, value=2023, step=1)
    mes = col2.selectbox("Mês (opcional)", options=["Todos", *list(range(1, 13))], index=0)
    limite = col3.slider("Limite de registros", min_value=10, max_value=2000, value=200, step=10)

    mes_param = None if mes == "Todos" else int(mes)

    with st.spinner("Carregando despesas..."):
        despesas = obter_despesas_deputado(deputado_id, ano=int(ano), mes=mes_param, limite=int(limite))
    df = despesas_para_df(despesas)

    if df.empty:
        st.info("Nenhuma despesa encontrada para o período selecionado.")
        return

    total = df['valorDocumento'].sum() if 'valorDocumento' in df.columns else 0.0
    st.metric("Total de Despesas (R$)", f"{total:,.2f}")
    st.write(f"Registros exibidos: {len(df)}")

    # Mostrar tabela principal
    display_cols = ['dataDocumento', 'tipoDespesa', 'nomeFornecedor', 'valorDocumento']
    present_cols = [c for c in display_cols if c in df.columns]
    st.dataframe(df[present_cols].rename(columns={
        'dataDocumento': 'Data',
        'tipoDespesa': 'Tipo',
        'nomeFornecedor': 'Fornecedor',
        'valorDocumento': 'Valor (R$)'
    }).sort_values(by='Valor (R$)', ascending=False), use_container_width=True)

    # Agrupar por tipo de despesa e mostrar gráfico
    if 'tipoDespesa' in df.columns and 'valorDocumento' in df.columns:
        agrup = df.groupby('tipoDespesa', as_index=False)['valorDocumento'].sum().sort_values('valorDocumento', ascending=False).head(15)
        agrup = agrup.rename(columns={'tipoDespesa': 'Tipo', 'valorDocumento': 'Total (R$)'})
        st.bar_chart(data=agrup.set_index('Tipo')['Total (R$)'])


def mostrar_comissoes_ui(deputado_id: int):
    st.header("Comissões")
    with st.spinner("Carregando comissões..."):
        comissoes = obter_comissoes_deputado(deputado_id)
    if not comissoes:
        st.info("Nenhuma comissão encontrada ou erro ao carregar.")
        return
    df = pd.DataFrame(comissoes)
    present = []
    for c in ['siglaOrgao', 'nomeOrgao', 'titulo']:
        if c in df.columns:
            present.append(c)
    if present:
        st.dataframe(df[present].rename(columns={
            'siglaOrgao': 'Sigla',
            'nomeOrgao': 'Nome',
            'titulo': 'Cargo/Título'
        }), use_container_width=True)
    else:
        st.json(comissoes)


def buscar_e_selecionar(nome_busca: str, label: str = "Selecione um deputado"):
    deputados = buscar_deputados(nome_busca)
    if not deputados:
        st.warning("Nenhum deputado encontrado com esse nome.")
        return None
    if len(deputados) == 1:
        return deputados[0]
    options = {f"{d['nome']} ({d.get('siglaPartido','')}/{d.get('siglaUf','')}) — id:{d['id']}": d for d in deputados}
    escolha = st.selectbox(label, options=list(options.keys()))
    return options.get(escolha)


def comparar_deputados_ui():
    st.title("Comparar Despesas entre Deputados")
    col1, col2 = st.columns(2)
    nome1 = col1.text_input("Nome do primeiro deputado")
    nome2 = col2.text_input("Nome do segundo deputado")

    ano = st.number_input("Ano", min_value=2000, max_value=2100, value=2023, step=1)
    mes = st.selectbox("Mês (opcional)", options=["Todos", *list(range(1, 13))], index=0)
    limite = st.slider("Limite por deputado", min_value=50, max_value=2000, value=1000, step=50)

    if st.button("Comparar"):
        if not nome1 or not nome2:
            st.warning("Preencha os dois nomes.")
            return
        dep1 = buscar_e_selecionar(nome1, "Selecione o primeiro deputado")
        dep2 = buscar_e_selecionar(nome2, "Selecione o segundo deputado")
        if not dep1 or not dep2:
            st.warning("Seleção inválida.")
            return
        if dep1['id'] == dep2['id']:
            st.warning("Você selecionou o mesmo deputado duas vezes.")
            return

        mes_param = None if mes == "Todos" else int(mes)
        with st.spinner("Carregando despesas dos deputados..."):
            d1 = obter_despesas_deputado(dep1['id'], ano=int(ano), mes=mes_param, limite=int(limite))
            d2 = obter_despesas_deputado(dep2['id'], ano=int(ano), mes=mes_param, limite=int(limite))

        total1 = calcular_total_despesas(d1)
        total2 = calcular_total_despesas(d2)

        st.subheader("Resultados")
        st.metric(f"{dep1['nome']}", f"R$ {total1:,.2f}")
        st.metric(f"{dep2['nome']}", f"R$ {total2:,.2f}")

        # Gráfico de comparação
        comp_df = pd.DataFrame({
            "Deputado": [dep1['nome'], dep2['nome']],
            "Total (R$)": [total1, total2]
        }).set_index("Deputado")
        st.bar_chart(comp_df["Total (R$)"])

        # Mostrar detalhes (10 primeiros) se o usuário quiser
        if st.checkbox("Ver detalhamento (10 primeiras despesas de cada)"):
            df1 = despesas_para_df(d1).head(10)
            df2 = despesas_para_df(d2).head(10)
            st.write(f"Despesas de {dep1['nome']}")
            st.dataframe(df1[['dataDocumento', 'tipoDespesa', 'nomeFornecedor', 'valorDocumento']].rename(columns={
                'dataDocumento': 'Data',
                'tipoDespesa': 'Tipo',
                'nomeFornecedor': 'Fornecedor',
                'valorDocumento': 'Valor (R$)'
            }), use_container_width=True)

            st.write(f"Despesas de {dep2['nome']}")
            st.dataframe(df2[['dataDocumento', 'tipoDespesa', 'nomeFornecedor', 'valorDocumento']].rename(columns={
                'dataDocumento': 'Data',
                'tipoDespesa': 'Tipo',
                'nomeFornecedor': 'Fornecedor',
                'valorDocumento': 'Valor (R$)'
            }), use_container_width=True)


def main():
    st.title("🔎 Sistema de Informações de Deputados Federais")
    st.sidebar.header("Navegação")
    menu = st.sidebar.radio("Escolha uma seção", ["Buscar deputado", "Comparar deputados", "Sobre"])

    if menu == "Buscar deputado":
        st.header("Buscar e visualizar deputado")
        nome = st.text_input("Digite o nome completo ou parte do nome do deputado")
        if st.button("Buscar"):
            if not nome:
                st.warning("Digite um nome para busca.")
            else:
                with st.spinner("Buscando deputados..."):
                    deputados = buscar_deputados(nome)
                if not deputados:
                    st.info("Nenhum deputado encontrado.")
                else:
                    if len(deputados) == 1:
                        deputado = deputados[0]
                    else:
                        options = {f"{d['nome']} ({d.get('siglaPartido','')}/{d.get('siglaUf','')}) — id:{d['id']}": d for d in deputados}
                        escolha = st.selectbox("Resultados encontrados — selecione um", options=list(options.keys()))
                        deputado = options[escolha]

                    detalhes = obter_detalhes_deputado(deputado['id'])
                    mostrar_info_basica(deputado, detalhes)
                    st.write("---")
                    mostrar_despesas_ui(deputado['id'], deputado.get('nome', '---'))
                    st.write("---")
                    mostrar_comissoes_ui(deputado['id'])

    elif menu == "Comparar deputados":
        comparar_deputados_ui()
    else:
        st.header("Sobre")
        st.markdown(
            """
            App criado para consultar a API de Dados Abertos da Câmara dos Deputados.
            Funcionalidades:
            - Buscar deputados por nome
            - Exibir informações básicas e detalhes
            - Listar e agregadar despesas por ano/mês
            - Listar comissões
            - Comparar despesas entre dois deputados
            
            Desenvolvido a partir do script original enviado por você.
            """
        )


if __name__ == "__main__":
    main()
