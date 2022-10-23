#MAIN FILE - This has all the modes + app variables used throughout the project.
#The game should be run in this file. 

#TERM PROJECT 
from cmu_112_graphics import *
from GameDesign import *
from MazeGeneration import *
from MonsterClass import *
from Levels import *

import pygame
pygame.mixer.init()

player = 0 #to save the Player every time the player dies (hard mode)
difficulty = 'Easy' #to save the difficulty every time the app restarts

#CITATION - all hex color codes are from https://htmlcolorcodes.com/color-picker/

#----------------------------- Sound Effects -----------------------------------
# from https://mixkit.co/free-sound-effects/game/
buttonPressSound = pygame.mixer.Sound('buttonPressSound.wav')
playerMovementSound = pygame.mixer.Sound('playerMovement.wav')
crystalCollectedSound = pygame.mixer.Sound('crystalCollected.wav')

#dialogues for Story Mode
dia2 = pygame.mixer.Sound('dialogue/dia2.wav')
dia4 = pygame.mixer.Sound('dialogue/dia4.wav')
dia6 = pygame.mixer.Sound('dialogue/dia6.wav')
dia7 = pygame.mixer.Sound('dialogue/dia7.wav')


# ---------------------------- Splash Screens ----------------------------------

##########################################
# StartScreen
##########################################
def startScreen_redrawAll(app, canvas):
    font = 'Courier 26 bold'
    cx, cy  = (app.width/2, app.height/2)
    shift = 50

    # black start screen background
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black', 
                            outline  = 'black')

    #monsters
    canvas.create_image(cx - 5*shift,cy + 5*shift, 
                          image=ImageTk.PhotoImage(app.vamp))

    #eye gif
    photoImage3 = app.eye[app.spriteCounter3] #left eye
    canvas.create_image(cx - 1.2*shift, cy - 6*shift, image=photoImage3)

    photoImage4 = app.eye[app.spriteCounter4] #right eye
    canvas.create_image(cx + 1.2*shift, cy - 6*shift, image=photoImage4)

    #press start button 
    canvas.create_image(cx,cy + shift, 
                          image=ImageTk.PhotoImage(app.greenButton))

    #press start text
    photoImage = app.pressStart[app.spriteCounter]
    canvas.create_image(cx - .2*shift, cy + shift, image=photoImage)

    #easy mode and hard mode text
    canvas.create_image(cx,cy, 
                         image=ImageTk.PhotoImage(app.gameMode))

    #butterflies
    canvas.create_image(cx - 5*shift,cy - shift, #top butterfly
                        image=ImageTk.PhotoImage(app.butterfly))

    canvas.create_image(cx + 5*shift, cy + 3*shift, 
                        image=ImageTk.PhotoImage(app.butterfly))  

    #game title:
    canvas.create_image(cx,cy - shift, 
                          image=ImageTk.PhotoImage(app.gameTitle))                 

def startScreen_timerFired(app): 
    app.spriteCounter = (1 + app.spriteCounter) % len(app.pressStart)
    app.spriteCounter3 = (1 + app.spriteCounter3) % len(app.eye)
    app.spriteCounter4 = (1 + app.spriteCounter4) % len(app.eye)

def startScreen_mouseMoved(app, event):
    cx, cy  = (app.width/2, app.height/2)
    shift = 50

    if(event.x >= (cx - 2*shift)   and 
       event.x <= (cx + 2*shift)   and 
       event.y >= cy - 2*shift     and 
       event.y <= cy - 1.5*shift):
       app.gameMode = app.easyModeImg

    elif(event.x >= (cx - 2*shift)    and 
        event.x <= (cx + 2*shift)     and 
        event.y >= cy - 1.1*shift       and 
        event.y <= cy - .65*shift):
        app.gameMode = app.hardModeImg
    

def startScreen_mousePressed(app, event):
    cx, cy  = (app.width/2, app.height/2)
    shift = 50
    #these are the coordinates of the green box
    if(event.x >= (cx - 2.9*shift) and 
       event.x <= (cx + 2.95*shift) and 
       event.y >= cy - shift/6     and 
       event.y <= cy + 1.65*shift):
       buttonPressSound.play()
       app.mode = 'pickPlayer'
    
    if(event.x >= (cx - 2*shift)   and 
       event.x <= (cx + 2*shift)   and 
       event.y >= cy - 2*shift     and 
       event.y <= cy - 1.5*shift):
       print("app.difficulty = 'Easy'")
       app.difficulty = 'Easy'

    elif(event.x >= (cx - 2*shift)    and 
        event.x <= (cx + 2*shift)     and 
        event.y >= cy - 1.1*shift       and 
        event.y <= cy - .65*shift):
        app.difficulty = 'Hard'
        print("app.difficulty = 'Hard'")



