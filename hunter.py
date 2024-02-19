import pygame
from random import choice
from constants import SCREEN
from object import Object
class Hunter(Object):
    animationFramerate = 12
    defaultX = 400
    defaultY = 590
    catchFrame = 0
    laughFrames = [1, 2]
    
    def __init__(self, width, height, tileset):
        super().__init__(self.defaultX, self.defaultY, width, height, None)
        self.tileset = self.load_tileset(tileset, width, height)
        self.flipX = choice([True,False])
        self.frame = 0
        self.frame_timer = 0
        self.velocity = [0, 0]
        self.going_down = False
        
    def update(self, state):
        self.velocity[1] = 2
        self.draw(state)
        yTemp = self.y

        if self.y <= (self.defaultY-100):
            self.going_down = True 

        elif self.y > yTemp:  
            self.going_down = False
              

        if self.going_down:
            self.y += self.velocity[1]  
        else:
            self.y -= self.velocity[1]  
        
    def load_tileset(self, filename, width, height):
        
        image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = image.get_size()    
        tileset = []
        line = []  
        for tile_x in range(0, image_width // width):
            rect = (tile_x * width, 0, width, height) 
            line.append(image.subsurface(rect)) 
        tileset.append(line)  
        return tileset
  
    
    def draw(self, state):
        if state == "catch":
            image = pygame.transform.scale(self.tileset[0][self.catchFrame], (self.width, self.height))
            SCREEN.blit(pygame.transform.flip(image, self.flipX, False), (self.x, self.y))
            
        if state == "laughing": 
            if self.frame >= len(self.laughFrames):
                self.frame = 0

            image_index = self.laughFrames[self.frame]  
            image = pygame.transform.scale(self.tileset[0][image_index], (self.width, self.height))
            SCREEN.blit(pygame.transform.flip(image, self.flipX, False), (self.x, self.y))

            self.frame_timer += 1
            if self.frame_timer < self.animationFramerate:
                return
            self.frame += 1
            if self.frame >= len(self.laughFrames):
                self.frame = 0
            self.frame_timer = 0  
                
    def initialState(self):
        self.x = self.defaultX
        self.y = self.defaultY
        self.flipX = choice([True,False])
        self.frame = 0
        self.frame_timer = 0
        self.going_down = False