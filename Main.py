import pygame
from constants import TIMER, FPS, SCREEN, KILLRADIUS, WIDTH
from cursor import Cursor
from pray import Pray
from hunter import Hunter
from random import randint
import time

pygame.init()
pygame.display.set_caption("DuckHunt")

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

preyTimer = 0
preyDefeatCount = []
preyMaxCount = 10
winPreyCount = 8
last_score = 0  
   
                            

preyCount = []
for _ in range(preyMaxCount):
    goose = Pray(-50, randint(200, 550), 154, 145, "images/goose_tileset.png")
    preyCount.append(goose)

dogCount = []  # List to store dog objects
dog = Hunter(400, 580, 200, 150, "assets/dog_tileset.png")
dogCount.append(dog)  # Add initial dog object to the list
targetCursor = Cursor(0, 0, 50, 50, CURSOR) 

def checkKillCollision(prey, targetCursor, radius):
    preyCenterX, preyCenterY = prey.getCenter()
    targetCursorCenterX, targetCursorCenterY = targetCursor.getCenter()
    distance = ((preyCenterX - targetCursorCenterX) ** 2 + (preyCenterY - targetCursorCenterY) ** 2) ** 0.5
    return distance <= radius

def showGame():
    run = True
    prayFramesUpdating = 0
    bulletsCount = 3
    bulletsMaxCount = 3 
    score  = 0
    preyScore = 0  
    laughing_start_time = None
    while run:
        TIMER.tick(FPS)
        
        SCREEN.fill(pygame.Color('#3FBFFE'))
        
        if len(preyCount) > 0:
            goose = preyCount[0]

            if goose.alive == False:
                goose.dying()

                if goose.y > 700:
                    
                    dog.update("catch")
                    if laughing_start_time is None:
                        laughing_start_time = time.time()
                
                    if time.time() - laughing_start_time >= 2.2:
                        preyCount.remove(goose)
                        preyDefeatCount.append(True)
                        prayFramesUpdating = 0
                    
            elif bulletsCount == 0 or prayFramesUpdating >= FPS * 5:  # or 5 sec & goose.alive == True
                goose.flyAway()
                
                
                dog.update("laughing")
                if laughing_start_time is None:
                    laughing_start_time = time.time()
                
                if time.time() - laughing_start_time >= 2.2:
                    if goose.y < -goose.width or goose.x > WIDTH + goose.width:
                        preyCount.remove(goose)
                        dogCount.remove(dog)
                        preyDefeatCount.append(False)
                        bulletsCount = bulletsMaxCount
                        prayFramesUpdating = 0
                        laughing_start_time = None 
                        dogCount.append(dog)
                               
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
        killCollision = checkKillCollision(goose, targetCursor, KILLRADIUS) 
        
        SCREEN.blit(HIT,(245,845))
        blit_arguments = []
        preyXPosition = 370
        for _ in range(preyMaxCount): 
            blit_arguments.append((PREY, (preyXPosition, 850)))
            SCREEN.blit(PREY, (preyXPosition, 850))
            preyXPosition += 30 
            
        for i, is_alive in enumerate(preyDefeatCount):
            if is_alive:  

                x, y = blit_arguments[i][1]  
                blit_arguments[i] = (PREYDEAD, (x, y)) 
                SCREEN.blit(PREYDEAD, (x, y))
                
            if not is_alive:  
                x, y = blit_arguments[i][1]  
                blit_arguments[i] = (PREYALIVE, (x, y)) 
                SCREEN.blit(PREYALIVE, (x, y))
            
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
        
        for event in pygame.event.get():
            if len(preyDefeatCount) == preyMaxCount and preyDefeatCount.count(True) >= winPreyCount:
                showResult(" You win! ", score, preyScore)
                return 
                
            elif len(preyDefeatCount) == preyMaxCount and preyDefeatCount.count(True) < winPreyCount:
                    showResult(" Oh no... You lose! ", score, preyScore)  
                    return 
                    
            else:
                if event.type == pygame.QUIT:
                    run = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and bulletsCount >= 1:
                    bulletsCount -= 1
                    
                    if killCollision:
                        textScore_render = pygame.font.Font(FONT, 35).render(str(goose.killPrice), True, "White")
                        textScore_loc = textScore_render.get_rect(center=(goose.x , goose.y ))
                        SCREEN.blit(textScore_render, textScore_loc)
                                        
                        goose.alive = False
                        score += goose.killPrice
                        preyScore += 1
                        bulletsCount = bulletsMaxCount      
        pygame.display.flip()        
        

def showResult(text, score, preys):
    run = True
    textRender = pygame.font.Font(FONT, 45).render(text, True, "White")
    scoreRender = pygame.font.Font(FONT, 45).render("Score: " + str(score), True, "White")
    prayRender = pygame.font.Font(FONT, 45).render("Ducks: " + str(preys) + " from "+ str(preyMaxCount), True, "White")
    
    text_loc = textRender.get_rect(center=(500, 200))
    score_loc = scoreRender.get_rect(center=(500, 250))
    pray_loc = prayRender.get_rect(center=(500, 300))

    while run:
        pygame.mouse.set_visible(True)
        # show black rectangle behind text
        pygame.draw.rect(SCREEN, (0, 0, 0), (250, 150, 500, 225))

        # show text
        SCREEN.blit(textRender, text_loc)
        SCREEN.blit(scoreRender, score_loc)
        SCREEN.blit(prayRender, pray_loc)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                run = False
                return 
                
        pygame.display.flip()
    pygame.quit()
    
def startMenu():
    run = True
    while run:  
        pygame.mouse.set_visible(True)
        SCREEN.blit(STARTBG,(0,0))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                showGame()   
                return        
    pygame.quit()

if __name__ == "__main__":
    startMenu()
         