from fastapi import FastAPI
from pydantic import BaseModel, constr
from uuid import UUID, uuid4
from enum import Enum

app = FastAPI()

class EstadosPosibles(str, Enum):
    terminado = "Terminado"
    noterminado = "No terminado"

class TareaIntroducida(BaseModel):
    titulo: constr(min_length=3, max_length=50)     # type: ignore
    descripcion: constr(max_length=140)             # type: ignore
    estado: EstadosPosibles = EstadosPosibles.noterminado


class Tarea(TareaIntroducida):
    id: UUID

tareas = []
@app.get("/tareas")
def listar():
    return tareas

@app.post("/tareas", response_model=Tarea)
def crear(tarea: TareaIntroducida):
    tareaNueva = tarea.dict()
    tareaNueva.update({"id": uuid4()})
    tareas.append(tareaNueva)
    return tareaNueva

    