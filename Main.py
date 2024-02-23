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


def backgroundScreenBlit(image, x, y):
    SCREEN.blit(image, (x, y))


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

def cursor():
    
    mousePos = pygame.mouse.get_pos()
    targetCursor.draw() 
    targetCursor.x = mousePos[0] - targetCursor.width / 2
    targetCursor.y = mousePos[1] - targetCursor.height / 2
    
def renderText(screen, font, text, size, color, position):
    
    rendered_text = pygame.font.Font(font, size).render(str(text), True, color)
    text_rect = rendered_text.get_rect(center=position)
    screen.blit(rendered_text, text_rect)

def bulletsUI(bulletsCount): 
       
    backgroundScreenBlit(SHOT, 85, 870) 
    bulletXPosition = 90
    for _ in range(bulletsCount):
        SCREEN.blit(BULLET, (bulletXPosition, 838))
        bulletXPosition += 30 
    renderText(SCREEN, FONT, "R = "+ str(bulletsCount), 25, "White", (135, 790))

def preyUIUpgrade(blit_arguments, prey_defeat_count):
    for i, is_alive in enumerate(prey_defeat_count):
        x, y = blit_arguments[i][1]
        if is_alive:
            blit_arguments[i] = (PREYDEAD, (x, y))
        else:
            blit_arguments[i] = (PREYALIVE, (x, y))
        backgroundScreenBlit(blit_arguments[i][0], x, y)
 
def preyUI():
    blit_arguments = []
    preyXPosition = 370
    for _ in range(PREY_MAX_COUNT):
        blit_arguments.append((PREY, (preyXPosition, 850)))
        backgroundScreenBlit(PREY, preyXPosition, 850)
        preyXPosition += 30
        
    preyUIUpgrade(blit_arguments, preyDefeatCount)   
    
def handle_user_events(bulletsMaxCount, checkKillCollision, bulletsCount, goose, targetCursor,  score, preyScore, preyDefeatCount, preyCount):
    """
    Handle user input events, such as quitting the game or shooting bullets.
    """
    for event in pygame.event.get():
        if len(preyDefeatCount) == PREY_MAX_COUNT and preyDefeatCount.count(True) >= WIN_PREY_COUNT:
            showResult(" You win! ", score, preyScore)
            return False
                
        elif len(preyDefeatCount) == PREY_MAX_COUNT and preyDefeatCount.count(True) < WIN_PREY_COUNT:
            showResult(" Oh no... You lose! ", score, preyScore)
            return False

        elif event.type == pygame.QUIT:
            return False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and bulletsCount >= 1:
            bulletsCount -= 1
            if checkKillCollision(goose, targetCursor, KILLRADIUS):
                renderText(SCREEN, FONT, goose.killPrice, 35, "White", (goose.x, goose.y))
                goose.alive = False
                score += goose.killPrice
                preyScore += 1
                bulletsCount = bulletsMaxCount
    return bulletsCount, score, True
    
def preyCounter(prayFramesUpdating, hunterStartTime, preyCount, preyDefeatCount, bulletsCount, bulletsMaxCount, goose, dog):
    """
    Counter for the prey.

    This function updates the prey state based on various conditions such as being shot, flying away, or being caught.
    It also updates the prey's movement and animation.
    """
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
            
    elif bulletsCount == 0 or prayFramesUpdating >= FPS * 5:
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
            prayFramesUpdating += 1

    return prayFramesUpdating, hunterStartTime, bulletsCount
        
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
            prayFramesUpdating, hunterStartTime, bulletsCount = preyCounter(prayFramesUpdating, hunterStartTime, preyCount, preyDefeatCount, bulletsCount, bulletsMaxCount, goose, dog)
                      
        backgroundScreenBlit(LAYERBG, 0, 0)            
        backgroundScreenBlit(HIT, 245, 845) 
        
        pygame.mouse.set_visible(False)
        cursor()
        
        backgroundScreenBlit(SCORE, 800, 870)     
        renderText(SCREEN, FONT, str(score), 35, "White", (880, 850))
        
        bulletsUI(bulletsCount)
        preyUI()
        
        bulletsCount, score, run  = handle_user_events(bulletsMaxCount, checkKillCollision, bulletsCount, goose, targetCursor,  score, preyScore, preyDefeatCount, preyCount)
        pygame.display.flip()     
  


def showResultText(text, score, preys):
    renderText(SCREEN, FONT, text, 45, "White", (500, 200))
    renderText(SCREEN, FONT, "Score: " + str(score), 45, "White", (500, 250))
    renderText(SCREEN, FONT, "Ducks: " + str(preys) + " from "+ str(PREY_MAX_COUNT), 45, "White", (500, 300))
            
def showResultEvents():
    """
    This function checks for events in the pygame event queue.
    It returns False if the QUIT event is detected or if the left mouse button is clicked.
    Otherwise, it returns True.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            return False
    return True

def showResult(text, score, preys):
    """
    This method is responsible for displaying the result of a certain operation or process.
    It might be used to show the outcome of a game, the result of a calculation, or any other type of result.
    The specific behavior of this method depends on the context in which it's used and the way it's implemented.
    """
    run = True
 
    while run:
        pygame.mouse.set_visible(True)
        pygame.draw.rect(SCREEN, (0, 0, 0), (250, 150, 500, 225))
        showResultText(text, score, preys)
        run = showResultEvents()   
        pygame.display.flip()
    pygame.quit()


    
def startMenuEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            showGame()
            return False
    return True
    
def startMenu():
    """
    This method is responsible for launching the game. This is the starting point of the game from which the user will start the game.
    """
    run = True
    while run:  
        pygame.mouse.set_visible(True)
        backgroundScreenBlit(STARTBG, 0, 0)
        run = startMenuEvents()   
        pygame.display.flip()      
    pygame.quit()


if __name__ == "__main__":
    startMenu()
         