import pytest
from constants import PREY_ORIGINAL
from prey import Prey


@pytest.fixture(autouse=True)
def prey_fixture():
    return Prey(0, 0, 10, 10, PREY_ORIGINAL, 100)
