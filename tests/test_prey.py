import pytest
from constants import BOUNDS_X, BOUNDS_Y


#  horizontalFlyRow = 1  upFlyRow = 0
@pytest.mark.parametrize(
    (
        "horizontal_velocity",
        "vertical_velocity",
        "expected_direction",
        "expected_flipX",
    ),
    [
        (4, 6, 0, False),  # First condition
        (-4, -2, 0, True),  # Second condition
        (-1, 0, 1, True),  # Third condition
        (2, 0, 1, False),  # Fourth condition
        (0, 0, 1, False),  # Nothing changes, last or default direction
    ]
)
def test_change_direction(prey_fixture, horizontal_velocity, vertical_velocity,
                          expected_direction, expected_flipX):
    prey_fixture.velocity = [horizontal_velocity, vertical_velocity]

    prey_fixture.changeDirection()

    assert prey_fixture.direction == expected_direction
    assert prey_fixture.flipX == expected_flipX


# BOUNDS_X = (20, 990) BOUNDS_Y = (20, 600)
@pytest.mark.parametrize(
    "moveDirection, x, y, height, width, expected_moveDirection",
    [
        (-1, BOUNDS_X[0], 30, 10, 10, 1),  # x at lower bound
        (1, BOUNDS_X[1] - 50, 30, 50, 50, -1),  # x at upper bound
        (-1, 30, BOUNDS_Y[0], 30, 30, 1),  # y at lower bound
        (1, 30, BOUNDS_Y[1] - 10, 10, 10, -1),  # y at upper bound
        (1, 80, 80, 60, 50, 1),
    ]
)
def test_move_moveDirection(moveDirection, prey_fixture, x, y, height, width,
                            expected_moveDirection):
    prey_fixture.moveDirection = moveDirection
    prey_fixture.x = x
    prey_fixture.y = y
    prey_fixture.height = height
    prey_fixture.width = width

    prey_fixture.move()

    assert prey_fixture.moveDirection == expected_moveDirection
