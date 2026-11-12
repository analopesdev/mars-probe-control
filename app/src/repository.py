import sqlite3

from src.database import DATABASE_PATH
from src.schema import CreateProbe, Probe, UpdateProbe

class ProbeRepository:
    def __init__(self, database_path: str = DATABASE_PATH):
        self.conn = sqlite3.connect(database_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def insert_probe(self, new_probe: CreateProbe) -> Probe:
        with self.conn:
            self.conn.execute(
                "INSERT INTO probes (id, position_x, position_y, direction, grid_max_x, grid_max_y) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    new_probe.id,
                    new_probe.position_x,
                    new_probe.position_y,
                    new_probe.direction.value,
                    new_probe.grid_max_x,
                    new_probe.grid_max_y,
                ),
            )
        return self.get_probe(new_probe.id)

    def update_probe(self, id: str, update_probe: UpdateProbe) -> Probe | None:
        with self.conn:
            self.conn.execute(
                "UPDATE probes SET position_x = ?, position_y = ?, direction = ? WHERE id = ?",
                (
                    update_probe.position_x,
                    update_probe.position_y,
                    update_probe.direction.value,
                    id,
                ),
            )
        return self.get_probe(id)

    def list_probes(self) -> list[Probe]:
        rows = self.conn.execute("SELECT * FROM probes").fetchall()
        return [Probe(**dict(row)) for row in rows]

    def get_probe(self, probe_id: str) -> Probe | None:
        row = self.conn.execute("SELECT * FROM probes WHERE id = ?", (probe_id,)).fetchone()
        return Probe(**dict(row)) if row else None
