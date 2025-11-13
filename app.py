import streamlit as st
import pandas as pd
import pyodbc

# ---------------------------
# CONFIGURAÇÃO DA CONEXÃO
# ---------------------------
def get_connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost;'          # Altera para o seu server
        'DATABASE=TemporalDB;'       # Altera para o seu DB
        'Trusted_Connection=yes;'
    )
    return conn

# ---------------------------
# FUNÇÕES DE CONSULTA
# ---------------------------
def get_all_data():
    query = "SELECT * FROM Funcionarios FOR SYSTEM_TIME ALL ORDER BY SysStartTime"
    conn = get_connection()
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()

def get_current_data():
    query = "SELECT * FROM Funcionarios"
    conn = get_connection()
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()

def get_data_as_of(date_str):
    query = "SELECT * FROM Funcionarios FOR SYSTEM_TIME AS OF ?"
    conn = get_connection()
    try:
        return pd.read_sql(query, conn, params=(date_str,))
    finally:
        conn.close()

# ---------------------------
# INTERFACE STREAMLIT
# ---------------------------
st.set_page_config(page_title="Base de Dados Temporais", layout="wide")
st.title("Visualização de Base de Dados Temporais (SQL Server)")

st.sidebar.header("Opções de Consulta")
mode = st.sidebar.radio("Escolha o tipo de consulta:",
                        ("Dados atuais", "Histórico completo", "Consultar por data específica"))

if mode == "Consultar por data específica":
    selected_date = st.sidebar.date_input("Escolha a data")
    selected_time = st.sidebar.time_input("Hora", value=pd.Timestamp.now().time())
    datetime_str = f"{selected_date}T{selected_time}"
    st.write(f"Consultando registros válidos em: **{datetime_str}**")
    df = get_data_as_of(datetime_str)

elif mode == "Histórico completo":
    st.write("Mostrando histórico completo da tabela temporal")
    df = get_all_data()

else:
    st.write("Mostrando estado atual dos dados")
    df = get_current_data()

# ---------------------------
# MOSTRAR RESULTADOS
# ---------------------------
if df.empty:
    st.warning("Nenhum dado encontrado para esta consulta.")
else:
    st.dataframe(df, use_container_width=True)
    st.success(f"{len(df)} registos encontrados ✅")
