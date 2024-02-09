import pygame
pygame.init()

WIDTH = 1000
HEIGHT = 1000
FPS = 60
timer = pygame.time.Clock
screen = pygame.display.set_mode([WIDTH, HEIGHT])

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
    pygame.quit()     


if __name__ == "__main__":
    main()
