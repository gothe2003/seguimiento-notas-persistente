import streamlit as st
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# Cargar credenciales desde variable de entorno
google_credentials = json.loads(os.environ.get("GOOGLE_SERVICE_ACCOUNT"))

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_dict(google_credentials, scope)
client = gspread.authorize(creds)

# Abre la hoja de cálculo
sheet = client.open("Seguimiento Notas").sheet1

st.title("Sistema de Seguimiento Académico con Persistencia")

# Leer datos existentes
data = sheet.get_all_records()

# Mostrar datos actuales
if data:
    st.subheader("Datos actuales")
    st.write(data)
else:
    st.write("No hay datos aún.")

# Formulario para agregar datos
st.subheader("Agregar nuevo registro")
with st.form("form", clear_on_submit=True):
    ramo = st.text_input("Ramo:")
    evaluacion = st.text_input("Evaluación:")
    nota = st.number_input("Nota (10-70):", min_value=10, max_value=70)
    peso = st.number_input("Peso (%):", min_value=0, max_value=100)
    submitted = st.form_submit_button("Agregar")

    if submitted:
        sheet.append_row([ramo, evaluacion, nota, peso])
        st.success("Registro agregado correctamente.")
