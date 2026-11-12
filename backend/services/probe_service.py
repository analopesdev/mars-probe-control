import uuid

from exceptions import (
    InvalidCommandError,
    InvalidGridError,
    OutOfGridError,
    ProbeNotFoundError,
)
from models.schema import CreateProbe, Direction, Probe, ProbeResponse, UpdateProbe
from repositories.probe_repository import ProbeRepository

DIRECTION_TO_MOVE = {
    Direction.NORTH: (0, 1),
    Direction.SOUTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.WEST: (-1, 0),
}

VALID_COMMANDS = {"M", "L", "R"}


class ProbeService:
    def __init__(self, probe_repository: ProbeRepository):
        self.probe_repository = probe_repository

    def launch_probe(self, grid_max_x: int, grid_max_y: int, direction: str) -> ProbeResponse:
        if grid_max_x <= 0 or grid_max_y <= 0:
            raise InvalidGridError()

        new_probe = CreateProbe(
            id=str(uuid.uuid4()),
            position_x=0,
            position_y=0,
            grid_max_x=grid_max_x,
            grid_max_y=grid_max_y,
            direction=Direction(direction),
        )
        return self._to_response(self.probe_repository.insert_probe(new_probe))

    def move_probe(self, probe_id: str, commands: str) -> ProbeResponse:
        self._validate_commands(commands)

        probe = self.probe_repository.get_probe(probe_id)
        if probe is None:
            raise ProbeNotFoundError(probe_id)

        direction = probe.direction
        x, y = probe.position_x, probe.position_y

        for command in commands:
            if command == "M":
                dx, dy = DIRECTION_TO_MOVE[direction]
                next_x, next_y = x + dx, y + dy
                if not (0 <= next_x <= probe.grid_max_x and 0 <= next_y <= probe.grid_max_y):
                    raise OutOfGridError()
                x, y = next_x, next_y
            elif command == "L":
                direction = direction.left()
            elif command == "R":
                direction = direction.right()

        updated = self.probe_repository.update_probe(
            probe_id, UpdateProbe(position_x=x, position_y=y, direction=direction)
        )
        return self._to_response(updated)

    def list_probes(self) -> list[ProbeResponse]:
        return [self._to_response(probe) for probe in self.probe_repository.list_probes()]

    @staticmethod
    def _validate_commands(commands: str) -> None:
        for command in commands:
            if command not in VALID_COMMANDS:
                raise InvalidCommandError(command)

    @staticmethod
    def _to_response(probe: Probe) -> ProbeResponse:
        return ProbeResponse(
            id=probe.id,
            x=probe.position_x,
            y=probe.position_y,
            direction=probe.direction,
            grid_max_x=probe.grid_max_x,
            grid_max_y=probe.grid_max_y,
        )
