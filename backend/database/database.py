import os
import sqlite3
from contextlib import closing

DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "probe.db"))

CREATE_PROBES_TABLE = """
CREATE TABLE IF NOT EXISTS probes (
    id          TEXT    NOT NULL PRIMARY KEY,
    position_x  INTEGER NOT NULL CHECK (position_x >= 0),
    position_y  INTEGER NOT NULL CHECK (position_y >= 0),
    direction   TEXT    NOT NULL CHECK (direction IN ('NORTH', 'EAST', 'SOUTH', 'WEST')),
    grid_max_x  INTEGER NOT NULL CHECK (grid_max_x >= 0),
    grid_max_y  INTEGER NOT NULL CHECK (grid_max_y >= 0),
    CHECK (position_x <= grid_max_x),
    CHECK (position_y <= grid_max_y)
)
"""


def init_db(database_path: str = DATABASE_PATH) -> None:
    with closing(sqlite3.connect(database_path)) as connection:
        with connection:
            connection.execute(CREATE_PROBES_TABLE)
