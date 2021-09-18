
from tkinter import *
import random

def mousePressed(event):
    redrawAll()

def keyPressed(event):
    if (event.keysym == "r"):
        init()
    if (event.keysym == "p"):
        canvas.data.paused = not (canvas.data.paused)
    elif canvas.data.isGameOver == False and canvas.data.paused == False:
        if (event.keysym == "Left"):
            moveFallingPiece(0,-1)
        elif (event.keysym == "Right"):
            moveFallingPiece(0,+1)
        elif (event.keysym == "Down"):
            moveFallingPiece(+1,0)
        elif (event.keysym == "Up"):
            rotateFallingPiece()
        elif (event.keysym == "="):
            canvas.data.delay = 250
        elif (event.keysym == "-"):
            canvas.data.delay = 2000
    redrawAll()
        
############Rotating Piece
def rotateFallingPiece():
    newPiece = [] # Make a temporary new matrix for rotated falling Piece
    canvas.data.currentRow = len(canvas.data.fallingPiece)
    canvas.data.currentCol = len(canvas.data.fallingPiece[0])
    currentFallingPiece = canvas.data.fallingPiece
    (oldRow,oldCol) = fallingPieceCenter()
    # Switch Rows and Cols into temporary rows and cols of pieces position
    canvas.data.currentRow = len(canvas.data.fallingPiece[0]) 
    canvas.data.currentCol = len(canvas.data.fallingPiece)
    (newRow,newCol) = fallingPieceCenter()
    canvas.data.fallingPieceRow -= (newRow - oldRow)
    canvas.data.fallingPieceCol -= (newCol - oldCol)
    
    for row in range(canvas.data.currentRow):
        newPiece += [[True]*canvas.data.currentCol]
        
    for col in range(len(canvas.data.fallingPiece[0])):
        for row in range(len(canvas.data.fallingPiece)):
            newPiece[col][row] = canvas.data.fallingPiece[row]\
                                 [len(canvas.data.fallingPiece[0])-1-col]
    canvas.data.fallingPiece = newPiece
    # Test whether the rotated Piece is in a legal place
    if (fallingPieceIsLegal(canvas.data.fallingPieceRow,
                           canvas.data.fallingPieceCol) == False):
        canvas.data.fallingPiece = currentFallingPiece
        canvas.data.fallingPieceRow += (newRow - oldRow)
        canvas.data.fallingPieceCol += (newCol - oldCol)

############Falling Piece
def fallingPieceCenter():
    (row, col) = (canvas.data.fallingPieceRow + canvas.data.currentRow,
                  canvas.data.fallingPieceCol + canvas.data.currentCol)
    return (row, col)

def moveFallingPiece(drow, dcol):
    # Move piece to next place and if it is not legal move it back
    canvas.data.fallingPieceRow += drow
    canvas.data.fallingPieceCol += dcol
    if (fallingPieceIsLegal(canvas.data.fallingPieceRow,
                            canvas.data.fallingPieceCol) == False):
        canvas.data.fallingPieceRow -= drow
        canvas.data.fallingPieceCol -= dcol
        return False
    return True

