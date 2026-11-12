from fastapi import APIRouter

from controllers.probe_controller import ProbeController
from models.schema import LaunchProbeRequest, MoveProbeRequest, ProbeListResponse, ProbeResponse

router = APIRouter()
controller = ProbeController()


@router.post("/probes", response_model=ProbeResponse)
def launch_probe(body: LaunchProbeRequest):
    return controller.launch_probe(body)


@router.post("/probes/{id}/commands", response_model=ProbeResponse)
def move_probe(id: str, body: MoveProbeRequest):
    return controller.move_probe(id, body)


@router.get("/probes", response_model=ProbeListResponse)
def list_probes():
    return controller.list_probes()
