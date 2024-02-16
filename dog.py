import pygame
from random import randint, choice
from constants import BOUNDS_X, BOUNDS_Y, SCREEN, WIDTH
from object import Object

class Pray(Object):
    
    def __init__(self, x, y, width, height, tileset, direction=1):
        super().__init__(x, y, width, height, None)
        self.tileset = self.load_tileset(tileset, width, height)
        self.direction = direction
        self.flipX = False
        self.frame = 0
        self.frames = [0, 1, 2, 1]
        self.frame_timer = 0
        self.velocity = [0, 0]
        
    def update(self):
        self.move()
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()
    
    
    