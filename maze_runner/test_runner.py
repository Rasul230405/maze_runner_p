from runner import (  # type: ignore
    create_runner,
    get_orientation,
    get_x,
    get_y,
    turn,
    forward,
)


def test_create_runner() -> None:
    """A Unit test for :func:runner.create_runner function"""
    runner = create_runner(1, 2, "S")
    assert get_x(runner) == 1
    assert get_y(runner) == 2
    assert get_orientation(runner) == "S"


def test_turn() -> None:
    """A Unit test for :func:runner.turn function"""
    runner = create_runner(1, 2, "S")
    runner = turn(runner, "Left")
    assert get_x(runner) == 1
    assert get_y(runner) == 2
    assert get_orientation(runner) == "E"


def test_forward() -> None:
    """A Unit test for :func:runner.forward function"""
    runner = create_runner(1, 2, "S")
    runner = forward(runner)
    assert get_x(runner) == 1
    assert get_y(runner) == 1
    assert get_orientation(runner) == "S"
