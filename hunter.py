import pygame
from random import choice
from constants import SCREEN
from gamechar import GameChar


class Hunter(GameChar):
    """
    Class for the hunter object in the game.
    Inherits from abstract GameChar.

    Attributes:
        - x (int): The x-coordinate of the hunter's position.
        - y (int): The y-coordinate of the hunter's position.
        - width (int): The width of the hunter's sprite.
        - height (int): The height of the hunter's sprite.
        - tileset (str): The filename of the tileset image
        for the hunter's sprite.
        - flipX (bool): Indicates whether the hunter's sprite
        should be flipped horizontally.
        - frame (int): The current frame index of
        the hunter's animation.
        - frames (list): A list of frame indices for
        the hunter's animation.
        - frameTimer (int): The timer for controlling
        the animation frame rate.
        - velocity (list): The velocity of the hunter
        in the x and y directions.
        - goingDown (bool): Indicates whether the hunter
        is moving down.
        - heighPlus (int): The maximum y-coordinate
        the hunter can reach before going down.

    Methods:
        - __init__(self, x, y, width, height, tileset, xMax):
        Constructor for Hunter class.
        - update(self, state): Updates the hunter's state and position.
        - loadTileset(self, filename, width, height):
        Loads the tileset image for the hunter's sprite.
        - draw(self, state): Draws the hunter's sprite
        on the screen depending on the state.
    """

    animationFramerate = 12
    defaultX = 400
    defaultY = 590
    reactionLine = 0
    catchFrame = 0
    laughFrames = [1, 2]
    heighPlus = 0

    def __init__(self, x, y, width, height, tileset, heighPlus):
        """
        Initialize the Hunter object.
        Args:
            x (int): The x-coordinate of the Hunter's position.
            y (int): The y-coordinate of the Hunter's position.
            width (int): The width of the Hunter.
            height (int): The height of the Hunter.
            tileset (str): The path to the tileset image.
            heighPlus (int): The additional height of the Hunter.
        """
        super().__init__(x, y, width, height, None)
        self.tileset = self.load_tileset(tileset, width, height)
        self.flipX = choice([True, False])
        self.frame = 0
        self.frameTimer = 0
        self.velocity = [0, 0]
        self.goingDown = False
        self.heighPlus = heighPlus
        self.state = None

    def update(self, state):
        """
        Updates the hunter's state and position. The hunter go up and down.
        Args:
            state: The current state of the game.
        """
        self.state = state
        self.velocity[1] = 4
        self.draw()
        yTemp = self.y

        if self.y <= (self.defaultY-self.heighPlus):
            self.goingDown = True
        elif self.y > yTemp:
            self.goingDown = False

        if self.goingDown:
            self.y += self.velocity[1]
        else:
            self.y -= self.velocity[1]

    def draw(self):
        """
        Draw the hunter on the screen based on the given state.
        Parameters:
        state (str): The state of the hunter.
        It can be "catch" or "laughing".
        """
        if self.state == "catch":
            image = pygame.transform.scale(
                self.tileset[self.catchFrame][self.reactionLine],
                (self.width, self.height))
            SCREEN.blit(pygame.transform.flip(
                image, self.flipX, False), (self.x, self.y))

        if self.state  == "laughing":
            if self.frame >= len(self.laughFrames):
                self.frame = 0

            image = pygame.transform.scale(self.tileset[
                self.laughFrames[self.frame]][self.reactionLine],
                                           (self.width, self.height))
            SCREEN.blit(pygame.transform.flip(
                image, self.flipX, False), (self.x, self.y))

            self.frameTimerMethod(self.laughFrames)     # GameChar method

    def initialState(self):
        """
        Initializes the state of the hunter object.
        """
        self.x = self.defaultX
        self.y = self.defaultY
        self.flipX = choice([True, False])
        self.frame = 0
        self.frameTimer = 0
        self.goingDown = False
        self.heighPlus = self.heighPlus
