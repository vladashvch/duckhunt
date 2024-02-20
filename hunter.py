import pygame
from random import choice
from constants import SCREEN
from gamechar import GameChar
class Hunter(GameChar):
    animationFramerate = 12
    defaultX = 400
    defaultY = 590
    reactionLine = 0
    catchFrame = 0
    laughFrames = [1, 2]

    
    def __init__(self, x, y, width, height, tileset):
        super().__init__(x, y, width, height, None)
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
        
    def draw(self, state):
        if state == "catch":
            image = pygame.transform.scale(self.tileset[self.catchFrame][self.reactionLine], (self.width, self.height))
            SCREEN.blit(pygame.transform.flip(image, self.flipX, False), (self.x, self.y))
            
        if state == "laughing": 
            if self.frame >= len(self.laughFrames):
                self.frame = 0

            image = pygame.transform.scale(self.tileset[self.laughFrames[self.frame]][self.reactionLine], (self.width, self.height))
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