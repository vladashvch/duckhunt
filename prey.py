import pygame
from random import randint, choice
from constants import BOUNDS_X, BOUNDS_Y, SCREEN, WIDTH, CHARANIMATIONFPS
from gamechar import GameChar
class Prey(GameChar):
    minVelocity = 4
    maxVelocity = 6
    horizontalFlyRow = 1 #row in tileset
    upFlyRow = 0
    moveFrameOrder = [0, 1, 2, 1]
    
    def __init__(self, x, y, width, height, tileset, killPrice, direction=1):
        super().__init__(x, y, width, height, None)
        self.tileset = self.load_tileset(tileset, width, height)
        self.direction = direction
        self.flipX = False
        self.frame = 0
        self.frameTimer = 0
        self.velocity = [0, 0]
        self.gooseFallChoice = choice([1,2])
        self.alive = True
        self.killPrice = killPrice
        
        
    def update(self):
        """
        Updates the prey's random position and draws it, pray's default movement while hunting.
        """
        self.move()
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()
    
    def draw(self):
        """
        Draws the prey on the screen based on direction. 
        
        Contains logic for frame by frame tiles changing.
        """
        image = pygame.transform.scale(self.tileset[self.moveFrameOrder[self.frame]][self.direction], (self.width, self.height))
        self.change_direction()
        SCREEN.blit(pygame.transform.flip(image,  self.flipX, False), (self.x, self.y))

        self.frameTimer += 1
        if self.frameTimer < CHARANIMATIONFPS:
            return     
        self.frame += 1
        if self.frame >= len(self.moveFrameOrder):
            self.frame = 0
        self.frameTimer = 0

    def change_direction(self):
        """
        Changes the direction of the prey based on its velocity.

        Contains logic for changing line of tileset and flipping by X-axis the image based on the velocity positive or negative value.
        """
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
        """
        Updates the prey's velocity, pray's default movement while hunting.
        
        Contains logic for changing prey's direction and x,y coordinate of the GameObj if any coordinate of pray is less than screen bounds or greater than screen bounds
        """
        # Changing the value if speed_x and speed_y both are zero
        if self.velocity == [0, 0]:
            self.velocity = [randint(self.minVelocity, self.maxVelocity) * self.direction, randint(self.minVelocity, self.maxVelocity) * self.direction]
        # Changing the direction and x,y coordinate of the GameObj if the coordinate of left side is less..or right side coordinate is greater..
        if self.x <= BOUNDS_X[0] or self.x + self.width >= BOUNDS_X[1]:
            self.moveDirection = -1 if self.x + self.width >= BOUNDS_X[1] else 1
            self.velocity[0] = choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.moveDirection
            self.velocity[1] = choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.moveDirection
        
        # Changing the direction and x,y coordinate of the GameObj if the coordinate of top side is less.. or bottom side coordinate is greater..
        if self.y <= BOUNDS_Y[0] or self.y + self.height >= BOUNDS_Y[1]:
            self.moveDirection = -1 if self.y + self.height >= BOUNDS_Y[1] else 1
            self.velocity[0] = choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.moveDirection
            self.velocity[1] = choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.moveDirection

    def dying(self):
        """
        Animates the prey's death and falling down from the screen.

        Prey has death animation 2 seconds, it's 2 cycles, and then goes down by value.
        """
        if self.frameTimer < CHARANIMATIONFPS*2: # 2 cycles
            SCREEN.blit(pygame.transform.scale(self.tileset[0][2], (self.width, self.height)), (self.x, self.y))
            self.frameTimer += 1
            self.y -= 0.5
            return
        
        self.y += 8
        SCREEN.blit(pygame.transform.scale(self.tileset[self.gooseFallChoice][2], (self.width, self.height)), (self.x, self.y))

    def flyAway(self):
        """
        Makes the prey fly away from the screen.

        Prey changes its position on screen diagonaly-up with given value to the left or right side depending on the side of the screen.
        """
        if self.x > WIDTH/2:
            self.velocity = [self.maxVelocity, -self.maxVelocity]
        else:
            self.velocity = [-self.maxVelocity, -self.maxVelocity]
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()
    
    def start(self):
        """
        Makes the prey fly on its start point before hunting.

        Prey moves diagonaly-up with given value to the right side
        """
        self.velocity = [8, -8]
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()








    
