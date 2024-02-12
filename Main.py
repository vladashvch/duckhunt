import pygame
from constants import TIMER, FPS, SCREEN, KILLRADIUS
from cursor import Cursor
from pray import Pray
from random import randint

pygame.init()

score  = 0
preyScore = 0
preyTimer = 0
preyCount = []
preyMaxCount = 10
bulletsCount = 3
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

                            
targetCursor = Cursor(0, 0, 50, 50, pygame.image.load("assets/cursor.png")) 
for _ in range(preyMaxCount):
    goose = Pray(-50, randint(200, 550), 154, 145, "images/goose_tileset.png")
    preyCount.append(goose)

def checkKillCollision(prey, targetCursor, radius):
    preyCenterX, preyCenterY = prey.getCenter()
    targetCursorCenterX, targetCursorCenterY = targetCursor.getCenter()

    distance = ((preyCenterX - targetCursorCenterX) ** 2 + (preyCenterY - targetCursorCenterY) ** 2) ** 0.5

    return distance <= radius



 
def showGameUi():
    run = True
    
    while run:
        TIMER.tick(FPS)
        current_time = pygame.time.get_ticks()

        score  = 0
        preyScore = 0
        # fill down layer of screen with color
        SCREEN.fill(pygame.Color('#3FBFFE'))
        
        # upper layer with grass and ui
        SCREEN.blit(LAYERBG,(0,0))
        
        pygame.mouse.set_visible(False)
        mousePos = pygame.mouse.get_pos()
        targetCursor.draw() 
        targetCursor.x = mousePos[0] - targetCursor.width / 2
        targetCursor.y = mousePos[1] - targetCursor.height / 2
        
        
        if len(preyCount) > 0:
            goose = preyCount[0]
            # update the goose's image based on its state
            if goose.alive == True:
                if goose.x < 20:
                    goose.start()
                else:
                    goose.update()
            else:
                # goose.flyAway()
                # if goose.y < -goose.width or goose.x > WIDTH + goose.width:
                #     preyCount.remove(goose)
                goose.dying()
                if goose.y > 700:
                    preyCount.remove(goose)
        
        # hit ui
        SCREEN.blit(HIT,(245,845))
        # loop spawning of "alive prey" icons
        preyAliveXPosition = 370
        for _ in range(preyMaxCount): 
            SCREEN.blit(PREYALIVE, (preyAliveXPosition, 850))
            preyAliveXPosition += 30 
        
        # score ui
        SCREEN.blit(SCORE,(800,870))
        
        
        global bulletsCount
        global bulletsMaxCount  
        SCREEN.blit(SHOT,(85,870))
        bulletXPosition = 90
        for _ in range(bulletsCount):
            SCREEN.blit(BULLET, (bulletXPosition, 838))
            bulletXPosition += 30 


        bulletsRender = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 25).render("R = "+ str(bulletsCount), True, "White")
        bulletsLoc = bulletsRender.get_rect(center=(135,790))
        SCREEN.blit(bulletsRender, bulletsLoc)
        
        
        killCollision = checkKillCollision(goose, targetCursor, KILLRADIUS)  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bulletsCount -= 1
                
                if killCollision:
                    goose.alive = False
                    score += goose.killPrice
                    preyScore += 1
                    bulletsCount = bulletsMaxCount 
                
                if bulletsCount <= 0:
                    bulletsCount = bulletsMaxCount
                     
                 
            
            
            # # show result depends on preyScore
            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #         showResult(" You win! ", score, preyScore)
            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            #         showResult(" Oh no... You lose! ", score, preyScore)          
        pygame.display.flip()        
    pygame.quit()     

def showResult(text, score, preys):
    run = True
    textRender = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 45).render(text, True, "White")
    scoreRender = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 45).render("Score: " + str(score), True, "White")
    prayRender = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 45).render("Ducks: " + str(preys) + " from "+ str(preyMaxCount), True, "White")
    
    text_loc = textRender.get_rect(center=(500, 200))
    score_loc = scoreRender.get_rect(center=(500, 250))
    pray_loc = prayRender.get_rect(center=(500, 300))

    while run:
        # show black rectangle behind text
        pygame.draw.rect(SCREEN, (0, 0, 0), (250, 150, 500, 225))

        # show text
        SCREEN.blit(textRender, text_loc)
        SCREEN.blit(scoreRender, score_loc)
        SCREEN.blit(prayRender, pray_loc)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                run = False
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
        SCREEN.blit(STARTBG,(0,0))
        pygame.display.flip()        
    pygame.quit()     

if __name__ == "__main__":
    startMenu()
    