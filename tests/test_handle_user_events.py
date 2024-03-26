import pygame
import pytest
from Main import handle_user_events
from constants import PREY_MAX_COUNT, WIN_PREY_COUNT
from prey import Prey
from gameobj import GameObj
from random import randint


class MockEvent:
    def __init__(self, type, button=None):
        self.type = type
        self.button = button


def pygame_event_get():
    event = MockEvent(pygame.QUIT)
    return [event]


@pytest.fixture
def mock_pygame_event_quit(monkeypatch):
    monkeypatch.setattr(pygame.event, "get", pygame_event_get)


@pytest.fixture
def mock_prey_objects():
    prey_objects = []
    preyTilesetPath = "assets/ordinar_goose_tileset.png"
    for _ in range(PREY_MAX_COUNT):
        prey_object = Prey(-50, randint(200, 550),
                           154, 145, preyTilesetPath, 100)
        prey_objects.append(prey_object)
    return prey_objects


@pytest.fixture
def mock_cursor_object():
    CURSOR = pygame.image.load("assets/cursor.png")
    targetCursor = GameObj(0, 0, 50, 50, CURSOR)
    return targetCursor


@pytest.mark.parametrize(
    "bulletsMaxCount, bulletsCount, score, preyScore, "
    "preyDefeatCount, expected_result",
    [
        (0, 20, 200, 9, [True] * PREY_MAX_COUNT, True),
        (0, 20, 200, 2, [True] * PREY_MAX_COUNT, True),
        (0, 20, 200, 8, [True] * PREY_MAX_COUNT, True),
        (0, 20, 200, 10, [True] * PREY_MAX_COUNT, True),
        (0, 20, 200, 5, [True] * PREY_MAX_COUNT, True),
        (0, 20, 200, 7, [True] * PREY_MAX_COUNT, True),
    ]
)
def test_handle_user_events_win(mock_pygame_event_quit,
                                mock_prey_objects, mock_cursor_object,
                                bulletsMaxCount, bulletsCount, score,
                                preyScore, preyDefeatCount, expected_result):
    handle_user_events(bulletsMaxCount, 20, bulletsCount,
                       mock_prey_objects[0], mock_cursor_object,
                       score, preyScore, preyDefeatCount)

    assert (len(preyDefeatCount) == PREY_MAX_COUNT
            and preyDefeatCount.count(True) >= WIN_PREY_COUNT) or \
           (len(preyDefeatCount) == PREY_MAX_COUNT
            and preyDefeatCount.count(True) < WIN_PREY_COUNT)
