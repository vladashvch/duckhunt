import pygame
from constants import TIMER, FPS, SCREEN, KILLRADIUS, WIDTH, PREY_MAX_COUNT, WIN_PREY_COUNT
from gameobj import GameObj
from prey import Prey
from hunter import Hunter
from random import randint
import time
import argparse

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
preyCount = []

parser = argparse.ArgumentParser(description='Optional arguments for the script.')
parser.add_argument('--red_goose', action='store_true', help='Use red goose tileset instead of the default one')
parser.add_argument('--drone', action='store_true', help='Use drone tileset instead of the default one')
args = parser.parse_args()

preyTilesetPath = "assets/ordinar_goose_tileset.png"
dogTilesetPath = "assets/dog_ordinar_goose_tileset.png"
if args.red_goose:
    preyTilesetPath = "assets/red_goose_tileset.png"
    dogTilesetPath = "assets/dog_red_goose_tileset.png"
elif args.drone:
    preyTilesetPath = "assets/drone_tileset.png"
    dogTilesetPath = "assets/dog_drone_tileset.png"   
    
for _ in range(PREY_MAX_COUNT):
    goose = Prey(-50, randint(200, 550), 154, 145, preyTilesetPath, 100)
    preyCount.append(goose)

dog = Hunter(Hunter.defaultX, Hunter.defaultY,200, 293, dogTilesetPath, 200)
targetCursor = GameObj(0, 0, 50, 50, CURSOR) 


def checkKillCollision(prey, targetCursor, radius):
    """
    Check if there is a collision between the prey and the target cursor within the given radius.
    Args:
        prey (object): The prey object.
        targetCursor (object): The target cursor object.
        radius (float): The radius within which the collision is checked.
    Returns:
        bool: True if there is a collision, False otherwise.
    """
    preyCenterX, preyCenterY = prey.getCenter()
    targetCursorCenterX, targetCursorCenterY = targetCursor.getCenter()
    distance = ((preyCenterX - targetCursorCenterX) ** 2 + (preyCenterY - targetCursorCenterY) ** 2) ** 0.5
    return distance <= radius

def showGame():
    """
    Show the main game loop for the Duck Hunt game.

    This function initializes the game variables, updates the game state, and handles user input.
    It displays the game screen, including the background, prey, score, bullets, and target cursor.
    The function also checks for collisions between the target cursor and the prey, and updates the score accordingly.
    The game loop continues until the player wins or loses the game, or chooses to quit.
    """
    run = True
    prayFramesUpdating = 0
    bulletsCount = 3
    bulletsMaxCount = 3 
    score  = 0
    preyScore = 0  
    hunterStartTime = None
    while run:
        TIMER.tick(FPS)
        
        SCREEN.fill(pygame.Color('#3FBFFE'))
        
        if len(preyCount) > 0:
            goose = preyCount[0]

            if goose.alive == False:
                goose.dying()

                if goose.y > 700:
                    dog.update("catch")
                    if hunterStartTime is None:
                        hunterStartTime = time.time()
                
                    if time.time() - hunterStartTime >= 2:
                        preyCount.remove(goose)
                        preyDefeatCount.append(True)
                        prayFramesUpdating = 0
                        hunterStartTime = None
                    
            elif bulletsCount == 0 or prayFramesUpdating >= FPS * 5:  # or 5 sec & goose.alive == True
                goose.flyAway()
                dog.update("laughing")
                if hunterStartTime is None:
                    hunterStartTime = time.time()
                
                if time.time() - hunterStartTime >= 2:
                    if goose.y < -goose.width or goose.x > WIDTH + goose.width:
                        preyCount.remove(goose)
                        preyDefeatCount.append(False)
                        bulletsCount = bulletsMaxCount
                        prayFramesUpdating = 0
                        hunterStartTime = None 
                               
            else:
                if goose.x < 20:
                    goose.start()
                    dog.initialState()
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
        blitArguments = []
        preyXPosition = 370
        for _ in range(PREY_MAX_COUNT): 
            blitArguments.append((PREY, (preyXPosition, 850)))
            SCREEN.blit(PREY, (preyXPosition, 850))
            preyXPosition += 30 
            
        for i, is_alive in enumerate(preyDefeatCount):
            if is_alive:  

                x, y = blitArguments[i][1]  
                blitArguments[i] = (PREYDEAD, (x, y)) 
                SCREEN.blit(PREYDEAD, (x, y))
                
            if not is_alive:  
                x, y = blitArguments[i][1]  
                blitArguments[i] = (PREYALIVE, (x, y)) 
                SCREEN.blit(PREYALIVE, (x, y))
            
        SCREEN.blit(SCORE,(800,870))
        textScoreRender = pygame.font.Font(FONT, 35).render(str(score), True, "White")
        textScoreLoc = textScoreRender.get_rect(center=(880,850))
        SCREEN.blit(textScoreRender, textScoreLoc)
        
        SCREEN.blit(SHOT,(85,870))
        bulletXPosition = 90
        for _ in range(bulletsCount):
            SCREEN.blit(BULLET, (bulletXPosition, 838))
            bulletXPosition += 30 
        bulletsRender = pygame.font.Font(FONT, 25).render("R = "+ str(bulletsCount), True, "White")
        bulletsLoc = bulletsRender.get_rect(center=(135,790))
        SCREEN.blit(bulletsRender, bulletsLoc)
        
        for event in pygame.event.get():
            if len(preyDefeatCount) == PREY_MAX_COUNT and preyDefeatCount.count(True) >= WIN_PREY_COUNT:
                showResult(" You win! ", score, preyScore)
                return 
                
            elif len(preyDefeatCount) == PREY_MAX_COUNT and preyDefeatCount.count(True) < WIN_PREY_COUNT:
                    showResult(" Oh no... You lose! ", score, preyScore)  
                    return 
                    
            else:
                if event.type == pygame.QUIT:
                    run = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and bulletsCount >= 1:
                    bulletsCount -= 1
                    
                    if killCollision:
                        textScoreRender = pygame.font.Font(FONT, 35).render(str(goose.killPrice), True, "White")
                        textScoreLoc = textScoreRender.get_rect(center=(goose.x , goose.y ))
                        SCREEN.blit(textScoreRender, textScoreLoc)
                                        
                        goose.alive = False
                        score += goose.killPrice
                        preyScore += 1
                        bulletsCount = bulletsMaxCount      
        pygame.display.flip()        
        

def showResult(text, score, preys):
    """
    This method is responsible for displaying the result of a certain operation or process.
    It might be used to show the outcome of a game, the result of a calculation, or any other type of result.
    The specific behavior of this method depends on the context in which it's used and the way it's implemented.
    """
    run = True
    textRender = pygame.font.Font(FONT, 45).render(text, True, "White")
    scoreRender = pygame.font.Font(FONT, 45).render("Score: " + str(score), True, "White")
    prayRender = pygame.font.Font(FONT, 45).render("Ducks: " + str(preys) + " from "+ str(PREY_MAX_COUNT), True, "White")
    
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
    """
    This method is responsible for launching the game. This is the starting point of the game from which the user will start the game.
    """
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
         