import pygame
import pytest


@pytest.mark.parametrize(
    "frameList, frame, frameTimer, expected_frame, expected_frameTimer",
    [
        ([0, 1, 2, 1], 0, 0, 0, 1),
        ([0, 1, 2, 1], 0, 12, 1, 0),
        ([0, 1, 2, 1], 0, 15, 1, 0),
        ([0, 1, 2, 1], 3, 12, 0, 0),
        ([0, 1, 2, 1], 8, 12, 0, 0),
        ([0, 1, 2, 1], 15, 0, 15, 1),
    ],
)
def test_frameTimerMethod(prey_fixture, frameList, expected_frame, frame,
                          frameTimer, expected_frameTimer):
    prey_fixture.frameTimer = frameTimer
    prey_fixture.frame = frame
    prey_fixture.frameTimerMethod(frameList)

    assert prey_fixture.frame == expected_frame and \
        prey_fixture.frameTimer == expected_frameTimer


@pytest.mark.parametrize(
    (
        "tileset_width",
        "tileset_height",
        "tile_width",
        "tile_height",
        "expected_tileset_len"
    ),
    [
        (64, 64, 32, 32, 2),
        (462, 435, 154, 145, 3),
        (8, 4, 1, 1, 8),  # 8 columns and 4 rows; tileset[column][row]
    ],
)
def test_load_tileset(monkeypatch, prey_fixture, tileset_width, tileset_height,
                      tile_width, tile_height, expected_tileset_len):
    mock_image = pygame.Surface((tileset_width, tileset_height))

    monkeypatch.setattr(pygame.image, 'load', lambda _: mock_image)

    tileset = prey_fixture.load_tileset(
        'mocked_filename', tile_width, tile_height)

    assert isinstance(tileset, list) and \
        isinstance(tileset[0][0], pygame.Surface) and \
        tileset[0][0].get_size() == (tile_width, tile_height)
    assert len(tileset) == expected_tileset_len  # tileset_width // tile_width
