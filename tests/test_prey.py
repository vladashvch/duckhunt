
import pytest


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
