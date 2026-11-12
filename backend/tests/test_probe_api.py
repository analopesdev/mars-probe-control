import pytest


def launch(client, x=5, y=5, direction="NORTH"):
    return client.post("/probes", json={"x": x, "y": y, "direction": direction})


def move(client, probe_id, commands):
    return client.post(f"/probes/{probe_id}/commands", json={"commands": commands})


# ---------- Lançar ----------

def test_launch_returns_id_and_initial_position(client):
    response = launch(client, direction="NORTH")

    assert response.status_code == 200
    body = response.json()
    assert body["id"]
    assert (body["x"], body["y"], body["direction"]) == (0, 0, "NORTH")


@pytest.mark.parametrize("x, y", [(0, 5), (5, 0), (-3, 5)])
def test_launch_with_grid_size_zero_or_negative_returns_422(client, x, y):
    response = launch(client, x=x, y=y)

    assert response.status_code == 422
    assert "Grid size" in response.json()["detail"]


def test_launch_with_invalid_direction_returns_422(client):
    assert launch(client, direction="UP").status_code == 422


def test_launch_with_malformed_body_returns_422(client):
    assert client.post("/probes", json={"x": 5}).status_code == 422
    assert client.post("/probes", json={"x": "a", "y": 5, "direction": "NORTH"}).status_code == 422


# ---------- Mover ----------

def test_move_example_from_the_challenge(client):
    probe_id = launch(client).json()["id"]

    response = move(client, probe_id, "MRM")

    assert response.status_code == 200
    assert response.json() == {
        "id": probe_id, "x": 1, "y": 1, "direction": "EAST", "grid_max_x": 5, "grid_max_y": 5,
    }


def test_move_unknown_probe_returns_404(client):
    response = move(client, "does-not-exist", "M")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_move_with_invalid_command_returns_422_and_does_not_move(client):
    probe_id = launch(client).json()["id"]

    response = move(client, probe_id, "MMX")

    assert response.status_code == 422
    assert "Invalid command" in response.json()["detail"]
    probe = client.get("/probes").json()["probes"][0]
    assert (probe["x"], probe["y"]) == (0, 0)


def test_move_out_of_the_grid_returns_422_and_does_not_move(client):
    probe_id = launch(client, x=2, y=2).json()["id"]

    response = move(client, probe_id, "MMM")

    assert response.status_code == 422
    assert "out of the grid" in response.json()["detail"]
    probe = client.get("/probes").json()["probes"][0]
    assert (probe["x"], probe["y"]) == (0, 0)


def test_move_with_malformed_body_returns_422(client):
    probe_id = launch(client).json()["id"]

    assert client.post(f"/probes/{probe_id}/commands", json={}).status_code == 422


# ---------- Listar ----------

def test_list_is_empty_at_first(client):
    response = client.get("/probes")

    assert response.status_code == 200
    assert response.json() == {"probes": []}


def test_list_returns_all_probes_with_their_grid_size(client):
    first_id = launch(client).json()["id"]
    second_id = launch(client, direction="WEST").json()["id"]
    move(client, first_id, "MRM")

    response = client.get("/probes")

    assert response.status_code == 200
    assert response.json() == {
        "probes": [
            {"id": first_id, "x": 1, "y": 1, "direction": "EAST", "grid_max_x": 5, "grid_max_y": 5},
            {"id": second_id, "x": 0, "y": 0, "direction": "WEST", "grid_max_x": 5, "grid_max_y": 5},
        ]
    }
