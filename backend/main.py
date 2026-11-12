import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from exceptions import (
    InvalidCommandError,
    InvalidGridError,
    OutOfGridError,
    ProbeNotFoundError,
)
from database import init_db
from controllers.probe_controller import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Probe API", description="API for the probe", lifespan=lifespan)
# Origens extras (ex.: a URL do front no Render), separadas por vírgula.
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)


def _error_handler(status_code: int):
    async def handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"detail": str(exc)})

    return handler


app.add_exception_handler(ProbeNotFoundError, _error_handler(404))
app.add_exception_handler(InvalidCommandError, _error_handler(422))
app.add_exception_handler(OutOfGridError, _error_handler(422))
app.add_exception_handler(InvalidGridError, _error_handler(422))
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