def startScreen_keyPressed(app, event):
    if(event.key == 'h'):
        app.mode = 'helpMode'

# ------------------------------------------------------------------------------
##########################################
# Pick A Player Mode
##########################################
def pickPlayer_redrawAll(app, canvas):
    font = 'Courier 26 bold'
    cx, cy  = (app.width/2, app.height/2)
    shift = 100
    canvas.create_rectangle(0, 0, app.width, app.height, fill = '#750509', 
                            outline  = 'black') 
    canvas.create_rectangle(app.margin*3, app.margin*3, app.width- app.margin*3, 
                            app.height- app.margin*3, fill = 'dark red', 
                            outline  = '#b1080f', width = 10)

    canvas.create_image(cx,cy - 2*shift, 
                          image=ImageTk.PhotoImage(app.PickPlayer))

    #players
    canvas.create_image(cx - 1.5*shift,cy + shift//9, 
                          image=ImageTk.PhotoImage(app.p1Pick))
    canvas.create_image(cx,cy, 
                          image=ImageTk.PhotoImage(app.p2Pick))
                          
    canvas.create_image(cx + 1.5*shift,cy, 
                          image=ImageTk.PhotoImage(app.p3Pick))
 
def pickPlayer_mousePressed(app, event):
    cx, cy  = (app.width/2, app.height/2)
    shift = 100
    #these are the coordinates of the buttons

    #if player 1 is chosen
    if(event.x >= (cx - 2*shift)   and 
       event.x < (cx - shift)      and 
       event.y >= (cy - .80*shift)  and 
       event.y <= (cy + .80*shift)):
       buttonPressSound.play()
       app.chosenPlayer = 0
       app.playercurrImg = app.p1Back
       levels(app)
       app.mode = 'storyIntro'

    elif(event.x >= (cx - shift//2)   and 
         event.x <  (cx + shift//2)   and 
         event.y >= (cy - .80*shift)  and 
         event.y <= (cy + .80*shift)): #player 2 is chosen
        buttonPressSound.play()
        app.chosenPlayer = 1
        app.playercurrImg = app.p2Back
        levels(app)
        app.mode = 'storyIntro'
    
    elif(event.x >= (cx + shift)      and 
         event.x <  (cx + 2*shift)    and 
         event.y >= (cy - .80*shift)  and 
         event.y <= (cy + .80*shift)): #player 3 is chosen
       buttonPressSound.play()
       app.chosenPlayer = 2
       app.playercurrImg = app.p3Back
       levels(app)
       app.mode = 'storyIntro'
       
def pickPlayer_keyPressed(app, event):
    if(event.key == 'Left'):
        app.mode = 'startScreen'
# ------------------------------------------------------------------------------
##########################################
# Story Intro Mode
##########################################

def storyIntro_redrawAll(app, canvas):
    cx, cy  = (app.width/2, app.height/2)
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    canvas.create_image(cx,cy, 
                         image=ImageTk.PhotoImage(app.loadingTxt))

# app.storyScreens = ['screen1', 'screen2', 'screen3']
def storyIntro_timerFired(app):
    app.timerDelay = 100
    app.count1 += 1

    if(app.count1 == 1):
        app.sound.fadeout()
        #CITATION - SONG: 'Transgender' by Crystal Castles
        app.song = 'Crystal-Castles-_TRANSGENDER_-Official.wav'
        app.sound = Sound(app.song)
        app.sound.start()
        app.sound.queue()

    if (app.count1 == 5):
        app.count1 = 0
        app.mode = 'screen1'
    
#Screen One
def screen1_redrawAll(app, canvas):
    cx, cy  = (app.width/2, app.height/2)
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    canvas.create_image(cx,cy, 
                         image=ImageTk.PhotoImage(app.dialogue1))    
    canvas.create_image(cx,cy - 200, 
                         image=ImageTk.PhotoImage(app.eyePic))

def screen1_timerFired(app):
    app.timerDelay = 100
    app.count1 += 1

    if (app.count1 == 15):
        dia2.play()
        app.count = 0 
        app.mode = 'screen2'

def screen1_keyPressed(app, event):
    if(event.key == 'w'):
        app.mode = 'screen2'


#Screen Two
def screen2_redrawAll(app, canvas):
    cx, cy  = (app.width/2, app.height/2)
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    canvas.create_image(cx,cy, 
                         image=ImageTk.PhotoImage(app.dialogue2))
    canvas.create_image(cx,cy - 200, 
                         image=ImageTk.PhotoImage(app.eyePic))

def screen2_timerFired(app):
    app.timerDelay = 100
    app.count1 += 1

    if (app.count1 == 35):
        app.count1 = 0
        app.mode = 'screen3'

def screen2_keyPressed(app, event):
    if(event.key == 'w'):
        app.mode = 'screen3'

#Screen Three
def screen3_redrawAll(app, canvas):
    cx, cy  = (app.width/2, app.height/2)
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    canvas.create_image(cx,cy, 
                         image=ImageTk.PhotoImage(app.dialogue3))
    canvas.create_image(cx,cy - 200, 
                         image=ImageTk.PhotoImage(app.eyePic))

def screen3_timerFired(app):
    app.timerDelay = 100
    app.count1 += 1

    if (app.count1 == 25):
        dia4.play()
        app.count1 = 0
        app.mode = 'screen4'

def screen3_keyPressed(app, event):
    if(event.key == 'w'):
        app.mode = 'screen4'

#Screen Four
def screen4_redrawAll(app, canvas):
    cx, cy  = (app.width/2, app.height/2)
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    canvas.create_image(cx,cy, 
                         image=ImageTk.PhotoImage(app.dialogue4))
    canvas.create_image(cx,cy - 200, 
                         image=ImageTk.PhotoImage(app.eyePic))

def screen4_timerFired(app):
    app.timerDelay = 100
    app.count1 += 1

    if (app.count1 == 45):
        app.count1 = 0
        app.mode = 'screen5'

def screen4_keyPressed(app, event):
    if(event.key == 'w'):
        app.mode = 'screen5'

#Screen Five 
def screen5_redrawAll(app, canvas):
    cx, cy  = (app.width/2, app.height/2)
    shift = 25
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    canvas.create_image(cx,cy - shift, 
                         image=ImageTk.PhotoImage(app.dialogue5))
    canvas.create_image(cx,cy - 200, 
                         image=ImageTk.PhotoImage(app.eyePic))

def screen5_timerFired(app):
    app.timerDelay = 100
    app.count1 += 1

    if (app.count1 == 20):
        dia6.play()
        app.count1 = 0
        app.mode = 'screen6'

def screen5_keyPressed(app, event):
    if(event.key == 'w'):
        app.mode = 'screen6'

#Screen Six
def screen6_redrawAll(app, canvas):
    cx, cy  = (app.width/2, app.height/2)
    shift = 50
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    canvas.create_image(cx,cy + 2.7*shift, 
                         image=ImageTk.PhotoImage(app.dialogue6))
    canvas.create_image(cx,cy - 200, 
                         image=ImageTk.PhotoImage(app.eyePic))

def screen6_timerFired(app):
    app.timerDelay = 100
    app.count1 += 1

    if (app.count1 == 125):
        dia7.play()
        app.count1 = 0
        app.mode = 'screen7'

def screen6_keyPressed(app, event):
    if(event.key == 'w'):
        app.mode = 'screen7'

#Screen Seven 
def screen7_redrawAll(app, canvas):
    cx, cy  = (app.width/2, app.height/2)
    shift = 50
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    canvas.create_image(cx,cy + 3*shift, 
                         image=ImageTk.PhotoImage(app.dialogue7))
    canvas.create_image(cx,cy - 200, 
                         image=ImageTk.PhotoImage(app.eyePic))

def screen7_timerFired(app):
    app.timerDelay = 100
    app.count1 += 1

    if (app.count1 == 75):
        app.count1 = 0
        app.helpScreenPlayer = getSpriteDirection(app,app.chosenPlayer, 'Front')
        app.mode = 'helpMode'

def screen7_keyPressed(app, event):
    if(event.key == 'w'):
        app.helpScreenPlayer = getSpriteDirection(app,app.chosenPlayer, 'Front')
        app.mode = 'helpMode'

# ------------------------------------------------------------------------------
##########################################
# Help Mode
##########################################

def helpMode_redrawAll(app, canvas):
    cx, cy  = (app.width/2, app.height/2)
    shift = 100
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'orange')
    canvas.create_image(cx,cy, 
                         image=ImageTk.PhotoImage(app.Instructions))

    image = canvas.create_image(cx,cy - 2.2*shift, 
                         image=ImageTk.PhotoImage(app.helpScreenPlayer))

    canvas.create_rectangle(cx - 1.5*shift, cy + 3.4*shift, cx + 1.5*shift,cy + 3.85*shift, 
                            fill = 'light blue', outline = 'blue', width = 4)

    canvas.create_text(cx + shift//25, cy + 3.6*shift,
                       fill = 'black',text = 'Click Any Key To Go To Game',
                       font = 'Courier 16 bold')

def helpMode_keyPressed(app, event):
    app.helpScreenPlayer
    if event.key == "Up":        
        app.helpScreenPlayer = getSpriteDirection(app,app.chosenPlayer, 'Back')
        playerMovementSound.play()

    elif event.key == "Down":    
        app.helpScreenPlayer = getSpriteDirection(app,app.chosenPlayer, 'Front')
        playerMovementSound.play()

    elif event.key == "Left":    
        app.helpScreenPlayer = getSpriteDirection(app,app.chosenPlayer, 'Left')
        playerMovementSound.play()

    elif event.key == "Right":   
        app.helpScreenPlayer = getSpriteDirection(app,app.chosenPlayer, 'Right')
        playerMovementSound.play()

    else:
        app.sound.unpause()
        app.mode = 'gameMode'

# ------------------------------------------------------------------------------
##########################################
# Final Boss Mode
##########################################
def finalBoss_redrawAll(app, canvas):
    font = 'Courier 32 bold'
    cx, cy = app.width/2, app.height/2
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    canvas.create_image(cx,cy - 200, 
                         image=ImageTk.PhotoImage(app.witchPic))

    lossTxt = f'''\n




        WHAT!?! You only give me 
                {app.crystalsCollected} crystals 

        and you expect me to HELP YOU?! 

        I will NOT, you are stuck 
        in this forest for eternity!
        '''

    winTxt = f'''\n






        WOW! You gave me {app.crystalsCollected} crystals!


        I will make a potion that 
        creates a portal.

        You will return home shortly. 

        '''


    if(app.crystalsCollected < 35):
        canvas.create_text(cx - 50, cy, 
                           text= lossTxt,
                           font=font, fill='white')
    
    elif(app.crystalsCollected >= 35):
        canvas.create_text(cx - 50, cy, 
                           text= winTxt,
                           font='Courier 28 bold', fill='white')
   
def finalBoss_timerFired(app):
    app.count1 += 1

    if (app.count1 == 30):
        app.count1 = 0
        app.sound.stop()

        if(app.crystalsCollected < 35):
            pass
        else:
            #SONG - Count Contessa by Azealia Banks 
            app.song = 'CountContessa.wav'
            app.sound = Sound(app.song)
            app.sound.start()
        app.mode = 'gameEnd'

##########################################
# Game End Mode
##########################################
def gameEnd_redrawAll(app, canvas): 
    cx, cy = app.width/2, app.height/2
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')

    if(app.crystalsCollected < 35):
        canvas.create_text(cx, cy - 200, 
                           text= "YOU DIDN'T MAKE IT HOME :(",
                           font= 'Lato 40 bold', fill='red')
    
    elif(app.crystalsCollected >= 35):
        canvas.create_text(cx, cy - 200, 
                           text= 'YOU MADE IT HOME!',
                           font='Lato 40 bold', fill='light green')
    
    canvas.create_text(cx, cy - 75, 
                           text= 'Want To Play Again?',
                           font='Lato 30 bold', fill='white')
    canvas.create_image(cx,cy + 50, 
                          image=ImageTk.PhotoImage(app.greenButton))
    #press start text
    photoImage = app.pressStart[app.spriteCounter]
    canvas.create_image(cx - .2*50, cy + 50, image=photoImage)

def gameEnd_mousePressed(app, event):
    cx, cy  = (app.width/2, app.height/2)
    shift = 50
    #these are the coordinates of the green box
    if(event.x >= (cx - 2.9*shift) and 
       event.x <= (cx + 2.95*shift) and 
       event.y >= cy - shift/6     and 
       event.y <= cy + 1.65*shift):
       buttonPressSound.play()
       appStarted(app)
       app.mode = 'startScreen'

def gameEnd_timerFired(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.pressStart)
    
# ------------------------------------------------------------------------------

##########################################
# Game Mode
##########################################
def gameMode_mousePressed(app, event):
    cx, cy  = (app.width/2, app.height/2)
    if(app.YouLose):
        shift = 100
        if(event.x >= (cx - 1.5*shift) and 
           event.x <= (cx + 1.5*shift) and 
           event.y >=  cy + shift//2  and 
           event.y <=  cy + shift):
            if(app.difficulty == 'Hard'):
                app.YouLose = False
                player = app.chosenPlayer
                difficulty = app.difficulty
                appStarted(app)
                app.sound.stop()
                app.song = 'Crystal-Castles-_TRANSGENDER_-Official.wav'
                app.sound = Sound(app.song)
                app.sound.start()
                app.sound.queue()
                app.chosenPlayer = player
                app.difficulty = difficulty
                app.playercurrImg = getSpriteDirection(app,app.chosenPlayer, 'Back')
                levels(app)
                app.mode = 'gameMode'

            elif(app.difficulty == 'Easy'):
                app.YouLose = False
                app.bush = loadImage(app,'sprites/bush.png', 2/7)
                resetMonsterScale(app)
                resetPlayer(app)

                if(app.level == 3):
                    app.bush = app.scaleImage(app.bush, 2/3)
                    # rescalePlayer(app, 3/4)
                    # rescaleMonsters(app, 3/4)

                elif(app.level == 4):
                    rescalePlayer(app, 3/4)
                    rescaleMonsters(app, 3/4)
                    app.bush = app.scaleImage(app.bush, 3/4)
                    app.bush = app.scaleImage(app.bush, 3/4)

                elif(app.level ==5):
                    rescalePlayer(app, 3/4)
                    rescaleMonsters(app, 3/4)
                    app.bush = app.scaleImage(app.bush, 3/4)
                    app.bush = app.scaleImage(app.bush, 3/4)
                    app.bush = app.scaleImage(app.bush, .75)

                levels(app)


    r = 20
    if( event.x >= (1.5*cx - r) and 
        event.x <= (1.5*cx + r) and 
        event.y >= (cy/7 - r  ) and 
        event.y <= (cy/7  + r ) ):
        appStarted(app)
        app.mode = 'startScreen'
   
    elif(event.x >= (1.7*cx - r) and 
        event.x <= (1.7*cx + r) and 
        event.y >= (cy/7 - r  ) and 
        event.y <= (cy/7  + r ) ):
        app.sound.pause()
        app.helpScreenPlayer = getSpriteDirection(app,app.chosenPlayer, 'Front')
        app.mode = 'helpMode'
    
    elif(event.x >= (1.9*cx - r) and 
        event.x <= (1.9*cx + r) and 
        event.y >= (cy/7 - r  ) and 
        event.y <= (cy/7  + r )):
        app.pauseMusic = not(app.pauseMusic) 
        print('music button pressed')
        print('app.pauseMusic = ', app.pauseMusic)
        if(app.pauseMusic):
            app.sound.pause()
        else:
            app.sound.unpause()


def gameMode_keyPressed(app, event):
    drow, dcol = 0, 0

    if event.key == "Up":        
        drow, dcol = -1, 0
        app.playercurrImg = getSpriteDirection(app,app.chosenPlayer, 'Back')
        playerMovementSound.play()

    elif event.key == "Down":    
        drow, dcol = +1, 0
        app.playercurrImg = getSpriteDirection(app,app.chosenPlayer, 'Front')
        playerMovementSound.play()

    elif event.key == "Left":    
        drow, dcol = 0, -1
        app.playercurrImg = getSpriteDirection(app,app.chosenPlayer, 'Left')
        playerMovementSound.play()

    elif event.key == "Right":   
        drow, dcol = 0, +1
        app.playercurrImg = getSpriteDirection(app,app.chosenPlayer, 'Right')
        playerMovementSound.play()
    
    elif event.key == 's':
        app.song = 'Sewerslvt-Ecifircas.wav'
        app.sound = Sound(app.song)
        app.sound.start()
        app.crystalsCollected = 15
        app.mode = 'finalBoss'

    elif event.key == 'a':
        app.song = 'Sewerslvt-Ecifircas.wav'
        app.sound = Sound(app.song)
        app.sound.start()
        app.crystalsCollected = 40
        app.mode = 'finalBoss'
    
    movePlayer(app, drow, dcol)
    checkIfLevelDone(app)
    checkCrystalCollection(app)

def gameMode_timerFired(app):
        if(app.YouLose):
            return
        app.timerDelay = 350
     
        app.slime.moveMonsterUpDown(app)
        app.slime.checkMonsterCollision(app)

        app.goblin.moveGoblin(app)
        app.goblin.checkGobCollision(app)

        if(app.level == 2):
            app.goblin1.moveGoblin(app)
            app.goblin1.checkGobCollision(app)

            app.slime1.moveMonsterUpDown(app)
            app.slime1.checkMonsterCollision(app)

        elif(app.level == 3):
            app.goblin1.moveGoblin(app)
            app.goblin1.checkGobCollision(app)

            app.slime1.moveMonsterUpDown(app)
            app.slime1.checkMonsterCollision(app)

            app.vampire.moveVampire(app)
            app.vampire.checkVampCollision(app)

            app.ghost.moveGhost(app)
            app.ghost.checkGhostCollision(app)
            
        elif(app.level == 4):
            app.goblin1.moveGoblin(app)
            app.goblin1.checkGobCollision(app)

            app.vampire.moveVampire(app)
            app.vampire.checkVampCollision(app)

            app.slime1.moveMonsterUpDown(app)
            app.slime1.checkMonsterCollision(app)

            app.zombie.moveZombie(app)
            app.zombie.checkZomCollision(app)

            app.ghost.moveGhost(app)
            app.ghost.checkGhostCollision(app)

            app.ghost1.moveGhost(app)
            app.ghost1.checkGhostCollision(app)

        elif(app.level == 5):
            app.goblin1.moveGoblin(app)
            app.goblin1.checkGobCollision(app)

            app.vampire.moveVampire(app)
            app.vampire.checkVampCollision(app)

            app.vampire1.moveVampire(app)
            app.vampire1.checkVampCollision(app)

            app.slime1.moveMonsterUpDown(app)
            app.slime1.checkMonsterCollision(app)

            app.zombie.moveZombie(app)
            app.zombie.checkZomCollision(app)

            app.zombie1.moveZombie(app)
            app.zombie1.checkZomCollision(app)

            app.ghost.moveGhost(app)
            app.ghost.checkGhostCollision(app)

            app.ghost1.moveGhost(app)
            app.ghost1.checkGhostCollision(app)
            

def gameMode_redrawAll(app, canvas):
    r = 20
    cx, cy  = (app.width/2, app.height/2)
    
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'dark green', 
                            outline  = 'black')
    canvas.create_rectangle(app.margin*3, app.margin*3, app.width- app.margin*3, 
                            app.height- app.margin*3, fill = 'black', 
                            outline  = 'black')

    drawBoard(app, canvas)
    drawBushes(app, canvas)
    drawGoal(app, canvas)
    drawCrystals(app, canvas)
    drawPlayer(app, canvas)
    app.slime.drawMonster(app, canvas)
    app.goblin.drawGoblin(app, canvas)

    if(app.level == 2):
        app.goblin1.drawGoblin(app, canvas)
        app.slime1.drawMonster(app, canvas)
    
    elif(app.level == 3):
        app.goblin1.drawGoblin(app, canvas)
        app.vampire.drawVampire(app, canvas)
        app.slime1.drawMonster(app, canvas)
        app.ghost.drawGhost(app, canvas)
        
    elif(app.level == 4):
        app.goblin1.drawGoblin(app, canvas)
        app.vampire.drawVampire(app, canvas)
        app.ghost.drawGhost(app, canvas)
        app.ghost1.drawGhost(app, canvas)
        app.slime1.drawMonster(app, canvas)
        app.zombie.drawZombie(app, canvas)

    elif(app.level == 5):
        app.slime1.drawMonster(app, canvas)
        app.goblin1.drawGoblin(app, canvas)
        app.vampire.drawVampire(app, canvas)
        app.vampire1.drawVampire(app, canvas)
        app.ghost.drawGhost(app, canvas)
        app.ghost1.drawGhost(app, canvas)
        app.zombie.drawZombie(app, canvas)
        app.zombie1.drawZombie(app, canvas)


    #Current Level
    shift = 100
    canvas.create_text(cx,cy - 3.7*shift, 
                        text=f'Current Level: {app.level}',
                        fill="#22311d", font='Arial 26 bold')
    #Crystals Collected
    canvas.create_text(cx,cy - 3.4*shift, 
                        text=f'Crystals Collected: {app.crystalsCollected}',
                        fill="#22311d", font='Arial 26 bold')
    #Lives
    canvas.create_text(cx - 3*shift,cy - 3.4*shift, 
                        text=f'Lives: {app.lives}',
                        fill="#22311d", font='Arial 26 bold')

    #icons: home, help, music
    canvas.create_oval(1.5*cx - r, cy/7 - r, 1.5*cx + r, cy/7  + r,
                       fill='#4a6741', outline='#22311d', width = r/4)
    canvas.create_text((1.5*cx + 1.5*cx)//2, (cy/7 +cy/7)//2, 
                        text='⌂',fill="#22311d", font='Arial 26 bold')    

    canvas.create_oval(1.7*cx - r, cy/7 - r, 1.7*cx + r, cy/7  + r,
                       fill='#4a6741', outline='#22311d', width = r/4)
    canvas.create_text((1.7*cx + 1.7*cx)//2, (cy/7 +cy/7)//2, 
                        text='?',fill="#22311d", font='Arial 26 bold') 
    #crystal note
    canvas.create_text(cx, cy + 3.5*shift, 
                        text='35 crystals total are needed to return home',fill="#22311d", font='Lato 15 bold')

    if(app.pauseMusic):
        txt = ' ▷'
        
    else:
        txt = '||'
    canvas.create_oval(1.9*cx - r, cy/7 - r, 1.9*cx + r, cy/7  + r,
                       fill='#4a6741', outline='#22311d', width = r/4)
    canvas.create_text((1.9*cx + 1.9*cx)//2, (cy/7 +cy/7)//2, 
                        text=txt,fill="#22311d", font='Arial 23 bold')
    
    if(app.YouLose):
        canvas.create_rectangle(app.margin*5, app.margin*8, app.width-app.margin*5, 
                            app.height-app.margin*8, fill = 'dark red', 
                            outline  = '#4A0404', width = 10)
        canvas.create_text(cx, cy - shift//4, 
                        text='YOU DIED',fill= "#4A0404", font='Courier 70 bold')
        
        canvas.create_rectangle(cx - 1.5*shift, cy + shift//2, cx + 1.5*shift, cy + shift, 
                                fill = '#800000', 
                                outline  = '#4A0404', width = 5)

        canvas.create_text(cx, cy + .75*shift, 
                        text='CLICK TO TRY AGAIN',fill="#4A0404",font='Courier 24 bold')     
                        
