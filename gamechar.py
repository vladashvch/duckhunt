import pygame
from constants import SCREEN
from abc import ABC, abstractmethod
from gameobj import GameObj

class GameChar(ABC, GameObj):
    """
    An abstract class for game characters classes, that have velocity.

    Methods:
        update(): Updates the character's position based on its velocity. Use for basic movement. An abstract method.
        load_tileset(filename, width, height): Loads the tileset from the given file.
    """
    @abstractmethod
    def update(self):
        """Updates the character's position based on its velocity and draws."""
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()
    
    def load_tileset(self, filename, width, height):
        """
        Loads the tileset from the given file.
        Args:
            filename (str): The name of the image file to be loaded as a tileset.
            width (int): The number of pixels across each tile in the tileset.
            height (int): The number of pixels down each tile is in the tileset.
        Returns:
            list: A list of pygame Surface objects representing all the images in the tileset
        """
        image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = image.get_size()    
        tileset = []
        for tile_x in range(0, image_width // width):
            line = []
            tileset.append(line)
            for tile_y in range(0, image_height // height):
                rect = ( tile_x * width, tile_y * height, width, height)
                line.append(image.subsurface(rect))
        return tileset
    
    @abstractmethod
    def draw(self):
        image = pygame.transform.scale(self.tileset[self.moveFrameOrder[self.frame]][self.direction], (self.width, self.height))
        SCREEN.blit(pygame.transform.flip(image, self.flipX, self.flipY), (self.x, self.y))
