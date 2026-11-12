from models.schema import LaunchProbeRequest, MoveProbeRequest, ProbeListResponse, ProbeResponse
from repositories.probe_repository import ProbeRepository
from services.probe_service import ProbeService


class ProbeController:
    def __init__(self, probe_service: ProbeService | None = None):
        self.probe_service = probe_service or ProbeService(ProbeRepository())

    def launch_probe(self, body: LaunchProbeRequest) -> ProbeResponse:
        return self.probe_service.launch_probe(body.x, body.y, body.direction)

    def move_probe(self, probe_id: str, body: MoveProbeRequest) -> ProbeResponse:
        return self.probe_service.move_probe(probe_id, body.commands)

    def list_probes(self) -> ProbeListResponse:
        return ProbeListResponse(probes=self.probe_service.list_probes())
