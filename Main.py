import pygame
pygame.init()

WIDTH = 1000
HEIGHT = 1000
FPS = 60
score  = 0
preyScore = 0
preyTimer = 0
preyCount = []

timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

STARTBG = pygame.image.load("images/startmenu.png")
LAYERBG = pygame.image.load("images/background.png")



def showResult(text, score):
    run = True
    PLAY_TEXT = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 45).render(text + " Score: " + str(score), True, "White")
    PLAY_RECT = PLAY_TEXT.get_rect(center=(500, 260))


    # Визначаємо розміри контура
    stroke_width = 2

    # Намальований прямокутник з контуром та заповненням
    border_rect = PLAY_RECT.inflate(stroke_width, stroke_width)
    
    # Відображаємо заповнений прямокутник
    pygame.draw.rect(screen, "Black", border_rect)  # Заповнений прямокутник

    # Відображаємо контур прямокутника
    pygame.draw.rect(screen, "White", border_rect, stroke_width)  # Контур прямокутника

    # Відображаємо текст у центрі прямокутника
    screen.blit(PLAY_TEXT, PLAY_RECT)
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                run = False
            pygame.display.flip()
    pygame.quit()                                
    

def showGameUi():
    run = True
    
    
    while run:
        screen.fill(pygame.Color('#3FBFFE'))
        timer.tick(FPS)
        screen.blit(LAYERBG,(0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    showResult(" You win! ", score)
                      
        pygame.display.flip()        
    pygame.quit()     

def startMenu():
    run = True
    
    while run:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    showGameUi()  
                    
        screen.blit(STARTBG,(0,0))
        pygame.display.flip()        
    pygame.quit()     

if __name__ == "__main__":
    startMenu()
    