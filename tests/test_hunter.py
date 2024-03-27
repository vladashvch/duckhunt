import pytest
import pygame
from hunter import Hunter
from constants import HUNTER_ORIGINAL, SCREEN


@pytest.fixture
def hunter():
    return Hunter(0, 0, 32, 32, HUNTER_ORIGINAL, 10) 


@pytest.mark.parametrize("heighPlus, expected_going_down",[
    (700, False),  
    (100, True), 
    (10, True),  
])
def test_update_goingDown_start(hunter, heighPlus, expected_going_down):
    hunter.heighPlus = heighPlus  
    hunter.update(None) 
    assert hunter.goingDown == expected_going_down

