import pygame
pygame.init()


WIDTH = 1000
HEIGHT = 1000
FPS = 60
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()

score  = 0
preyScore = 0
preyTimer = 0
preyCount = []
preyMaxCount = 10
bulletsCount = []
bulletsMaxCount = 3

pygame.display.set_caption("DuckHunt")

STARTBG = pygame.image.load("assets/startmenu.png")
LAYERBG = pygame.image.load("assets/background.png")

HIT = pygame.image.load("assets/hit.png")
PREYDEAD = pygame.image.load("assets/preydead.png")
PREYALIVE = pygame.image.load("assets/preyalive.png")

SHOT = pygame.image.load("assets/shot.png")
BULLET = pygame.image.load("assets/bullet.png")
SCORE =  pygame.image.load("assets/score.png")


def showResult(text, score, preys):
    run = True
    text_render = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 45).render(text, True, "White")
    score_render = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 45).render("Score: " + str(score), True, "White")
    pray_render = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 45).render("Ducks: " + str(preys) + " from "+ str(preyMaxCount), True, "White")
    
    text_loc = text_render.get_rect(center=(500, 200))
    score_loc = score_render.get_rect(center=(500, 250))
    pray_loc = pray_render.get_rect(center=(500, 300))

    while run:
        # show black rectangle behind text
        pygame.draw.rect(screen, (0, 0, 0), (250, 150, 500, 225))

        # show text
        screen.blit(text_render, text_loc)
        screen.blit(score_render, score_loc)
        screen.blit(pray_render, pray_loc)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                run = False
        pygame.display.flip()
    pygame.quit()                                


def showGameUi():
    run = True
    
    while run:
        timer.tick(FPS)
        
        # fill down layer of screen with color
        screen.fill(pygame.Color('#3FBFFE'))
        
        # upper layer with grass and ui
        screen.blit(LAYERBG,(0,0))
        
        # hit ui
        screen.blit(HIT,(245,845))
        # loop spawning of "alive prey" icons
        preyAliveXPosition = 370
        for _ in range(preyMaxCount): 
            screen.blit(PREYALIVE, (preyAliveXPosition, 850))
            preyAliveXPosition += 30 
        
        # score ui
        screen.blit(SCORE,(800,870))
        textScore_render = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 35).render(str(preyScore), True, "White")
        textScore_loc = textScore_render.get_rect(center=(880,850))
        screen.blit(textScore_render, textScore_loc)
        
        # bullets count ui
        bullets_render = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 25).render("R = "+ str(len(bulletsCount)), True, "White")
        bullets__loc = bullets_render.get_rect(center=(135,790))
        screen.blit(bullets_render, bullets__loc)
        
        # shot ui
        screen.blit(SHOT,(85,870))
        # loop spawning of bullets icons
        bulletXPosition = 90
        for _ in range(bulletsMaxCount):
            screen.blit(BULLET, (bulletXPosition, 838))
            bulletXPosition += 30 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            # show result depends on preyScore
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    showResult(" You win! ", score, preyScore)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    showResult(" Oh no... You lose! ", score, preyScore)          
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
        
        #show start menu bg
        screen.blit(STARTBG,(0,0))
        pygame.display.flip()        
    pygame.quit()     

if __name__ == "__main__":
    startMenu()
    