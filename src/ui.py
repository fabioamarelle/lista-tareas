import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/tareas"

st.title("Gestión de Tareas")

# Crear nueva tarea
with st.form("crear_tarea"):
    titulo = st.text_input("Título", max_chars=50)
    descripcion = st.text_area("Descripción", max_chars=140)
    if st.form_submit_button("Crear Tarea"):
        response = requests.post(API_URL, json={"titulo": titulo, "descripcion": descripcion})
        if response.status_code == 201:
            st.success("Tarea creada")
        else:
            st.error("Error al crear tarea")

# Listar tareas
st.subheader("Tareas existentes")
response = requests.get(API_URL)
if response.status_code == 200:
    tareas = response.json()
    for tarea in tareas:
        st.text(f"{tarea['titulo']}") 
        st.text(f"{tarea['descripcion']}") 
        if st.button(f"Eliminar {tarea['titulo']}"):
            requests.delete(f"{API_URL}/{tarea['id']}")
            st.rerun()
