import pygame
from constants import SCREEN

class GameInit():

    def __init__(self, x, y, width, height, image):
            """
            Constructor for GameObj class.
            Args:
                x (int): The x-coordinate of the top left corner of the object.
                y (int): The y-coordinate of the top left corner of the object.
                width (int): The width of the object.
                height (int): The height of the object.
                image (str, pygame.Surface): The image path.
            """
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.image = image