# ------------------------------------------------------------------------------
##########################################
# Main App
##########################################

def appStarted(app):
    #music
    app.pauseMusic = False 
    app.song = "forestFyre.wav"
    app.sound = Sound(app.song)
    app.sound.start()

    # --------------------------gif & images------------------------------------
    app.spriteCounter = 0
    app.spriteCounter2 = 0
    app.spriteCounter3 = 0
    app.spriteCounter4 = 0

    app.pressStart = loadAnimatedGif('gifs/pressStart.gif')

    # https://www.pixilart.com/art/eye-opening-cf5d43a0902e5e7
    app.eye = loadAnimatedGif('gifs/eye.gif')
    
    #https://www.istockphoto.com/photo/scary-vampire-man-on-dark-background-gm1277109819-376409661
    app.vamp = loadImage(app, 'monsters/vampire.png')

    app.gameTitle = loadImage(app, 'images/title.png')
    app.gameMode = loadImage(app, 'images/easyHardMode.png')
    app.easyModeImg = loadImage(app, 'images/easyModeChosen.png')
    app.hardModeImg = loadImage(app, 'images/hardModeChosen.png')

    app.greenButton = loadImage(app, 'images/pixel_art (green).png', 2/4)
    app.butterfly = loadImage(app, 'images/pixel_art (1) copy.png', 2/6) 
    app.loadingTxt = loadImage(app, 'images/Loading.png')
    app.PickPlayer = loadImage(app, 'images/PickPlayer.png')
    app.Instructions = loadImage(app, 'images/Instructions.png', .82)
    app.eyePic = loadImage(app, 'images/eyeImg.png', 3)

    #FROM - https://www.shutterstock.com/image-vector/scary-witch-head-purple-hat-vintage-1815296378?irclickid=VCQR%3APQ3mxyIRCJ33oUxgVIDUkGX9A0X0Xdm0E0&irgwc=1&utm_medium=Affiliate&utm_campaign=vectorified&utm_source=2201181&utm_term=&c3ch=Affiliate&c3nid=IR-2201181
    app.witchPic = loadImage(app, 'images/witch.png', 2/3)
 
    #this generator was used to create my sprites: 
    #https://sanderfrenken.github.io/Universal-LPC-Spritesheet-Character-Generator/

    #player 1 sprites:
    app.p1Fr = loadImage(app,'sprites/player1Fr.png') 
    app.p1Back = loadImage(app,'sprites/player1Back.png')
    app.p1Left = loadImage(app,'sprites/player1Left.png')
    app.p1Right = loadImage(app,'sprites/player1right.png')

    #player 2 sprites:
    app.p2Fr = loadImage(app,'sprites/player2Fr.png')
    app.p2Back = loadImage(app,'sprites/player2Back.png') 
    app.p2Left = loadImage(app,'sprites/player2Left.png')
    app.p2Right = loadImage(app,'sprites/player2right.png')

    # player 3 sprites:
    app.p3Fr = loadImage(app,'sprites/player3Fr.png')
    app.p3Back = loadImage(app,'sprites/player3Back.png') 
    app.p3Left = loadImage(app,'sprites/player3Left.png')
    app.p3Right = loadImage(app,'sprites/player3right.png')

    #Monster Sprites:
    app.gobLeft = loadImage(app,'sprites/gobLeft.png', .98)
    app.gobRight = loadImage(app,'sprites/gobRight.png',.98)
    app.ghostBack = loadImage(app,'sprites/ghostBack.png', .98)
    app.ghostFr = loadImage(app,'sprites/ghostFr.png', .98)
    app.slimeFr = loadImage(app,'sprites/slimeFr.png', 1/4)
    app.slimeBack = loadImage(app,'sprites/slimeBack.png', 1/4)
    app.vampFr = loadImage(app,'sprites/vampFr.png',.98)
    app.vampBack = loadImage(app,'sprites/vampBack.png',.98)
    app.zomFr = loadImage(app,'sprites/zomFr.png',.98)
    app.zomBack = loadImage(app,'sprites/zomBack.png',.98)
    app.zomRight = loadImage(app,'sprites/zomRight.png',.98)
    app.zomLeft = loadImage(app,'sprites/zomLeft.png',.98)

    #For Pick a Player Screen
    app.p1Pick = app.scaleImage(app.p1Fr, 2.5)
    app.p2Pick = app.scaleImage(app.p2Fr, 2.5)
    app.p3Pick = app.scaleImage(app.p3Fr, 2.5)

    app.chosenPlayer = None
    app.playercurrImg = None
    app.helpScreenPlayer = None

    #FROM - http://pixelartmaker.com/art/25a3c9d33e60413
    app.bush = loadImage(app,'sprites/bush.png', 2/7 )
    
    #---------------------------------------------------------------------------
    #other
    app.margin = 30
    app.mode = 'startScreen'
    app.count = 0
    app.storyScreens = ['screen1', 'screen2', 'screen3']
    app.storyIndex = 0
    
    #story mode counters (to change text):
    app.count1 = 0

    #story mode texts (in images): 
    #SOURCE - images were created using google draw. 
    app.dialogue1 = loadImage(app,'dialogue/dia1.png', 0.7)
    app.dialogue2 = loadImage(app,'dialogue/dia2.png', 0.7) 
    app.dialogue3 = loadImage(app,'dialogue/dia3.png', 0.7)
    app.dialogue4 = loadImage(app,'dialogue/dia4.png', 0.7)
    app.dialogue5 = loadImage(app,'dialogue/dia5.png', 0.7)
    app.dialogue6 = loadImage(app,'dialogue/dia6.png', 0.7)
    app.dialogue7 = loadImage(app,'dialogue/dia7.png', 0.7)

    #for game
    app.rows, app.cols, app.cellSize, app.margin2 = gameDimensions(app)
    app.playerRow, app.playerCol = app.rows-1, app.cols-1
    app.goalRow, app.goalCol = 0, random.randrange(app.cols)
    
    app.maze = set()
    app.level = 1
    app.lives = 4
    app.YouLose = False
    app.difficulty = "Easy"

    app.r = 10 #radius
    app.emptyColor = '#22311d'
    app.board =[([app.emptyColor] * app.cols) for row in range(app.rows)]
    app.bushes = []
    app.crystalLocations = []
    app.crystalsCollected = 0

