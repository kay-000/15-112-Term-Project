# GAME DESIGN - This file has the basic design functions for the game.
#draws + moves the player, draws the crystals, draws the board, etc. 


from cmu_112_graphics import *
import pygame
import random
pygame.mixer.init()

#CITATION - all hex color codes are from https://htmlcolorcodes.com/color-picker/


#----------------------------- Sound Effects -----------------------------------
# from https://mixkit.co/free-sound-effects/game/
crystalCollectedSound = pygame.mixer.Sound('crystalCollected.wav')

#--------------------------Sound Class------------------------------------------
# source: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1
        pygame.mixer.music.load(path)

    # Returns True if the sound is currently playing
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())

    # Loops = number of times to loop the sound.
    # If loops = 1 or 1, play it once.
    # If loops > 1, play it loops + 1 times.
    # If loops = -1, loop forever.
    def start(self, loops=1):
        self.loops = loops
        pygame.mixer.music.play(loops=loops)

    # Stops the current sound from playing
    def stop(self):
        pygame.mixer.music.stop()
    
    #CITATION - https://www.pygame.org/docs/ref/mixer.html
    def fadeout(self):
        pygame.mixer.music.fadeout(2500) #milliseconds
    
    def pause(self):
        pygame.mixer.music.pause()
    
    def unpause(self):
        pygame.mixer.music.unpause()

    def queue(self):
        #SONG - Genesis by Grimes
        pygame.mixer.music.queue('Grimes-_-Genesis.ogg')




# ------------------------------------------------------------------------------
def gameDimensions(app):
    #default values
    rows = 10
    cols = 10
    cellSize = 20
    margin = 100

    return (rows, cols, cellSize, margin)

# from www.cs.cmu.edu/~112/notes/notes-animations-part1.html #exampleGrids
def getCellBounds(app, row, col):
    gridWidth  = app.width - 2*app.margin2
    gridHeight = app.height - 2*app.margin2
    x0 = app.margin2 + gridWidth * col / app.cols
    x1 = app.margin2 + gridWidth * (col+1) / app.cols
    y0 = app.margin2 + gridHeight * row / app.rows
    y1 = app.margin2 + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

def drawCell(app,canvas,row, col, color):
    if color == '#6CAA40': #lighter green color
        cellOutlineWidth = 0
    elif(color == '#22311d'): #dark green color
        cellOutlineWidth = 2
    else:
        cellOutlineWidth = 2
    x0, y0, x1, y1 = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, 
                            outline = 'black', width = cellOutlineWidth)

def drawBoard(app, canvas): 
    for row in range(app.rows):
        for col in range(app.cols):
            color =  app.board[row][col]
            drawCell(app,canvas,row, col, color)

def drawBushes(app, canvas):
    for cell in app.bushes:
        row, col = cell
        x0, y0, x1, y1 = getCellBounds(app, row, col)
        cx, cy = (x0 + x1)//2, (y0 + y1)//2
        canvas.create_image(cx,cy, 
                        image=ImageTk.PhotoImage(app.bush))


# -------------------------------- Player --------------------------------------
def drawGoal(app, canvas):
    #get a random col, it will be placed anywhere in row 0
    drawCell(app,canvas,app.goalRow, app.goalCol, 'red')

def drawPlayer(app, canvas):
    x0, y0, x1, y1 = getCellBounds(app, app.playerRow, app.playerCol)
    cx, cy = (x0 + x1)//2, (y0 + y1)//2
    image = canvas.create_image(cx,cy, 
                         image=ImageTk.PhotoImage(app.playercurrImg))

def movePlayer(app, drow, dcol):
        app.playerRow += drow
        app.playerCol += dcol

    #if move is out of bounds 
        if (app.playerRow < 0 or app.playerRow >= app.rows or 
            app.playerCol < 0 or app.playerCol >= app.cols or 
            app.board[app.playerRow][app.playerCol] == '#22311d'):

                app.playerRow -= drow
                app.playerCol -= dcol

        app.slime.checkMonsterCollision(app)
        app.goblin.checkGobCollision(app)

        if(app.level == 2):
            app.goblin1.checkGobCollision(app)

        elif(app.level == 3):
            app.goblin1.checkGobCollision(app)
            app.slime1.checkMonsterCollision(app)
            app.vampire.checkVampCollision(app)
            app.ghost.checkGhostCollision(app)
            
        elif(app.level == 4):
            app.goblin1.checkGobCollision(app)
            app.vampire.checkVampCollision(app)
            app.slime1.checkMonsterCollision(app)
            app.zombie.checkZomCollision(app)
            app.ghost.checkGhostCollision(app)
            app.ghost1.checkGhostCollision(app)

        elif(app.level == 5):
            app.goblin1.checkGobCollision(app)
            app.vampire.checkVampCollision(app)
            app.vampire1.checkVampCollision(app)
            app.slime1.checkMonsterCollision(app)
            app.zombie.checkZomCollision(app)
            app.zombie1.checkZomCollision(app)
            app.ghost.checkGhostCollision(app)
            app.ghost1.checkGhostCollision(app)

# -------------------------------- Crystals ------------------------------------
def drawCrystals(app, canvas):
  
    #crystals can be different & random colors:
    crystalColors = ['#ffcae5', '#ffaed7', '#ff77bc']
    #pick a random color
    color = random.randrange(3)

    for cell in app.crystalLocations:
        row, col = cell
        x0, y0, x1, y1 = getCellBounds(app, row, col)
        cx, cy = (x0 + x1)//2, (y0 + y1)//2
        
        canvas.create_oval(cx - app.r, cy -app.r, cx + app.r, cy + app.r, 
                           fill = crystalColors[color], outline = '#ff77bc')

def placeCrystals(app):
    count = 0
    maxCrystals = 2**app.level
    while (count != maxCrystals):

        #pick a random cell that is a path, not a wall.
        randomRow = random.randrange(app.rows)
        randomCol = random.randrange(app.cols)
        crystalCell = (randomRow, randomCol)
        
        if(crystalCell in app.maze): #the path
            if(app.board[randomRow][randomCol] != 'red'):
                count += 1
                app.crystalLocations.append((randomRow, randomCol))


def checkCrystalCollection(app):
    playerCell = app.playerRow, app.playerCol
    if(playerCell in app.crystalLocations):
        crystalCollectedSound.play()
        app.crystalsCollected += 1
        app.crystalLocations.remove(playerCell)







    





