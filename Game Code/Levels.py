# Main Game - making the levels
from GameDesign import *
from MazeGeneration import *
from MonsterClass import *
import pygame

#CITATION - all hex color codes are from https://htmlcolorcodes.com/color-picker/

#----------------------------- Sound Effects -----------------------------------
# from https://mixkit.co/free-sound-effects/game/
levelUpSound = pygame.mixer.Sound('levelUp.wav')

#-------------------------------------------------------------------------------

def checkIfLevelDone(app): #basically checks if you've reached the end goal
    row, col = app.playerRow, app.playerCol
    gRow, gCol = app.goalRow, app.goalCol

    if((row, col) == (gRow, gCol)):
        levelUpSound.play()
        app.level += 1
        app.rows += 5
        app.cols += 5
        app.r -= 1
        levels(app)

#I think I'll have five levels for now
def levels(app):
    #reseting everything 
    app.maze = set()
    app.crystalLocations = []
    app.bushes = []
    app.playerRow = app.rows-1
    app.playerCol = app.cols-1
    app.goalCol = random.randrange(app.cols)
    app.lives = 4
    app.board =[(['#22311d'] * app.cols) for row in range(app.rows)]
    generateMaze(app) 
    placeCrystals(app)

    #monsters
    app.slime = Monster(app)
    app.goblin = Goblin(app)
    app.zombie = Zombie(app)
    app.vampire = Vampire(app)
    app.ghost = ghost(app)

    app.slime1 = Monster(app)
    app.vampire1 = Vampire(app)
    app.goblin1 = Goblin(app)
    app.ghost1 = ghost(app)
    app.zombie1 = Zombie(app)

    app.slime2 = Monster(app)
    app.vampire2 = Vampire(app)
    app.goblin2 = Goblin(app)
    app.ghost2 = ghost(app)
    app.zombie2 = Zombie(app)

    if(app.level == 1):
        app.bush = loadImage(app,'sprites/bush.png', 2/7)

    elif(app.level == 2):
        app.bush = app.scaleImage(app.bush, 2/3)

    elif(app.level == 3):
        app.bush = app.scaleImage(app.bush, 3/4)
        rescalePlayer(app, 3/4)
        rescaleMonsters(app, 3/4)
    
    elif(app.level == 4):
        app.bush = app.scaleImage(app.bush, 3/4)
    
    elif(app.level == 5):
        app.bush = app.scaleImage(app.bush, .75)
    
    elif(app.level == 6):
        app.sound.stop()
        #SONG - Ecifircas by Sewerslvt
        app.song = 'Sewerslvt-Ecifircas.wav'
        app.sound = Sound(app.song)
        app.sound.start()
        app.mode = 'finalBoss'
    

def rescalePlayer(app, scale):
    if(app.chosenPlayer == 0):
        app.p1Fr = app.scaleImage(app.p1Fr, scale)
        app.p1Back = app.scaleImage(app.p1Back, scale)
        app.p1Left = app.scaleImage(app.p1Left, scale)
        app.p1Right =app.scaleImage(app.p1Right, scale)
    
    elif(app.chosenPlayer == 1):
        app.p2Fr = app.scaleImage(app.p2Fr, scale)
        app.p2Back = app.scaleImage(app.p2Back, scale)
        app.p2Left = app.scaleImage(app.p2Left, scale)
        app.p2Right =app.scaleImage(app.p2Right, scale)
    
    elif(app.chosenPlayer == 2):
        app.p3Fr = app.scaleImage(app.p3Fr, scale)
        app.p3Back = app.scaleImage(app.p3Back, scale)
        app.p3Left = app.scaleImage(app.p3Left, scale)
        app.p3Right =app.scaleImage(app.p3Right, scale)

def rescaleMonsters(app, scale):
    app.gobLeft = app.scaleImage(app.gobLeft, scale)
    app.gobRight = app.scaleImage(app.gobRight, scale)
    app.ghostBack = app.scaleImage(app.ghostBack, scale)
    app.ghostFr = app.scaleImage(app.ghostFr, scale)
    app.slimeFr = app.scaleImage(app.slimeFr, 1/2)
    app.slimeBack = app.scaleImage(app.slimeBack, 1/2)
    app.vampFr = app.scaleImage(app.vampFr, scale)
    app.vampBack = app.scaleImage(app.vampBack, scale)
    app.zomFr = app.scaleImage(app.zomFr, scale)
    app.zomBack = app.scaleImage(app.zomBack, scale)
    app.zomRight = app.scaleImage(app.zomRight, scale)
    app.zomLeft = app.scaleImage(app.zomLeft, scale)
    
def loadImage(app, png, scale = 1):
    img1 = app.loadImage(png)
    img2 = app.scaleImage(img1, scale)
    return img2
