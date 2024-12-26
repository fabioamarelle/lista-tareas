import streamlit as st
import uvicorn, requests
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import nest_asyncio

nest_asyncio.apply()

app = FastAPI()

class Tarea(BaseModel):
    id: int
    titulo: str
    descripcion: str

tareas = []

@app.get("/tareas")
async def obtener_tareas():
    return tareas

@app.post("/tareas")
async def agregar_tarea(tarea: Tarea):
    tareas.append(tarea)
    return tarea

def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

import threading
thread = threading.Thread(target=start_fastapi, daemon=True)
thread.start()

# Título
st.title("Lista de Tareas")

# Cargar tareas
if st.button("Cargar Tareas"):
    response = requests.get("http://127.0.0.1:8000/tareas")
    if response.status_code == 200:
        tareas = response.json()
        st.write(tareas)
    else:
        st.error("Error al cargar las tareas")

# Crear tareas
titulo = st.text_input("Título de la tarea")
descripcion = st.text_input("Descripción de la tarea")

if st.button("Agregar tarea"):
    if titulo and descripcion:
        tarea = {"id": len(tareas) + 1, "titulo": titulo, "descripcion": descripcion}
        response = requests.post("http://127.0.0.1:8000/tareas", json=tarea)
        if response.status_code == 200:
            st.success("Tarea agregada con éxito")
        else:
            st.error("Error al agregar tarea")
    else:
        st.error("Por favor, complete todos los campos")
