import pygame
from object import Object
from random import randint
import random
class Pray(Object):
    animationFramerate = 12
    minVelocity = 4
    maxVelocity = 8
    horizontalFlyRow = 1 #row in tileset
    upFlyRow = 0

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
    
    def draw(self):
        image = pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction], (self.width, self.height))
        self.change_direction()
        self.gameScreen.blit(pygame.transform.flip(image,  self.flipX, False), (self.x, self.y))

        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.frame = 0
            return
        
        self.frame_timer += 1

        if self.frame_timer < self.animationFramerate:
            return
        
        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0

        self.frame_timer = 0

    def change_direction(self):
        self.flipX = False
        self.direction =  self.horizontalFlyRow
        #logic depending on velocity to change direction
    
    def move(self):
        # Changing the value if speed_x and speed_y both are zero
        if self.velocity == [0, 0]:
            self.velocity = [randint(self.minVelocity, self.maxVelocity) * self.direction, randint(self.minVelocity, self.maxVelocity) * self.direction]
        # Changing the direction and x,y coordinate of the object if the coordinate of left side is less..or right side coordinate is greater..
        if self.x <= 20 or self.x + self.width >= 990:
            self.move_direction = -1 if self.x + self.width >= 990 else 1
            self.velocity[0] = random.choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.move_direction
            self.velocity[1] = random.choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.move_direction
        
        # Changing the direction and x,y coordinate of the object if the coordinate of top side is less.. or bottom side coordinate is greater..
        if self.y <= 20 or self.y + self.height >= 600:
            self.move_direction = -1 if self.y + self.height >= 600 else 1
            self.velocity[0] = random.choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.move_direction
            self.velocity[1] = random.choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.move_direction



    