def placeFallingPiece():
    # Put piece on board, by setting the place it cannot go anywhere legally
    # the color of the piece
    rows = len(canvas.data.fallingPiece)
    cols = len(canvas.data.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if(canvas.data.fallingPiece[row][col] == True):
                canvas.data.board[int(row+canvas.data.fallingPieceRow)][int(col+canvas.data.fallingPieceCol)] = canvas.data.fallingPieceColor
    
def fallingPieceIsLegal(pieceRow, pieceCol):
    # Tests whether pieces falls off border 
    # Tests whether pieces falls off border 
    rows = len(canvas.data.fallingPiece)
    cols = len(canvas.data.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if canvas.data.fallingPiece[row][col] == True:
                 if ((pieceRow+row < 0) or (pieceRow+row >= canvas.data.rows) or\
                     (pieceCol+col < 0) or (pieceCol+col >= canvas.data.cols)):
                     return False
                 elif (canvas.data.board[int(pieceRow+row)][int(pieceCol+col)] !=
                       canvas.data.emptyColors):
                     return False       
    return True 

#############New Piece

def newFallingPiece():
    index = random.randint(0,6)
    canvas.data.fallingPiece = canvas.data.tetrisPieces[index]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[index]
    canvas.data.fallingPieceRow = int(0)
    canvas.data.fallingPieceCol = int(canvas.data.cols/2 - len(canvas.data.tetrisPieces[index][0])/2) 
    
################Draw

def redrawAll():
    canvas.delete(ALL)
    if canvas.data.isGameOver == True:
        drawGame()
        canvas.create_text(canvas.data.canvasWidth/2,
                           canvas.data.canvasHeight*2/5, text="Game Over!",
                           fill="black", font="Helvetica 32 bold")
        canvas.create_text(canvas.data.canvasWidth/2,
                           canvas.data.canvasHeight*3/5,
                           text="Press 'r' to reset", fill="black",
                           font="Helvetica 18 bold")
    else:
        drawGame()
        drawFallingPiece()
    # Draw Score
    canvas.create_text(canvas.data.canvasWidth/8, canvas.data.margin/2,
                       text="Score: " + str(canvas.data.score), fill="white",
                    font="Helvetica 12")
    # Draw Directions
    canvas.create_text(canvas.data.canvasWidth/2, canvas.data.canvasHeight - canvas.data.margin/2,
                       text="P to Pause   R to Restart   UP to Rotate", fill = "white",
                       font = "Helvetica 12")
    # If Paused, Draw Pause
    if (canvas.data.paused == True):
        canvas.create_text(canvas.data.canvasWidth - canvas.data.canvasWidth / 8,
                           canvas.data.margin / 2, text="Paused", fill = "white",
                           font="Helvetica 12")


def drawGame():
    # draw the background of board
    canvas.create_rectangle(0,0,
                            canvas.data.canvasWidth,
                            canvas.data.canvasHeight, fill="Black")
    drawBoard()

def drawBoard():
    # Draw the Board of Tetris
    tetrisBoard = canvas.data.board
    rows = len(tetrisBoard)
    cols = len(tetrisBoard[0])
    for row in range(rows):
        for col in range(cols):
            drawCell(row, col, tetrisBoard[row][col])

def drawCell(row, col, cellColor):
    # Draws each cell black and a smaller cell within it the color of the piece
    # if contained or else, draw the unoccupied place blue
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    gridMargin = 1
    canvas.create_rectangle(left-gridMargin, top-gridMargin,
                            right+gridMargin, bottom+gridMargin, fill="white")
    canvas.create_rectangle(left+gridMargin, top+gridMargin,
                            right-gridMargin, bottom-gridMargin, fill=cellColor)


def drawFallingPiece():
    rows = len(canvas.data.fallingPiece)
    cols = len(canvas.data.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if (canvas.data.fallingPiece[row][col] == True):
                drawCell(row+canvas.data.fallingPieceRow,
                         col+canvas.data.fallingPieceCol,
                         canvas.data.fallingPieceColor)

##############Full Rows

def removeFullRows():
    # Checks if a row is full and pops it if it is, score is changed accordingly

    tetrisBoard = canvas.data.board
    rows = canvas.data.rows
    newRow = rows
    cols = canvas.data.cols
    count = 0
    score=0

    for oldRow in range(rows-1,-1,-1):
        count = 0
        for oldCol in range(cols):
            if tetrisBoard[oldRow][oldCol] == canvas.data.emptyColors:
                count += 1
        if count == 0:
            score += 1
        elif count != 0:
            newRow -= 1
            for newCol in range(cols):
                tetrisBoard[newRow][newCol] = tetrisBoard[oldRow][newCol]
    for row in range(newRow-1,-1,-1):
        for col in range(cols):
            tetrisBoard[row][col] = canvas.data.emptyColors
                  
    canvas.data.score += score * score * 100

def make2dList(rows, cols):
    tetrisBoard = []
    for row in range(rows):
        tetrisBoard += [[canvas.data.emptyColors]*cols]
    return tetrisBoard

def timerFired():
    redrawAll()
    if (canvas.data.isGameOver == False) and (canvas.data.paused == False):
        if moveFallingPiece(1,0) == False:
            placeFallingPiece()
            removeFullRows()
            newFallingPiece()
            if fallingPieceIsLegal(canvas.data.fallingPieceRow,
                                   canvas.data.fallingPieceCol) == False:
                    canvas.data.isGameOver = True
        canvas.data.score += 1
    if(canvas.data.score < 8000):
        delay = 600 - 5 * (canvas.data.score // 100)
    elif (canvas.data.score < 18000):
        delay = 280 - 1 * (canvas.data.score // 100)
    else:
        delay = 100
    
    canvas.after(delay, timerFired) # pause, then call timerFired again

def init():
    canvas.data.board = make2dList(canvas.data.rows,canvas.data.cols)
    canvas.data.score = 0
    canvas.data.paused = False
    #Seven "standard" pieces (tetrominoes)
    iPiece = [ [ True,  True,  True,  True] ]
    
    jPiece = [ [ True, False, False ],
               [ True, True,  True] ]
    
    lPiece = [ [ False, False, True],
               [ True,  True,  True] ]
    
    oPiece = [ [ True, True],
               [ True, True] ]
    
    sPiece = [ [ False, True, True],
               [ True,  True, False ] ]
    
    tPiece = [ [ False, True, False ],
               [ True,  True, True] ]
    
    zPiece = [ [ True,  True, False ],
               [ False, True, True] ]
    canvas.data.tetrisPieces = [ iPiece, jPiece, lPiece,
                                 oPiece, sPiece, tPiece, zPiece ]
    canvas.data.tetrisPieceColors = [ "SteelBlue", "CadetBlue", "MediumTurquoise",
                                      "DodgerBlue", "CornflowerBlue", "RoyalBlue", "SkyBlue" ]
    canvas.data.fallingPiece = []
    canvas.data.fallingPieceColor = ""
    canvas.data.isGameOver = False
    newFallingPiece()

def run(rows, cols):
    # create the root and the canvas
    global canvas
    root = Tk()
    root.title("P Y T H O N    T E T R I S")
    margin = 25
    cellSize = 35
    canvasWidth = 2*margin + cols*cellSize
    canvasHeight = 2*margin + rows*cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0,height=0)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.emptyColors = "Gainsboro"
    canvas.data.margin = margin
    canvas.data.cellSize = cellSize
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    canvas.data.rows = rows
    canvas.data.cols = cols
    init()
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run(18,10)
