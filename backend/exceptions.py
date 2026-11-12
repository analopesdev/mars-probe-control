class ProbeError(Exception):
    """Base class for all probe errors."""


class ProbeNotFoundError(ProbeError):
    def __init__(self, probe_id: str):
        super().__init__(f"Probe with id {probe_id} not found")


class InvalidCommandError(ProbeError):
    def __init__(self, command: str):
        super().__init__(f"Invalid command: {command}")


class OutOfGridError(ProbeError):
    def __init__(self):
        super().__init__("Probe cannot move out of the grid")


class InvalidGridError(ProbeError):
    def __init__(self):
        super().__init__("Grid size must be greater than 0")
