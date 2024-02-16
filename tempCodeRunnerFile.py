                            

preyCount = []
for _ in range(preyMaxCount):
    goose = Pray(-50, randint(200, 550), 154, 145, "images/goose_tileset.png")
    preyCount.append(goose)

dog = Dog(500, 500, 200, 150, "assets/dog_tileset.png")
targetCursor = Cursor(0, 0, 50, 50, CURSOR) 

def checkKillCollision(prey, targetCursor, radius):
    preyCenterX, preyCenterY = prey.getCenter()
    targetCursorCenterX, targetCursorCenterY = targetCursor.getCenter()
    distance = ((preyCenterX - targetCursorCenterX) ** 2 + (preyCenterY - targetCursorCenterY) ** 2) ** 0.5
    return distance <= radius