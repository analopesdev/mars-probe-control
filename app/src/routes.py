from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.database import init_db
from src.exceptions import (
    InvalidCommandError,
    InvalidGridError,
    OutOfGridError,
    ProbeNotFoundError,
)
from src.repository import ProbeRepository
from src.schema import LaunchProbeRequest, MoveProbeRequest, ProbeListResponse, ProbeResponse
from src.service import ProbeService


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Probe API", description="API for the probe", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)
probe_service = ProbeService(ProbeRepository())


def _error_handler(status_code: int):
    async def handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"detail": str(exc)})

    return handler

app.add_exception_handler(ProbeNotFoundError, _error_handler(404))
app.add_exception_handler(InvalidCommandError, _error_handler(422))
app.add_exception_handler(OutOfGridError, _error_handler(422))
app.add_exception_handler(InvalidGridError, _error_handler(422))

@app.post("/probes", response_model=ProbeResponse)
def launch_probe(body: LaunchProbeRequest):
    return probe_service.launch_probe(body.x, body.y, body.direction)

@app.post("/probes/{id}/commands", response_model=ProbeResponse)
def move_probe(id: str, body: MoveProbeRequest):
    return probe_service.move_probe(id, body.commands)

@app.get("/probes", response_model=ProbeListResponse)
def list_probes():
    return ProbeListResponse(probes=probe_service.list_probes())
