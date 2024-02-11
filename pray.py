import pygame
from object import Object
from random import randint, choice
from constants import BOUNDS_X, BOUNDS_Y
class Pray(Object):
    alive = True
    killPrice = 100
    animationFramerate = 12
    minVelocity = 4
    maxVelocity = 8
    horizontalFlyRow = 1 #row in tileset
    upFlyRow = 0
    randomFall = choice([1,2])

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
        if self.velocity[0] >= 0 and not (0 <= self.velocity[1] <= self.minVelocity+1): #↑↓ →→
            self.direction = self.upFlyRow
        elif self.velocity[0] <= 0 and not (0 <= self.velocity[1] <= self.minVelocity+1): #↑↓ ←←
            self.direction = self.upFlyRow
            self.flipX = True
        elif self.velocity[0] < 0: #←
            self.direction =  self.horizontalFlyRow
            self.flipX = True
        elif self.velocity[0] > 0: #→
            self.direction = self.horizontalFlyRow
    
    def move(self):
        # Changing the value if speed_x and speed_y both are zero
        if self.velocity == [0, 0]:
            self.velocity = [randint(self.minVelocity, self.maxVelocity) * self.direction, randint(self.minVelocity, self.maxVelocity) * self.direction]
        # Changing the direction and x,y coordinate of the object if the coordinate of left side is less..or right side coordinate is greater..
        if self.x <= BOUNDS_X[0] or self.x + self.width >= BOUNDS_X[1]:
            self.move_direction = -1 if self.x + self.width >= BOUNDS_X[1] else 1
            self.velocity[0] = choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.move_direction
            self.velocity[1] = choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.move_direction
        
        # Changing the direction and x,y coordinate of the object if the coordinate of top side is less.. or bottom side coordinate is greater..
        if self.y <= BOUNDS_Y[0] or self.y + self.height >= BOUNDS_Y[1]:
            self.move_direction = -1 if self.y + self.height >= BOUNDS_Y[1] else 1
            self.velocity[0] = choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.move_direction
            self.velocity[1] = choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.move_direction

    def dying(self):
        if self.frame_timer < self.animationFramerate*2: # 2 cycles
            self.gameScreen.blit(pygame.transform.scale(self.tileset[0][2], (self.width, self.height)), (self.x, self.y))
            self.frame_timer += 1
            self.y -= 0.5
            return
        
        self.y += 8
        self.gameScreen.blit(pygame.transform.scale(self.tileset[self.randomFall][2], (self.width, self.height)), (self.x, self.y))

    def flyAway(self):
        if self.x > 1000/2:
            self.velocity = [8, -8]
        else:
            self.velocity = [-8, -8]
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()
    
    def start(self):
        self.velocity = [8, -8]
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()







    
