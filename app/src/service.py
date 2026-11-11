import uuid

from src.repository import ProbeRepository
from src.schema import CreateProbe, CreateProbResponse, MoveProbeResponse
from src.schema import Direction

direction_to_move = {
    "SOUTH": (-1, 0),
    "EAST": (0, 1),
    "NORTH": (1, 0),
    "WEST": (0, -1)
}

class ProbeService:
    def __init__(self):
        self.probe_repository = ProbeRepository()

    def launch_probe(self, grid_max_x: int, grid_max_y: int, direction_grid: str):
        direction = Direction(direction_grid)

        if grid_max_x <= 0 or grid_max_y <= 0:
            raise ValueError("Grid size must be greater than 0")

        if direction not in Direction.values():
            raise ValueError("Invalid direction")

        new_probe = CreateProbe(
                        id=str(uuid.uuid4()), 
                        position_x=0, 
                        position_y=0, 
                        grid_max_x=grid_max_x, 
                        grid_max_y=grid_max_y, 
                        direction=direction_grid
                    )

        probe_created = self.probe_repository.insert_probe(new_probe)

        create_probe_response = CreateProbResponse(id=probe_created.id, probe_pos_x=0, probe_pos_y=0, probe_direction=direction_grid)

        return create_probe_response.model_dump()

    def move_probe(self, probe_id: str, commands: list[str]):
        probe = self.probe_repository.get_probe(probe_id)

        if probe is None:
            raise ValueError(f"Probe with id {probe_id} not found")

        grid_max_x = probe.grid_max_x
        grid_max_y = probe.grid_max_y
        direction = Direction(probe.direction)

        x = probe.position_x
        y = probe.position_y

        self.validate_command(commands)

        for command in commands:
            match command:
                case "M":
                    forward_x, forward_y = direction_to_move[direction]

                    x = x + forward_x
                    y = y + forward_y

                    if grid_max_x < x or x < 0 or grid_max_y < y or y < 0:
                        raise ValueError("Probe cannot move out of the grid")

                case "R":
                    direction = direction.right()

                case "L":
                    direction = direction.left()
        
        probe.position_x = x
        probe.position_y = y
        probe.direction = direction
        
        self.probe_repository.update_probe(probe_id, probe)

        return MoveProbeResponse(x=x, y=y, direction=direction)

    def list_probes(self):
        return self.probe_repository.get_all_probes()

    def validate_command(self, commands: list[str]):
        for command in commands:
            if command not in ["M", "L", "R"]:
                raise ValueError(f"Invalid command: {command}")