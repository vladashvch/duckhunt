import os
import pytest
from constants import ASSETS_PATH
from prey import Prey


@pytest.fixture(autouse=True)
def prey_fixture():
    preyTilesetPath = os.path.join(ASSETS_PATH, "ordinar_goose_tileset.png")
    return Prey(0, 0, 10, 10, preyTilesetPath, 100)
