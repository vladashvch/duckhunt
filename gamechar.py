from abc import ABC, abstractmethod
from gameobj import GameObj

class GameChar(ABC, GameObj):
    @abstractmethod
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()
