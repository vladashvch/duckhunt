from abc import ABC, abstractmethod
from gameobj import GameObj

class GameChar(ABC, GameObj):
    """
    An abstract class for game characters classes, that have velocity.

    Methods:
        update(): Updates the character's position based on its velocity. An abstract method.
    """
    @abstractmethod
    def update(self):
        """Updates the character's position based on its velocity and draws."""
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()
