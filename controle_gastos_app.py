
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Controle de Gastos Familiares", layout="wide")

if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=["Data", "Descrição", "Valor", "Categoria"])

st.title("Controle de Gastos Familiares")

with st.form("form_lancamento"):
    col1, col2, col3 = st.columns([2, 4, 2])
    data = col1.date_input("Data")
    descricao = col2.text_input("Descrição")
    valor = col3.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f")
    categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Outros"])
    submitted = st.form_submit_button("Adicionar")

    if submitted and descricao and valor:
        novo = {"Data": data, "Descrição": descricao, "Valor": valor, "Categoria": categoria}
        st.session_state.dados = pd.concat([st.session_state.dados, pd.DataFrame([novo])], ignore_index=True)
        st.success("Gasto adicionado com sucesso!")

st.markdown("---")
st.subheader("Tabela de Gastos")
st.dataframe(st.session_state.dados, use_container_width=True)

col1, col2 = st.columns([1, 1])
total_gasto = st.session_state.dados["Valor"].sum()
col1.metric("Total Gasto", f"R$ {total_gasto:,.2f}")

# Criar um botão para exportar como Excel
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    st.session_state.dados.to_excel(writer, index=False, sheet_name='Gastos')

output.seek(0)

col2.download_button(
    label="Baixar como Excel",
    data=output,
    file_name="controle_gastos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Gráfico de gastos por categoria
if not st.session_state.dados.empty:
    st.subheader("Distribuição de Gastos por Categoria")
    fig, ax = plt.subplots()
    st.session_state.dados.groupby("Categoria")["Valor"].sum().plot.pie(
        autopct="%.1f%%", ax=ax, figsize=(6, 6), ylabel=""
    )
    st.pyplot(fig)
