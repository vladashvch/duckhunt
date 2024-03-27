import pygame
import os

WIDTH = 1000
HEIGHT = 1000
FPS = 60
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
TIMER = pygame.time.Clock()
BOUNDS_X = (20, 990)
BOUNDS_Y = (20, 600)
KILLRADIUS = 20
CHARANIMATIONFPS = 12

PREY_MAX_COUNT = 10
WIN_PREY_COUNT = 8

ASSETS_PATH = "assets"

STARTBG = pygame.image.load(os.path.join(ASSETS_PATH, "startmenu.png"))
LAYERBG = pygame.image.load(os.path.join(ASSETS_PATH, "background.png"))
HIT = pygame.image.load(os.path.join(ASSETS_PATH, "hit.png"))
PREYDEAD = pygame.image.load(os.path.join(ASSETS_PATH, "preydead.png"))
PREYALIVE = pygame.image.load(os.path.join(ASSETS_PATH, "preyalive.png"))
PREY = pygame.image.load(os.path.join(ASSETS_PATH, "prey.png"))
SHOT = pygame.image.load(os.path.join(ASSETS_PATH, "shot.png"))
BULLET = pygame.image.load(os.path.join(ASSETS_PATH, "bullet.png"))
SCORE = pygame.image.load(os.path.join(ASSETS_PATH, "score.png"))
FONT = os.path.join(ASSETS_PATH, "VCR_OSD_MONO_1.001.ttf")
CURSOR = pygame.image.load(os.path.join(ASSETS_PATH, "cursor.png"))
PREY_ORIGINAL = os.path.join(ASSETS_PATH, "ordinar_goose_tileset.png")
HUNTER_ORIGINAL = os.path.join(ASSETS_PATH, "dog_ordinar_goose_tileset.png")