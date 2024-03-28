import pytest
import pygame
from Main import bulletsUI, handle_user_events, SCREEN, FONT
from constants import PREY_MAX_COUNT, WIN_PREY_COUNT, PREY_ORIGINAL, CURSOR
from prey import Prey
from gameobj import GameObj
from random import randint


# ----------bulletsUI----------
@pytest.mark.parametrize("bulletsCount", [0, 1, 5, 10])
def test_bulletsUI(bulletsCount, monkeypatch):

    def mock_renderText(screen, font, text, size, color, position):
        mock_renderText.called = True
        mock_renderText.args = (screen, font, text, size, color, position)

    mock_renderText.called = False

    monkeypatch.setattr("Main.renderText", mock_renderText)

    bulletsUI(bulletsCount)

    expected_text = "R = " + str(bulletsCount)
    assert mock_renderText.called
    args = mock_renderText.args
    assert args[0:] == (SCREEN, FONT, expected_text, 25, "White", (135, 790))


# ----------handle_user_events----------
class MockEvent:
    def __init__(self, type, button=None):
        self.type = type
        self.button = button


@pytest.fixture
def mock_pygame_event_quit(monkeypatch):
    monkeypatch.setattr("pygame.event.get", pygame_event_get)


def pygame_event_get():
    event = MockEvent(pygame.QUIT)
    return [event]


@pytest.fixture
def mock_prey_objects():
    prey_objects = []
    for _ in range(PREY_MAX_COUNT):
        prey_object = Prey(-50, randint(200, 550),
                           154, 145, PREY_ORIGINAL, 100)
        prey_objects.append(prey_object)
    return prey_objects


@pytest.fixture
def mock_cursor_object():
    targetCursor = GameObj(0, 0, 50, 50, CURSOR)
    return targetCursor


@pytest.mark.parametrize(
    "bulletsMaxCount, bulletsCount, score, preyScore, "
    "preyDefeatCount",
    [
        (0, 20, 200, 9, [True] * PREY_MAX_COUNT),
        (0, 20, 200, 2, [True] * PREY_MAX_COUNT),
        (0, 20, 200, 8, [True] * PREY_MAX_COUNT),
        (0, 20, 200, 10, [True] * PREY_MAX_COUNT),
        (0, 20, 200, 5, [True] * PREY_MAX_COUNT),
        (0, 20, 200, 7, [True] * PREY_MAX_COUNT),
    ]
)
def test_handle_user_events_win(mock_pygame_event_quit,
                                mock_prey_objects, mock_cursor_object,
                                bulletsMaxCount, bulletsCount, score,
                                preyScore, preyDefeatCount):
    result = handle_user_events(bulletsMaxCount, 20, bulletsCount,
                                mock_prey_objects[0], mock_cursor_object,
                                score, preyScore, preyDefeatCount)

    if preyDefeatCount.count(True) >= WIN_PREY_COUNT:
        assert result[3] is False
    elif preyDefeatCount.count(True) < WIN_PREY_COUNT:
        assert result[3] is False
    else:
        assert result[3] is True
