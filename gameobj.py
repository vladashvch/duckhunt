import pygame
from constants import SCREEN


class GameObj():
    """
    A class used to represent a game object.

    Methods:
        getCenter(): Returns the center of the object.
        draw(): Draws the object on the screen, based on values given to
        object when created it.
    """
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

    def getCenter(self):
        """
        finds the center of an object use for objects collisions

        return: tuple (center_x, center_y)
        """
        return self.x + self.width / 2, self.y + self.height / 2

    def draw(self):
        """
        Draws the object on the screen, based on values given to object when
        created it. Rescaling image to object's width and height.
        """
        SCREEN.blit(
            pygame.transform.scale(self.image, (self.width, self.height)),
            (self.x, self.y))
