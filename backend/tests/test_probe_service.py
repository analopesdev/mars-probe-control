import pytest

from exceptions import (
    InvalidCommandError,
    InvalidGridError,
    OutOfGridError,
    ProbeNotFoundError,
)
from models.schema import Direction


def launch(service, x=5, y=5, direction="NORTH"):
    return service.launch_probe(x, y, direction)


def position(probe):
    return (probe.x, probe.y, probe.direction)


# ---------- Lançamento ----------

def test_launch_starts_at_origin_with_given_direction(service):
    probe = launch(service, direction="EAST")

    assert position(probe) == (0, 0, Direction.EAST)
    assert probe.id


def test_each_launch_gets_a_different_id(service):
    assert launch(service).id != launch(service).id


@pytest.mark.parametrize("x, y", [(0, 5), (5, 0), (-1, 5), (5, -1)])
def test_launch_rejects_grid_size_zero_or_negative(service, x, y):
    with pytest.raises(InvalidGridError):
        launch(service, x=x, y=y)


# ---------- Movimento ----------

def test_example_from_the_challenge_MRM(service):
    probe = launch(service)

    moved = service.move_probe(probe.id, "MRM")

    assert position(moved) == (1, 1, Direction.EAST)


def test_move_forward_follows_the_direction(service):
    probe = launch(service)

    assert position(service.move_probe(probe.id, "MM")) == (0, 2, Direction.NORTH)


@pytest.mark.parametrize(
    "commands, expected",
    [
        ("R", Direction.EAST),
        ("RR", Direction.SOUTH),
        ("RRR", Direction.WEST),
        ("RRRR", Direction.NORTH),
        ("L", Direction.WEST),
        ("LL", Direction.SOUTH),
        ("LLL", Direction.EAST),
    ],
)
def test_turning_changes_direction_without_moving(service, commands, expected):
    probe = launch(service)

    assert position(service.move_probe(probe.id, commands)) == (0, 0, expected)


def test_commands_accumulate_across_requests(service):
    probe = launch(service)

    service.move_probe(probe.id, "M")
    moved = service.move_probe(probe.id, "RM")

    assert position(moved) == (1, 1, Direction.EAST)


def test_empty_sequence_keeps_the_probe_where_it_is(service):
    probe = launch(service)

    assert position(service.move_probe(probe.id, "")) == (0, 0, Direction.NORTH)


# ---------- Limites da malha ----------

def test_grid_limit_is_inclusive(service):
    # Malha 2 x 2: a sonda pode chegar até (2, 2).
    probe = launch(service, x=2, y=2)

    moved = service.move_probe(probe.id, "MMRMM")

    assert position(moved) == (2, 2, Direction.EAST)


def test_probe_cannot_leave_through_the_south_edge(service):
    probe = launch(service, direction="SOUTH")

    with pytest.raises(OutOfGridError):
        service.move_probe(probe.id, "M")


def test_probe_cannot_leave_through_the_west_edge(service):
    probe = launch(service, direction="WEST")

    with pytest.raises(OutOfGridError):
        service.move_probe(probe.id, "M")


def test_probe_cannot_leave_through_the_north_edge(service):
    probe = launch(service, x=5, y=2)

    with pytest.raises(OutOfGridError):
        service.move_probe(probe.id, "MMM")


def test_probe_cannot_leave_through_the_east_edge(service):
    probe = launch(service, x=2, y=5, direction="EAST")

    with pytest.raises(OutOfGridError):
        service.move_probe(probe.id, "MMM")


# ---------- Tudo ou nada ----------

def test_sequence_that_leaves_the_grid_is_not_applied_at_all(service):
    probe = launch(service, x=2, y=2)

    # Os dois primeiros M são válidos, o terceiro derrubaria a sonda.
    with pytest.raises(OutOfGridError):
        service.move_probe(probe.id, "MMM")

    assert position(service.list_probes()[0]) == (0, 0, Direction.NORTH)


def test_sequence_with_invalid_command_is_not_applied_at_all(service):
    probe = launch(service)

    with pytest.raises(InvalidCommandError):
        service.move_probe(probe.id, "MMXM")

    assert position(service.list_probes()[0]) == (0, 0, Direction.NORTH)


@pytest.mark.parametrize("commands", ["X", "m", "MRX", "M R", "123"])
def test_only_upper_case_M_L_R_are_valid_commands(service, commands):
    probe = launch(service)

    with pytest.raises(InvalidCommandError):
        service.move_probe(probe.id, commands)


# ---------- Sonda inexistente e listagem ----------

def test_move_unknown_probe(service):
    with pytest.raises(ProbeNotFoundError):
        service.move_probe("does-not-exist", "M")


def test_list_is_empty_at_first(service):
    assert service.list_probes() == []


def test_list_returns_every_probe_with_its_current_state(service):
    first = launch(service)
    second = launch(service, direction="WEST")
    service.move_probe(first.id, "MM")

    probes = {probe.id: position(probe) for probe in service.list_probes()}

    assert probes == {
        first.id: (0, 2, Direction.NORTH),
        second.id: (0, 0, Direction.WEST),
    }
