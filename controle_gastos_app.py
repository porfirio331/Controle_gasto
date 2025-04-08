
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Controle de Gastos", layout="centered")

if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=['Data', 'Categoria', 'Descrição', 'Valor'])
if 'salario' not in st.session_state:
    st.session_state.salario = 0.0

# Estados dos campos de entrada para reset
if 'descricao_temp' not in st.session_state:
    st.session_state.descricao_temp = ''
if 'valor_temp' not in st.session_state:
    st.session_state.valor_temp = ''

st.title("Controle de Gastos Familiares")

st.subheader("Salário Mensal")
salario = st.text_input("Digite seu salário (R$)", value=str(st.session_state.salario).replace('.', ','))

try:
    salario_float = float(salario.replace(',', '.'))
    st.session_state.salario = salario_float
except:
    st.warning("Digite um valor válido para o salário.")
    salario_float = 0.0

st.subheader("Adicionar Gasto")
with st.form("formulario_gastos"):
    col1, col2 = st.columns(2)
    data = col1.date_input("Data")
    categoria = col2.selectbox("Categoria", ["Alimentação", "Transporte", "Moradia", "Lazer", "Educação", "Outros"])
    descricao = st.text_input("Descrição", value=st.session_state.descricao_temp)
    valor_str = st.text_input("Valor (R$)", value=st.session_state.valor_temp)
    enviado = st.form_submit_button("Adicionar")

    if enviado:
        try:
            valor = float(valor_str.replace(',', '.'))
            novo = {'Data': data, 'Categoria': categoria, 'Descrição': descricao, 'Valor': valor}
            st.session_state.dados = pd.concat([st.session_state.dados, pd.DataFrame([novo])], ignore_index=True)
            st.session_state.descricao_temp = ''
            st.session_state.valor_temp = ''
            st.experimental_rerun()
        except:
            st.error("Digite um valor válido com vírgula (,) como separador decimal.")
            st.session_state.descricao_temp = descricao
            st.session_state.valor_temp = valor_str

st.subheader("Gastos Registrados")
st.dataframe(st.session_state.dados, use_container_width=True)

total_gasto = st.session_state.dados['Valor'].sum()
saldo_restante = st.session_state.salario - total_gasto

col1, col2 = st.columns(2)
col1.metric("Total Gasto", f"R$ {total_gasto:,.2f}".replace('.', ','))
col2.metric("Saldo Restante", f"R$ {saldo_restante:,.2f}".replace('.', ','))

st.subheader("Exportar Dados")
col1, col2 = st.columns(2)
if not st.session_state.dados.empty:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        st.session_state.dados.to_excel(writer, index=False, sheet_name='Gastos')
        pd.DataFrame([{
            'Salário': st.session_state.salario,
            'Total Gasto': total_gasto,
            'Saldo Restante': saldo_restante
        }]).to_excel(writer, index=False, sheet_name='Resumo')
    output.seek(0)
    col2.download_button(
        label="Baixar como Excel",
        data=output,
        file_name="controle_gastos_com_virgula.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    col2.write("Nenhum dado para exportar ainda.")
