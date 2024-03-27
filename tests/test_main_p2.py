import pytest
from Main import (preyCounter, PREY_ORIGINAL,
                  HUNTER_ORIGINAL, PREY_MAX_COUNT)
from prey import Prey
from hunter import Hunter
from random import randint


# ----------preyCounter----------
@pytest.fixture
def goose():
    return Prey(-50, randint(200, 550), 154, 145,
                PREY_ORIGINAL, 100)


@pytest.fixture
def dog():
    return Hunter(Hunter.defaultX, Hunter.defaultY,
                  200, 293, HUNTER_ORIGINAL, 200)


def test_preyCounter_goose_alive_false(goose, dog):
    goose.alive = False
    goose.y = 710
    preyCount = []
    for _ in range(PREY_MAX_COUNT):
        new_goose = Prey(-50, randint(200, 550), 154, 145, PREY_ORIGINAL, 100)
        preyCount.append(new_goose)
    preyCounter(0, None, preyCount, [], 3, 3, goose, dog)
    assert dog.state == "catch"


def test_preyCounter_bulletsCount_zero(goose, dog):
    preyCounter(0, 0, [], [], 0, 10, goose, dog)

    assert dog.state == "laughing"
