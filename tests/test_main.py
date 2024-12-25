from fastapi.testclient import TestClient
from fastapi import status
from src.main import app, tareas    # importa de /src/main.py


def test_listar_tareas_devuelve_HTTP200OK():                 # El archivo y las funciones tienen que empezar por test
    cliente = TestClient(app)   
    respuesta = cliente.get("/tareas")                      # Pide la carpeta /tareas
    assert respuesta.status_code == status.HTTP_200_OK      # Se espera el código HTTP 200 OK
    
def test_listar_tareas_devuelve_JSON():
    cliente = TestClient(app)
    respuesta = cliente.get("/tareas")
    assert respuesta.headers["Content-Type"] == "application/json"

def test_listar_tareas_devuelve_lista():
    cliente = TestClient(app)
    respuesta = cliente.get("/tareas")
    assert isinstance(respuesta.json(), list)

def test_tarea_tiene_id_titulo_desc_estado():
    tareas.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "Título",
            "descripcion": "Descripción",
            "estado": "Finalizado",
        }
    )
    cliente = TestClient(app)
    respuesta = cliente.get("/tareas")
    assert "id" in respuesta.json()[0] and "titulo" in respuesta.json()[0] and "descripcion" in respuesta.json()[0] and "estado" in respuesta.json()[0]
    tareas.clear()
    
def test_tareas_acepta_comando_POST():
    cliente = TestClient(app)
    respuesta = cliente.post("/tareas")
    assert respuesta.status_code != status.HTTP_405_METHOD_NOT_ALLOWED
