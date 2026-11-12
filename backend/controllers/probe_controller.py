from fastapi import APIRouter

from models.schema import LaunchProbeRequest, MoveProbeRequest, ProbeListResponse, ProbeResponse
from repositories.probe_repository import ProbeRepository
from services.probe_service import ProbeService

router = APIRouter()
probe_service = ProbeService(ProbeRepository())


@router.post("/probes", response_model=ProbeResponse)
def launch_probe(body: LaunchProbeRequest):
    return probe_service.launch_probe(body.x, body.y, body.direction)


@router.post("/probes/{id}/commands", response_model=ProbeResponse)
def move_probe(id: str, body: MoveProbeRequest):
    return probe_service.move_probe(id, body.commands)


@router.get("/probes", response_model=ProbeListResponse)
def list_probes():
    return ProbeListResponse(probes=probe_service.list_probes())
