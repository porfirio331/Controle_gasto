
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Controle de Gastos Familiares", layout="centered")

st.title("Controle de Gastos Familiares")

# Inicialização do estado
if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=["Data", "Categoria", "Descrição", "Valor", "Tipo", "Forma de Pagamento", "Observações"])

# Formulário de entrada de dados
with st.form("entrada_dados"):
    st.subheader("Nova Transação")
    col1, col2 = st.columns(2)
    data = col1.date_input("Data", value=date.today())
    categoria = col2.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Saúde", "Moradia", "Educação", "Outros"])
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor", min_value=0.0, step=0.01)
    tipo = st.radio("Tipo", ["Entrada", "Saída"], horizontal=True)
    forma_pagamento = st.selectbox("Forma de Pagamento", ["Dinheiro", "Cartão", "Transferência", "Pix", "Outros"])
    observacoes = st.text_input("Observações")

    submitted = st.form_submit_button("Adicionar")
    if submitted:
        nova_linha = {
            "Data": data,
            "Categoria": categoria,
            "Descrição": descricao,
            "Valor": valor,
            "Tipo": tipo,
            "Forma de Pagamento": forma_pagamento,
            "Observações": observacoes
        }
        st.session_state.dados = pd.concat([st.session_state.dados, pd.DataFrame([nova_linha])], ignore_index=True)
        st.success("Transação adicionada com sucesso!")

# Exibir tabela
st.subheader("Todas as Transações")
st.dataframe(st.session_state.dados, use_container_width=True)

# Resumo
st.subheader("Resumo Financeiro")
total_entradas = st.session_state.dados.query("Tipo == 'Entrada'")["Valor"].sum()
total_saidas = st.session_state.dados.query("Tipo == 'Saída'")["Valor"].sum()
saldo = total_entradas - total_saidas

col1, col2, col3 = st.columns(3)
col1.metric("Entradas", f"R$ {total_entradas:,.2f}")
col2.metric("Saídas", f"R$ {total_saidas:,.2f}")
col3.metric("Saldo", f"R$ {saldo:,.2f}")

# Gráfico de categorias
st.subheader("Gastos por Categoria")
gastos_categoria = st.session_state.dados.query("Tipo == 'Saída'").groupby("Categoria")["Valor"].sum()

if not gastos_categoria.empty:
    fig, ax = plt.subplots()
    gastos_categoria.plot.pie(ax=ax, autopct="%.1f%%", startangle=90)
    ax.set_ylabel("")
    st.pyplot(fig)
else:
    st.info("Nenhum gasto registrado para exibir o gráfico.")

# Exportar dados
st.subheader("Exportar Dados")
col1, col2 = st.columns(2)
if col1.download_button("Baixar como CSV", st.session_state.dados.to_csv(index=False).encode("utf-8"), file_name="controle_gastos.csv"):
    st.success("Arquivo CSV gerado com sucesso.")
if col2.download_button("Baixar como Excel", st.session_state.dados.to_excel(index=False, engine="openpyxl"), file_name="controle_gastos.xlsx"):
    st.success("Arquivo Excel gerado com sucesso.")
