import pygame

WIDTH = 1000
HEIGHT = 1000
FPS = 60
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
TIMER = pygame.time.Clock()
BOUNDS_X = (20, 990)
BOUNDS_Y = (20, 600)
KILLRADIUS = 20
CHARANIMATIONFPS = 12