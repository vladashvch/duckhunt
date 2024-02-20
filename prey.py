import pygame
from random import randint, choice
from constants import BOUNDS_X, BOUNDS_Y, SCREEN, WIDTH, CHARANIMATIONFPS
from gamechar import GameChar
class Prey(GameChar):
    """
    Class for the prey object in the game. Inherits from abstract GameChar.

    Attributes:
        killPrice (int): The score value of the prey.
        minVelocity (int): The minimum velocity of the prey.
        maxVelocity (int): The maximum velocity of the prey.
        horizontalFlyRow (int): The row in the tileset for the horizontal flying animation.
        upFlyRow (int): The row in the tileset for the upward flying animation.
        moveFrameOrder (list): The order of the frames in the tileset for the flying animation.
        
    Methods:
        update(): Updates the prey's random-directioned position, pray's default movement while hunting.
        dying(): Animates the prey's death and falling down from the screen.
        flyAway(): Makes the prey fly away from the screen.
        start(): Makes the prey fly on its start point before hunting.
        draw(): Draws the prey on the screen based on direction.
        change_direction(): Changes the direction of the prey based on its velocity.
        move(): Moves the prey based on its velocity and changes velocity if it hits the screen bounds.
    """
    killPrice = 100
    minVelocity = 4
    maxVelocity = 6
    horizontalFlyRow = 1 #row in tileset
    upFlyRow = 0
    moveFrameOrder = [0, 1, 2, 1]
    
    def __init__(self, x, y, width, height, tileset, direction=1):
        """
        Constructor for Prey class.
        Args:
            x (int): The x-coordinate of the top left corner of the prey.
            y (int): The y-coordinate of the top left corner of the prey.
            width (int): The width of the prey.
            height (int): The height of the prey.
            tileset (str): The path to the tileset image for the prey.
            direction (int): The direction the prey is facing. 1 for right, -1 for left.
        """
        super().__init__(x, y, width, height, None)
        self.tileset = self.load_tileset(tileset, width, height)
        self.direction = direction
        self.flipX = False
        self.frame = 0
        self.frame_timer = 0
        self.velocity = [0, 0]
        self.gooseFallChoice = choice([1,2])
        self.alive = True
        
        
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

        self.frame_timer += 1

        if self.frame_timer < CHARANIMATIONFPS:
            return
        
        self.frame += 1
        if self.frame >= len(self.moveFrameOrder):
            self.frame = 0

        self.frame_timer = 0

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
            self.move_direction = -1 if self.x + self.width >= BOUNDS_X[1] else 1
            self.velocity[0] = choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.move_direction
            self.velocity[1] = choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.move_direction
        
        # Changing the direction and x,y coordinate of the GameObj if the coordinate of top side is less.. or bottom side coordinate is greater..
        if self.y <= BOUNDS_Y[0] or self.y + self.height >= BOUNDS_Y[1]:
            self.move_direction = -1 if self.y + self.height >= BOUNDS_Y[1] else 1
            self.velocity[0] = choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.move_direction
            self.velocity[1] = choice([0, randint(self.minVelocity, self.maxVelocity) ]) * self.move_direction

    def dying(self):
        """
        Animates the prey's death and falling down from the screen.

        Prey has death animation 2 seconds, it's 2 cycles, and then goes down by value.
        """
        if self.frame_timer < CHARANIMATIONFPS*2: # 2 cycles
            SCREEN.blit(pygame.transform.scale(self.tileset[0][2], (self.width, self.height)), (self.x, self.y))
            self.frame_timer += 1
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







    
