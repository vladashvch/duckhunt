import pygame
from object import Object

class Pray(Object):
    def __init__(self, x, y, width, height, tileset, direction=1):
        super().__init__(x, y, width, height, None)
        self.tileset = self.load_tileset(tileset, width, height)
        self.direction = direction
        self.frame = 0
        self.frames = [0, 1, 2, 1]
        self.frame_timer = 0
        self.velocity = [0, 0]

    def load_tileset(self, filename, width, height):
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