def appStopped(app):
    app.sound.stop()
    pass

#This returns the player image you want.
#sprite is a number (index) and direction is a string
def getSpriteDirection(app,sprite, direction):
    #in order: p1, p2,  p3, goblin, ghost, vampire, zombie
    #           0  1    2    3       4         5      6

    frontFacingSprites = [app.p1Fr, app.p2Fr, app.p3Fr]
    backSprites = [app.p1Back, app.p2Back, app.p3Back]
    leftSprites = [app.p1Left, app.p2Left, app.p3Left]
    rightSprites = [app.p1Right, app.p2Right, app.p3Right]

    if(direction == 'Front'):
        return frontFacingSprites[sprite]
    
    elif(direction == 'Back'):
        return backSprites[sprite]
    
    elif(direction == 'Left'):
        return leftSprites[sprite]

    elif(direction == 'Right'):
        return rightSprites[sprite]

def resetPlayer(app):
    #player 1 sprites:
    app.p1Fr = loadImage(app,'sprites/player1Fr.png') 
    app.p1Back = loadImage(app,'sprites/player1Back.png')
    app.p1Left = loadImage(app,'sprites/player1Left.png')
    app.p1Right = loadImage(app,'sprites/player1right.png')

    #player 2 sprites:
    app.p2Fr = loadImage(app,'sprites/player2Fr.png')
    app.p2Back = loadImage(app,'sprites/player2Back.png') 
    app.p2Left = loadImage(app,'sprites/player2Left.png')
    app.p2Right = loadImage(app,'sprites/player2right.png')

    # player 3 sprites:
    app.p3Fr = loadImage(app,'sprites/player3Fr.png')
    app.p3Back = loadImage(app,'sprites/player3Back.png') 
    app.p3Left = loadImage(app,'sprites/player3Left.png')
    app.p3Right = loadImage(app,'sprites/player3right.png')

