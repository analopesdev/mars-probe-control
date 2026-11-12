from enum import StrEnum

from pydantic import BaseModel


class Direction(StrEnum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"

    def right(self) -> "Direction":
        order = list(Direction)
        return order[(order.index(self) + 1) % len(order)]

    def left(self) -> "Direction":
        order = list(Direction)
        return order[(order.index(self) - 1) % len(order)]


class Probe(BaseModel):
    id: str
    position_x: int
    position_y: int
    direction: Direction
    grid_max_x: int
    grid_max_y: int


class CreateProbe(BaseModel):
    id: str
    position_x: int
    position_y: int
    grid_max_x: int
    grid_max_y: int
    direction: Direction

class UpdateProbe(BaseModel):
    position_x: int
    position_y: int
    direction: Direction

class MoveProbeRequest(BaseModel):
    commands: str


class ProbeResponse(BaseModel):
    id: str
    x: int
    y: int
    direction: Direction

class ProbeListResponse(BaseModel):
    probes: list[ProbeResponse]
