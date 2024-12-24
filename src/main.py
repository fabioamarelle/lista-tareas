from fastapi import FastAPI
app = FastAPI()

tareas = []
@app.get("/tareas")
def listar():
    return tareas