def resetMonsterScale(app):
    app.gobLeft = loadImage(app,'sprites/gobLeft.png', .98)
    app.gobRight = loadImage(app,'sprites/gobRight.png',.98)
    app.ghostBack = loadImage(app,'sprites/ghostBack.png', .98)
    app.ghostFr = loadImage(app,'sprites/ghostFr.png', .98)
    app.slimeFr = loadImage(app,'sprites/slimeFr.png', 1/4)
    app.slimeBack = loadImage(app,'sprites/slimeBack.png', 1/4)
    app.vampFr = loadImage(app,'sprites/vampFr.png',.98)
    app.vampBack = loadImage(app,'sprites/vampBack.png',.98)
    app.zomFr = loadImage(app,'sprites/zomFr.png',.98)
    app.zomBack = loadImage(app,'sprites/zomBack.png',.98)
    app.zomRight = loadImage(app,'sprites/zomRight.png',.98)
    app.zomLeft = loadImage(app,'sprites/zomLeft.png',.98)

#I made this method to make it easier to load and scale images
def loadImage(app, png, scale = 1):
    img1 = app.loadImage(png)
    img2 = app.scaleImage(img1, scale)
    return img2

# source: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
def loadAnimatedGif(path):
    # load first sprite outside of try/except to raise file-related exceptions
    spritePhotoImages = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            spritePhotoImages.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e:
            return spritePhotoImages

runApp(width=800, height=800)
