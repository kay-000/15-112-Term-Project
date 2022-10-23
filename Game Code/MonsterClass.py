#Monster Class
from GameDesign import *
import random

#CITATION - all monsters were created using this sprite generator:
# https://sanderfrenken.github.io/Universal-LPC-Spritesheet-Character-Generator/#?body=Humanlike_white

#--------------------------- Monster Sounds ------------------------------------

# from https://mixkit.co/free-sound-effects/game/
zomSound = pygame.mixer.Sound('zomSound.wav')
slimeSound = pygame.mixer.Sound('slimeSound.wav')
ghostSound = pygame.mixer.Sound('ghostSound.mp3')
gobSound = pygame.mixer.Sound('gobSound.wav')
vampSound = pygame.mixer.Sound('vampSound.wav')


#-------------------------------------------------------------------------------


#all monsters have a color
class Monster():
    def __init__(self, app):
        self.color = 'orange' #default color - i'll call these slimes
        self.monsterRow, self.monsterCol = self.getMonsterRowCol(app)
        self.monsterIndex = 3
        self.monsterImg = getSpriteDirection(app, self.monsterIndex, 'Front')
        self.monsterSound = slimeSound
        self.direction = 1

    def getMonsterRowCol(self, app):
        while True:
            randRow, randCol = random.randrange(app.rows), random.randrange(app.cols)
            if(app.board[randRow][randCol] == '#6CAA40' and 
               self.isLegal(app, randRow, randCol)): 
                row, col = randRow, randCol
                break
            else:
                continue    
        return row, col
    
    #a monster placement is legal if:
    #   1. not between two walls
    #   2. not bounded between a wall and an edge
    def isLegal(self, app, row, col):
        
        #for the row
        if(self.inBounds(app, row+1, col) and self.inBounds(app, row-1, col)):
            if(app.board[row+1][col] != '#6CAA40' and 
               app.board[row-1][col] !='#6CAA40'):
                return False
        
        elif(row+1 >= app.rows and row-1 >=0): #bounded below but not on top
            if(app.board[row-1][col] !='#6CAA40'):
                return False

        elif(row-1 < 0 and row+1 >=0): #bounded above but not below
            if(app.board[row+1][col] !='#6CAA40'):
                return False
                    
        #for cols
        if(self.inBounds(app, row, col+1) and self.inBounds(app, row, col-1)):
            if(app.board[row][col+1] != '#6CAA40' and 
               app.board[row][col-1] !='#6CAA40'):
                return False

        elif(col+1 >= app.cols and col-1 >=0): #bounded right but not left
            if(app.board[row][col-1] !='#6CAA40'):
                return False

        elif(col-1 < 0 and col+1 >=0): #bounded left but right
            if(app.board[row][col+1] !='#6CAA40'):
                return False

        #it cannot be placed in the players starting position
        pRow, pCol = (app.rows - 1), (app.cols - 1)
        playerSurrounding = {(pRow, pCol), (pRow-1, pCol), 
                             (pRow+1, pCol),(pRow, pCol-1),(pRow, pCol+1)}
        #add all possible. 
        if((row, col) in playerSurrounding):
            return False

        return True

    def inBounds(self, app, row, col):
        #if in bounds:
        if (row >= 0 and row < app.rows and col >= 0 and col < app.cols):
            return True
        #out of bounds:
        else:
            return False

    def checkMonsterCollision(self,app):
        row, col = app.playerRow, app.playerCol
        mRow, mCol = self.monsterRow, self.monsterCol
        if((row, col) == (mRow, mCol)):
            self.monsterSound.play()
            app.lives -= 1
            if(app.lives == 1):
                app.playerRow, app.playerCol = app.rows-1, app.cols-1

            if(app.lives == 0):
                app.YouLose = True
                return 
                
    def drawMonster(self,app,canvas): 
        shift = 10
        x0, y0, x1, y1 = getCellBounds(app, self.monsterRow, self.monsterCol)
        cx, cy = (x0 + x1)//2, ((y0 + y1)//2) - shift
        image = canvas.create_image(cx,cy, 
                            image=ImageTk.PhotoImage(self.monsterImg))

    def moveMonsterUpDown(self, app):
            if(self.direction == -1):
                self.monsterImg = getSpriteDirection(app, self.monsterIndex, 'Back')
            else:
                self.monsterImg = getSpriteDirection(app, self.monsterIndex, 'Front')
            #move up and down 
            self.monsterRow += self.direction
            self.monsterCol += 0

           #if move is out of bounds.
            if (self.monsterRow < 0  or self.monsterCol < 0):
                self.monsterRow = 0
                self.direction *= -1

            elif(self.monsterRow >= (app.rows) or self.monsterCol >= app.cols):
                self.monsterRow = app.rows-1
                self.direction *= -1

            elif(app.board[self.monsterRow][self.monsterCol] != '#6CAA40'):
                self.direction *= -1
                self.monsterRow += self.direction

    def moveMonsterLeftRight(self, app):
            if(self.direction == -1):
                self.monsterImg = getSpriteDirection(app, self.monsterIndex, 'Left')
            else:
                self.monsterImg = getSpriteDirection(app, self.monsterIndex, 'Right')
            #move up and down 
            self.monsterRow += 0
            self.monsterCol += self.direction

        #if move is out of bounds 
            if (self.monsterRow < 0  or self.monsterCol < 0):
                self.monsterCol = 0
                self.direction *= -1

            elif(self.monsterRow >= (app.rows) or self.monsterCol >= (app.cols)):
                self.monsterCol = app.cols-1
                self.direction *= -1

            elif(app.board[self.monsterRow][self.monsterCol] != '#6CAA40'):
                self.direction *= -1
                self.monsterCol += self.direction
            
            
