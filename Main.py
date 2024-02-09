import pygame
pygame.init()

WIDTH = 1000
HEIGHT = 1000
FPS = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
STARTBG = pygame.image.load("images/startmenu.png")
LAYERBG = pygame.image.load("images/background.png")

def play():
    run = True
    
    while run:
        screen.fill(pygame.Color('#3FBFFE'))
        timer.tick(FPS)
        screen.blit(LAYERBG,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()        
    pygame.quit()     

def start_menu():
    run = True
    
    while run:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    play()  
                    
        screen.blit(STARTBG,(0,0))
        pygame.display.flip()        
    pygame.quit()     

if __name__ == "__main__":
    start_menu()
    