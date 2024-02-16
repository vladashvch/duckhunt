import pygame
from constants import TIMER, FPS, SCREEN, KILLRADIUS, WIDTH
from cursor import Cursor
from pray import Pray
from random import randint

pygame.init()
pygame.display.set_caption("DuckHunt")

preyTimer = 0
preyCount = []
preyDefeatCount = []
preyMaxCount = 10
winPreyCount = 8
last_score = 0

STARTBG = pygame.image.load("assets/startmenu.png")
LAYERBG = pygame.image.load("assets/background.png")
HIT = pygame.image.load("assets/hit.png")
PREYDEAD = pygame.image.load("assets/preydead.png")
PREYALIVE = pygame.image.load("assets/preyalive.png")
PREY = pygame.image.load("assets/prey.png")
SHOT = pygame.image.load("assets/shot.png")
BULLET = pygame.image.load("assets/bullet.png")
SCORE =  pygame.image.load("assets/score.png")
FONT = "assets/VCR_OSD_MONO_1.001.ttf"
CURSOR = pygame.image.load("assets/cursor.png")

                            
targetCursor = Cursor(0, 0, 50, 50, CURSOR) 
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
    prayFramesUpdating = 0
    while run:
        TIMER.tick(FPS)
        bulletsCount = 3
        bulletsMaxCount = 3 
        score  = 0
        preyScore = 0   
        # fill down layer of screen with color
        SCREEN.fill(pygame.Color('#3FBFFE'))
        
        if len(preyCount) > 0:
            goose = preyCount[0]
            # update the goose's image based on its state
            if goose.alive == False:
                goose.dying()
                if goose.y > 700:
                    preyCount.remove(goose)
                    preyDefeatCount.append(True)
                    prayFramesUpdating = 0
            elif bulletsCount == 0 or prayFramesUpdating>=FPS * 5: #or 5 sec & goose.alive == True
                goose.flyAway()
                if goose.y < -goose.width or goose.x > WIDTH + goose.width:
                    preyCount.remove(goose)
                    preyDefeatCount.append(False)
                    bulletsCount = bulletsMaxCount
                    prayFramesUpdating = 0  
            else:
                if goose.x < 20:
                    goose.start()
                else:
                    goose.update()
                    prayFramesUpdating+=1
         
      
        SCREEN.blit(LAYERBG,(0,0))
        
        pygame.mouse.set_visible(False)
        mousePos = pygame.mouse.get_pos()
        targetCursor.draw() 
        targetCursor.x = mousePos[0] - targetCursor.width / 2
        targetCursor.y = mousePos[1] - targetCursor.height / 2
        
        SCREEN.blit(HIT,(245,845))
        preyXPosition = 370
        for _ in range(preyMaxCount): 
            SCREEN.blit(PREY, (preyXPosition, 850))
            preyXPosition += 30 
            
        SCREEN.blit(SCORE,(800,870))
        textScore_render = pygame.font.Font(FONT, 35).render(str(score), True, "White")
        textScore_loc = textScore_render.get_rect(center=(880,850))
        SCREEN.blit(textScore_render, textScore_loc)
        
        SCREEN.blit(SHOT,(85,870))
        bulletXPosition = 90
        for _ in range(bulletsCount):
            SCREEN.blit(BULLET, (bulletXPosition, 838))
            bulletXPosition += 30 
        bulletsRender = pygame.font.Font(FONT, 25).render("R = "+ str(bulletsCount), True, "White")
        bulletsLoc = bulletsRender.get_rect(center=(135,790))
        SCREEN.blit(bulletsRender, bulletsLoc)
        
        killCollision = checkKillCollision(goose, targetCursor, KILLRADIUS)  
        for event in pygame.event.get():
            if len(preyDefeatCount) == preyMaxCount and preyDefeatCount.count(True) >= winPreyCount:
                showResult(" You win! ", score, preyScore)
                
            elif len(preyDefeatCount) == preyMaxCount and preyDefeatCount.count(True) < winPreyCount:
                    showResult(" Oh no... You lose! ", score, preyScore)  
                    
            else:
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and bulletsCount >= 1:
                    bulletsCount -= 1
                    
                    if killCollision:
                        goose.alive = False
                        score += goose.killPrice
                        preyScore += 1
                        bulletsCount = bulletsMaxCount
          
                   
        pygame.display.flip()        
    pygame.quit()     

def showResult(text, score, preys):
    run = True
    textRender = pygame.font.Font(FONT, 45).render(text, True, "White")
    scoreRender = pygame.font.Font(FONT, 45).render("Score: " + str(score), True, "White")
    prayRender = pygame.font.Font(FONT, 45).render("Ducks: " + str(preys) + " from "+ str(preyMaxCount), True, "White")
    
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
    