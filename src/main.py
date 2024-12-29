import streamlit as st
import requests, uuid, threading, nest_asyncio, uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

nest_asyncio.apply()

# Crea la aplicación FastAPI
app = FastAPI()

class Tarea(BaseModel):
    id: int
    titulo: str
    descripcion: str

tareas_por_usuario = {}

# Rutas FastAPI
@app.get("/tareas/{user_id}")
async def obtener_tareas(user_id: str):
    return tareas_por_usuario.get(user_id, [])

@app.post("/tareas/{user_id}")
async def agregar_tarea(user_id: str, tarea: Tarea):
    if user_id not in tareas_por_usuario:
        tareas_por_usuario[user_id] = []
    tareas_por_usuario[user_id].append(tarea)
    return tarea

@app.delete("/tareas/{user_id}/{tarea_id}")
async def eliminar_tarea(user_id: str, tarea_id: int):
    if user_id in tareas_por_usuario:
        tareas_por_usuario[user_id] = [t for t in tareas_por_usuario[user_id] if t.id != tarea_id]
    return {"message": "Tarea eliminada"}

def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

thread = threading.Thread(target=start_fastapi, daemon=True)
thread.start()


def cargar_tareas():
    try:
        # Crea un ID de usuario
        user_id = st.session_state.get("user_id")
        if not user_id:
            user_id = str(uuid.uuid4())  
            st.session_state.user_id = user_id  # Guarda el ID de usuario en la sesión de Streamlit

        response = requests.get(f"http://127.0.0.1:8000/tareas/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al cargar las tareas. Código de respuesta: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error al intentar conectar con la API: {e}")
        return []


st.title("Lista de Tareas")

# Cargar tareas automáticamente al inicio para el usuario actual
tareas = cargar_tareas()

tareas_a_eliminar = []
for tarea in tareas:
    col1, col2 = st.columns([0.1, 0.9]) 
    with col1:
        eliminar = st.checkbox("", key=f"checkbox_{tarea['id']}")
        if eliminar:
            tareas_a_eliminar.append(tarea['id'])
    with col2:
        st.markdown(f"**{tarea['titulo']}**: {tarea['descripcion']}")

# Botón para eliminar las tareas seleccionadas
if st.button("Eliminar tareas seleccionadas") and tareas:
    for tarea_id in tareas_a_eliminar:
        response = requests.delete(f"http://127.0.0.1:8000/tareas/{st.session_state.user_id}/{tarea_id}")


    tareas = cargar_tareas()

# Crear una nueva tarea
titulo = st.text_input("Título")
descripcion = st.text_input("Descripción")

if st.button("Agregar tarea"):
    if titulo and descripcion:
        tarea = {"id": len(tareas) + 1, "titulo": titulo, "descripcion": descripcion}
        try:
            response = requests.post(f"http://127.0.0.1:8000/tareas/{st.session_state.user_id}", json=tarea)
            if response.status_code == 200:
                st.success("Tarea agregada con éxito")
                # Recargar las tareas después de agregar una nueva tarea
                tareas = cargar_tareas()
                st.rerun()
            else:
                st.error(f"Error al agregar tarea. Código de respuesta: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error al intentar conectar con la API: {e}")
    else:
        st.error("Por favor, complete todos los campos")
    