class Goblin(Monster):
    def __init__(self,app):
        super().__init__(app)
        self.color = 'light green'
        self.monsterRow, self.monsterCol = super(Goblin,self).getMonsterRowCol(app)
        self.monsterIndex = 4
        self.monsterImg = getSpriteDirection(app, self.monsterIndex, 'Left')
        self.monsterSound = gobSound

    def drawGoblin(self,app,canvas): 
        super(Goblin,self).drawMonster(app,canvas)

    def moveGoblin(self, app):
        super(Goblin, self).moveMonsterLeftRight(app)

    def checkGobCollision(self,app):
        super(Goblin, self).checkMonsterCollision(app)
    
class Zombie(Monster):
    def __init__(self,app):
        self.color = 'dark green'
        self.monsterRow, self.monsterCol = super(Zombie,self).getMonsterRowCol(app)
        self.monsterIndex = 7
        self.monsterImg = getSpriteDirection(app, self.monsterIndex, 'Front')
        self.monsterSound = zomSound
        self.direction = 1

    def drawZombie(self,app,canvas): 
        super(Zombie,self).drawMonster(app,canvas)

    def moveZombie(self, app):
        choice = random.randrange(2)
        if(choice == 0):
            super(Zombie, self).moveMonsterLeftRight(app)
        else:
            super(Zombie, self).moveMonsterUpDown(app)

    def checkZomCollision(self,app):
        super(Zombie, self).checkMonsterCollision(app)

class Vampire(Monster):
    def __init__(self,app):
        self.color = 'grey'
        self.monsterRow, self.monsterCol = super(Vampire,self).getMonsterRowCol(app)
        self.monsterIndex = 6
        self.monsterImg = getSpriteDirection(app, self.monsterIndex, 'Front')
        self.monsterSound = vampSound
        self.direction = 1
    
    def drawVampire(self,app,canvas): 
        super(Vampire,self).drawMonster(app,canvas)

    def moveVampire(self, app):
        super(Vampire, self).moveMonsterUpDown(app)

    def checkVampCollision(self,app):
        super(Vampire, self).checkMonsterCollision(app)
        
class ghost(Monster):
    def __init__(self,app):
        self.color = 'white'
        self.monsterRow, self.monsterCol = super(ghost,self).getMonsterRowCol(app)
        self.monsterIndex = 5
        self.monsterImg = getSpriteDirection(app, self.monsterIndex, 'Front')
        self.monsterSound = ghostSound
        self.direction = 1
    
    def drawGhost(self,app,canvas): 
        super(ghost,self).drawMonster(app,canvas)

    def moveGhost(self, app):
        super(ghost, self).moveMonsterUpDown(app)
    
    def checkGhostCollision(self,app):
        super(ghost, self).checkMonsterCollision(app)
    
class la_Llorona(Monster): #maybe final boss ??? 
    def __init__(self,app):
        self.color = 'black'
        self.monsterRow, self.monsterCol = self.getMonsterRowCol(app)
        self.direction = 1

#This returns the sprite image you want.
#sprite is a number (index) and direction is a string
def getSpriteDirection(app,sprite, direction):
    #in order: p1, p2,  p3, slime   goblin,   ghost, vampire, zombie
    #           0  1    2     3       4         5      6       7

    frontFacingSprites = [app.p1Fr, app.p2Fr, app.p3Fr, app.slimeFr,0, app.ghostFr, app.vampFr, app.zomFr]
    backSprites = [app.p1Back, app.p2Back, app.p3Back, app.slimeBack,0, app.ghostBack, app.vampBack, app.zomBack]
    leftSprites = [app.p1Left, app.p2Left, app.p3Left, 0, app.gobLeft, 0, 0, app.zomLeft]
    rightSprites = [app.p1Right, app.p2Right, app.p3Right, 0, app.gobRight, 0, 0, app.zomRight]

    if(direction == 'Front'):
        return frontFacingSprites[sprite]
    
    elif(direction == 'Back'):
        return backSprites[sprite]
    
    elif(direction == 'Left'):
        return leftSprites[sprite]

    elif(direction == 'Right'):
        return rightSprites[sprite]
