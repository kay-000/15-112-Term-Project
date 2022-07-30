# Maze Generation - Prim's Algorithm - this file generates the maze. 
import random
import math

def generateMaze(app):
 
    #1. start w/ a grid 
    wallsL = [] 
    vistedCells = set() 

    #2. pick a random cell
    randomRow = random.randrange(app.rows)
    randomCol = random.randrange(app.cols)
   
    #3. add random cell to the list of visted cells:
    app.maze.add((randomRow,randomCol))
    vistedCells.add((randomRow,randomCol))

    #random cell is the current cell
    row, col = randomRow, randomCol

    #add surrounding walls (aka neighbors)
    neighbors = [(row-1, col),(row+1, col),
                         (row, col-1),(row, col+1)]
    for n in neighbors:
        nRow, nCol = n
        if(isLegal(app, nRow, nCol)): #checks if it's out of bounds
            wallsL.append(n)

    #make sure that the player always has a path at the start:
    pRow, pCol = (app.rows - 1), (app.cols - 1)
    app.maze.add((pRow, pCol))
    app.maze.add((pRow-1, pCol))
    app.maze.add((pRow+1, pCol))
    app.maze.add((pRow, pCol-1))
    app.maze.add((pRow, pCol+1))
    
    #make sure there is always a path to the end goal (underneath)
    app.maze.add((app.goalRow+1, app.goalCol))

    while(len(wallsL) != 0):
        surrList = []
    
        #pick a random wall/neighbor
        currWall = random.choice(wallsL)
        wRow, wCol = currWall

        currNeighbors = [(wRow-1, wCol),(wRow+1, wCol),
                         (wRow, wCol-1),(wRow, wCol+1)]

        #check all the surrounding walls around the current wall.
        for surrounding in currNeighbors:
            #1. keep track of which neighbors are in vistedCells
            #2. if surrounding in visted then add it to a list.
            if surrounding in vistedCells:
                sRow, sCol = surrounding 
                if(isLegal(app, sRow, sCol)):
                    surrList.append(surrounding)
        
        #if two elements in list then do nothing and remove wall from wallsL
        if(len(surrList) == 2):

            if(surrList[0] in wallsL and (surrList[1]) in wallsL):
                wallsL.remove(surrList[0])
                wallsL.remove(surrList[1])

            elif(surrList[0] in wallsL):
                wallsL.remove(surrList[0])

            elif(surrList[1] in wallsL):
                wallsL.remove(surrList[1])

        #if one element in list, then get the opposite cell of currWall. 
        elif(len(surrList) == 1):
            if(surrList[0] == (wRow, wCol+1)):
                oppCell = (wRow, wCol-1)

            elif(surrList[0] == (wRow, wCol-1)):
                oppCell = (wRow, wCol+1)

            elif(surrList[0] == (wRow+1, wCol)):
                oppCell = (wRow-1, wCol)

            elif(surrList[0] == (wRow-1, wCol)):
                oppCell = (wRow+1, wCol)

            oRow, oCol = oppCell

            if(isLegal(app, oRow, oCol)):
            # add it to visted, add to wallsL, and add to maze.
                vistedCells.add(oppCell)
                wallsL.append(oppCell)
                app.maze.add(oppCell)
                app.maze.add(currWall)

            # and add oppCells neighbors to wallsL (add all except currWall)
                oppCellNghbors = [(oRow-1, oCol),(oRow+1, oCol),
                                (oRow, oCol-1),(oRow, oCol+1)]
                
                for oNeighbor in oppCellNghbors:
                    onRow, onCol = oNeighbor
                    if(oNeighbor == currWall):
                        continue
                    elif(isLegal(app, onRow, onCol)):
                        wallsL.append(oNeighbor)
        wallsL.remove(currWall)

    #if there's a wall underneath the goal, remove it
    if(app.board[app.goalRow][app.goalCol] == '#22311d'):
        app.board[app.goalRow][app.goalCol] = 'red'

    #draw the maze now:
    #app.maze draws the PATH
    for cell in app.maze:
        row, col = cell
        if((row >= 0 and row < app.rows) and (col >= 0 and col < app.cols)):
            app.board[row][col] = '#6CAA40'
    
    #get all the walls saved to draw bushes later
    for r in range(len(app.board)):
        for c in range(len(app.board[0])):
            if(app.board[r][c] == '#22311d'):
                app.bushes.append((r, c))
    
# ------------------------------------------------------------------------------

def isLegal(app, row, col):
    #if in bounds:
    if (row >= 0 and row < app.rows and col >= 0 and col < app.cols):
        return True
    #out of bounds:
    else:
        return False
# ------------------------------------------------------------------------------