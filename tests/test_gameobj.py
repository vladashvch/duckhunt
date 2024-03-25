import pytest
from gameobj import GameObj


@pytest.fixture
def game_obj(request):
    x, y, width, height = request.param
    return GameObj(x, y, width, height, "")


@pytest.mark.parametrize(
    "game_obj, expected_center",
    [
        ((0, 0, 50, 50), (25, 25)),
        ((10, 20, 30, 40), (25, 40)),
        ((100, 100, 30, 30), (115, 115)),
        ((-10, -10, 60, 60), (20, 20)),
        ((0, 0, 100, 100), (50, 50)),
        ((-50, -50, 100, 100), (0, 0)),
        ((50, 50, 0, 0), (50, 50)),
        ((0, 0, 0, 0), (0, 0)),
    ],
    indirect=["game_obj"]
)
def test_getCenter(game_obj, expected_center):
    center = game_obj.getCenter()
    assert center == expected_center
    