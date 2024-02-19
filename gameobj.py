import pygame
from constants import SCREEN

class GameObj():
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
    
    #for collisions when shooting prays with mouse
    def getCenter(self): 
        return self.x + self.width / 2, self.y + self.height / 2
    
    def draw(self):
        SCREEN.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))

