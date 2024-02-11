import pygame
from constants import SCREEN
from abc import ABC, abstractmethod
class Object(ABC):
    @abstractmethod
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.velocity = [0,0]

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()

    def draw(self):
        SCREEN.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))
    #for collisions when shooting prays with mouse
    def getCenter(self): 
        return self.x + self.width / 2, self.y + self.height / 2

