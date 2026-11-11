from typing import Literal

from pydantic import BaseModel

Direction = Literal["NORTH", "EAST", "SOUTH", "WEST"]


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

class CreateProbResponse(BaseModel):
    id: str
    probe_pos_x: int
    probe_pos_y: int
    probe_direction: Direction


class UpdateProbe(BaseModel):
    position_x: int
    position_y: int
    direction: Direction

class MoveProbeResponse(BaseModel):
    x: int
    y: int
    direction: Direction