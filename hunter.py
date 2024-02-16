import pygame
from constants import SCREEN
from object import Object
from constants import TIMER, FPS
class Hunter(Object):
    animationFramerate = 12
    
    def __init__(self, x, y, width, height, tileset, direction=1):
        super().__init__(x, y, width, height, None)
        self.tileset = self.load_tileset(tileset, width, height)
        self.direction = direction
        self.flipX = False
        self.frame = 0
        self.frames = [0]  # Початково використовуємо перший кадр
        self.frame_timer = 0
        self.delay_timer = 0
        self.delay_duration = 5 * FPS  # Затримка у 5 секунд
        self.velocity = [0, 0]
        self.going_down = False
        
    def update(self, state):
        self.draw(state)
        yTemp = self.y

        if self.y <= 400:
            self.going_down = True 

        elif self.y > yTemp:  
            self.going_down = False  

        if self.going_down:
            self.y += 2  
        else:
            self.y -= 2
        
    def load_tileset(self, filename, width, height):
        
            image = pygame.image.load(filename).convert_alpha()
            image_width, image_height = image.get_size()    
            tileset = []
            line = []  # Створюємо список для зберігання тайлів першого рядка
            for tile_x in range(0, image_width // width):
                rect = (tile_x * width, 0, width, height)  # Виділяємо тайл з першого рядка
                line.append(image.subsurface(rect))  # Додаємо тайл до списку рядка
            tileset.append(line)  # Додаємо список рядка до загального списку тайлів
            return tileset
  
    
    def draw(self, state):
        if state == "laughing":
            self.frames = [1, 2]  # Використовуємо другий та третій кадри з тайлсету

        if self.frame >= len(self.frames):
            self.frame = 0

        image_index = self.frames[self.frame]  

        # Отримуємо зображення з тайлсету
        image = pygame.transform.scale(self.tileset[0][image_index], (self.width, self.height))
        SCREEN.blit(pygame.transform.flip(image, self.flipX, False), (self.x, self.y))

        self.frame_timer += 1
        if self.frame_timer < self.animationFramerate:
            return
        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0
        self.frame_timer = 0  
            
