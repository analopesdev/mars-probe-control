import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from src.database import init_db
from src.schema import Direction
from src.service import ProbeService

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Probe API", description="API for the probe", lifespan=lifespan)
probe_service = ProbeService()

@app.post("/probes")
def launch_probe(grid_max_x: int, grid_max_y: int, direction: Direction):
    try:
        result = probe_service.launch_probe(grid_max_x, grid_max_y, direction)
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Probe launched successfully", "data": result}

@app.put("/probes/{id}/move")
def move_probe(id: str, commands: list[str]):
    try:
        result = probe_service.move_probe(id, commands)
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Posição inválida: {e}")
    if result is None:
        raise HTTPException(status_code=404, detail="Probe not found")
    return {"message": "Probe moved successfully", "data": result.model_dump()}

@app.get("/probes")
def list_probes():
    return probe_service.list_probes().model_dump()
