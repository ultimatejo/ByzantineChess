"""
@author: JAT
Title: Byzantine Chess Model
Version: 1.1
Date: 12/12/2016

Version Tracking:
v1.0 - Initial Release
v1.1 - Corrected the coordinate converison into a move bug for upper and lower case    


USAGE NOTES:
This model is the main controller of the system. 
It maps the move into the board and processes the game 1 move at a time
"""

import tkinter as tk
import math as m
import numpy as np

###############################################################################
# Global references
root = None
moveStart = None
moveEnd = None
pieceLayout = None
board = None
lblToMove = None
posPieces = np.zeros([20,4],dtype=str)
firstMove = np.zeros([20,4],dtype=int)

###############################################################################
# Main model routine
def main():
    global root
    root = tk.Tk()
    CodeVersion = 'BC-v1.1'
    root.title("Byzantine Chess Game - %s" % CodeVersion)
    # Add main containers
    addMoveFrame(root,tk.TOP)
    addCanvas(root,1200,850,tk.TOP)
    # Add menu
    menuBar = tk.Menu(root)
    fileMenu = tk.Menu(menuBar)
    fileMenu.add_command(label="New",command=newGame)
    fileMenu.add_command(label="Open",command=openFile)
    fileMenu.add_command(label="Save",command=saveFile)
    fileMenu.add_separator
    fileMenu.add_command(label="Exit",command=root.destroy)
    menuBar.add_cascade(label="File",menu=fileMenu)
    
    root.config(menu=menuBar)
    root.mainloop()


###############################################################################
# Functions for code execution

# Set the initial layout of the game board
# This is stored in an array 20 by 4. The additional length in the array is to 
# allow the moves to wrap and the board to rotate if required
def posStart(posPieces, firstMove):
    for i in range(0,4):
        posPieces[0,i] = "."
        posPieces[1,i] = "."
        posPieces[2,i] = "."
        posPieces[3,i] = "."
        posPieces[8,i] = "."
        posPieces[9,i] = "."
        posPieces[10,i] = "."
        posPieces[11,i] = "."
        posPieces[16,i] = "."
        posPieces[17,i] = "."
        posPieces[18,i] = "."
        posPieces[19,i] = "."
        posPieces[4,i] = "p"
        firstMove[4,i] = 1
        firstMove[5,i] = 1
        firstMove[6,i] = 1
        posPieces[7,i] = "o"
        firstMove[7,i] = 1
        posPieces[12,i] = "P"
        firstMove[12,i] = 1
        firstMove[13,i] = 1
        firstMove[14,i] = 1
        posPieces[15,i] = "O"
        firstMove[15,i] = 1
    posPieces[5,0] = "q"
    posPieces[5,1] = "b"
    posPieces[5,2] = "n"
    posPieces[5,3] = "r"
    posPieces[6,0] = "k"
    posPieces[6,1] = "b"
    posPieces[6,2] = "n"
    posPieces[6,3] = "r"
    posPieces[13,0] = "K"
    posPieces[13,1] = "B"
    posPieces[13,2] = "N"
    posPieces[13,3] = "R"
    posPieces[14,0] = "Q"
    posPieces[14,1] = "B"
    posPieces[14,2] = "N"
    posPieces[14,3] = "R"
    return posPieces, firstMove    
    
# Locate the centre of a square on the board to place the piece on
def findCentroid(pts):
    # All pts are int he form of [x,y] coordinates
    cenX = pts[0] + pts[2] + pts[4] + pts[6]
    cenX = cenX / 4
    cenY = pts[1] + pts[3] + pts[5] + pts[7]
    cenY = cenY / 4
    pt = [cenX,cenY]
    return pt

# Update the locations of the pieces on the board
def placePieces(posPieces):
    global board       
    global pieceLayout
    counter = 0
    
    # Dictionary of piece images to convert for the board when required
    uni_pieces = {'R':'♜', 'N':'♞', 'B':'♝', 'Q':'♛', 'K':'♚', 'O':'♟', 'P':'♟',
                  'r':'♖', 'n':'♘', 'b':'♗', 'q':'♕', 'k':'♔', 'o':'♙', 'p':'♙', '.':'·'}    
    # Clear previous moves from board
    for j in range(0,16):
        for i in range(0,4):
            piece = posPieces[j+2,i]
            if (piece == "."):
                lblBoard = " "
            else:
                lblBoard = uni_pieces.get(piece)
            board.itemconfig(pieceLayout[counter], text=lblBoard)
            counter = counter + 1            
    
###############################################################################
# Functions for GUI Layout

# Quit the game
def btnQuit():
    global root
    root.destroy()

# Layout the GUI    
def addMoveFrame(parent, sideToPack):
    global lblToMove
    frmMoves = tk.Frame(parent)   
    lblInput = tk.Label(frmMoves, text="")
    lblInput.config(text="Enter move coordinates and direction: ")
    lblInput.pack(side=tk.LEFT)
    lblToMove = tk.Label(frmMoves, text="")
    lblToMove.config(text="White to move")
    lblToMove.pack(side=tk.LEFT)
    addTextBox(frmMoves,tk.LEFT)
    addButton(frmMoves,"Make Move",btnMove,tk.LEFT)
    frmMoves.pack(side=sideToPack)

def addTextBox(parent, sideToPack):
    global moveStart
    global moveEnd
    moveStart = tk.Entry(parent)
    moveStart.pack(side=sideToPack)
    moveEnd = tk.Entry(parent)
    moveEnd.pack(side=sideToPack)
    
def addButton(parent, txtBtn, command, sideToPack):
    v = tk.IntVar()    
    myRdbClck = tk.Radiobutton(parent,text='Clockwise', padx = 20, variable=v,value=1)
    myRdbClck.pack(side=sideToPack)
    myRdbClck = tk.Radiobutton(parent,text='Anti-clockwise', padx = 20, variable=v,value=2)
    myRdbClck.pack(side=sideToPack)  
    myBtn = tk.Button(parent, text=txtBtn,command=command)
    myBtn.pack(side=sideToPack)
    
def addCanvas(parent, width, height, sideToPack):
    global board
    board = tk.Canvas(root, width=width, height=height, bg='white')
    paintCanvas(board)
    newGame()
    board.pack(side=sideToPack)

def paintCanvas(c):
    # 'c' is the passed in canvas parent option    
    global pieceLayout
    pieceLayout = []
    # set canvas properties
    xOrigin = 550
    yOrigin = 425
    xRadius = [100,200,300,400,500]
    yRadius = [75,150,225,300,375]
    thetaStep = 22.5
    thetaStrt = 0
    counter = 0
        
    # Add coordinates
    canvas_id = c.create_text(10, 10, anchor="nw")
    c.itemconfig(canvas_id, text="Inner ring = 1 : Outer ring = 4")
    c.insert(canvas_id, 12,"")
    coordinates = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']
    #im = tk.PhotoImage(file='./Value.png')
    #c.create_image(10, 10, image=im)     
    
    # Shade Squares
    for j in range(0,16):
        canvas_id = c.create_text(m.cos(m.radians(thetaStrt+thetaStep*(j+0.5)))*(xRadius[4]+25) + xOrigin, 
                                  m.sin(m.radians(thetaStrt+thetaStep*(j+0.5)))*(yRadius[4]+25) + yOrigin, anchor="nw")
        c.itemconfig(canvas_id, text=coordinates[j])
        c.insert(canvas_id, 12,"")
        for i in range(0,4):
            points = [m.cos(m.radians(thetaStrt+thetaStep*j))*xRadius[i] + xOrigin, 
                      m.sin(m.radians(thetaStrt+thetaStep*j))*yRadius[i] + yOrigin,
                      m.cos(m.radians(thetaStrt+thetaStep*j))*xRadius[i+1] + xOrigin, 
                      m.sin(m.radians(thetaStrt+thetaStep*j))*yRadius[i+1] + yOrigin,
                      m.cos(m.radians(thetaStrt+thetaStep*(j+1)))*xRadius[i+1] + xOrigin, 
                      m.sin(m.radians(thetaStrt+thetaStep*(j+1)))*yRadius[i+1] + yOrigin,
                      m.cos(m.radians(thetaStrt+thetaStep*(j+1)))*xRadius[i] + xOrigin, 
                      m.sin(m.radians(thetaStrt+thetaStep*(j+1)))*yRadius[i] + yOrigin]
            
            if ((i+j) % 2 == 0):
                c.create_polygon(points, outline='black',fill='blue', width=3)
            else:
                c.create_polygon(points, outline='black',fill='red', width=3)
            # Add pieces if required
            pt = findCentroid(points)
            pieceLayout.append(c.create_text(pt[0]-5, pt[1]-2.5, font=("Purisa", 20)))
            c.itemconfig(pieceLayout[counter], text=" ")       
            counter = counter + 1                

###############################################################################
# Functions for GUI Actions

# Reset the position of the game
def newGame():
    global posPieces
    global firstMove
    posPieces, firstMove = posStart(posPieces, firstMove)
    placePieces(posPieces)

# Open a previously saved game location
def openFile():
    global posPieces
    f = open("SaveFile.bzc","r")
    counter = 0    
    for eachLine in f:
        substrs = eachLine.split(',')
        for j in range(0,4):        
            posPieces[counter,j] = substrs[j]
        counter = counter + 1
    f.close()

# Save the game position
def saveFile():
    global posPieces
    global firstMove
    f = open("SaveFile.bzc","w")
    for i in range (0,20):
        strToSave = ""        
        for j in range (0,4):
            strToSave = strToSave + posPieces[i,j] + ","
            strToSave = strToSave + firstMove[i,j] + ","
        strToSave = strToSave + "\n"        
        f.write(strToSave)
    f.close()
    
# Make a move    
def btnMove():   
    global lblToMove
    global moveStart
    global moveEnd
    global posPieces
    global firstMove
    
    # Pass values into the storage array
    coordStart = moveStart.get()  
    coordEnd = moveEnd.get()
    # Split the coordinates into separatre terms
    cStart = list(coordStart)
    cStart = [str(element).lower() for element in cStart]
    cEnd = list(coordEnd)
    cStart = [str(element).lower() for element in cStart]
        
    # Convert the alpha part into number
    cStart[0] = ord(cStart[0]) - 95
    cEnd[0] = ord(cEnd[0]) - 95
    cStart[1] = int(cStart[1])
    cEnd[1] = int(cEnd[1])    
    print (cStart)
    print (cEnd)    
    
    #moveValue = resolveToNum(cStart,cEnd,posPieces)

    # Check if the move made is legal      
    #isItLegal = legalMove(posPieces[int(cStart[0]),int(cStart[1])-1],
    #                      firstMove[int(cStart[0]),int(cStart[1])-1],posPieces,
    #                      coordStart,coordEnd,moveValue)
    isItLegal=1
    if (isItLegal == 0):
        tk.messagebox.showerror("Illegal Move","That move is not legal. Please try again")
        return
    
    # Move the piece from the start to the end
    posPieces[int(cEnd[0]),int(cEnd[1])-1] = posPieces[int(cStart[0]),int(cStart[1])-1]  
    posPieces[int(cStart[0]),int(cStart[1])-1] = "."
    firstMove[int(cStart[0]),int(cStart[1])-1] = 0
    placePieces(posPieces)
    
    if (lblToMove.cget("text")=="Black to move"):
        lblToMove.config(text="White to move")
    else:
        lblToMove.config(text="Black to move")
        
    
    moveStart.delete(0,tk.END)
    moveEnd.delete(0,tk.END)

###############################################################################
# Legal Move Checking
def legalMove(s_Piece, b_First, v_Board, s_Start, s_End, i_Move):
    # Value of 10 to switch row and 1 to switch column
    # N E = +
    # S W = -
    v_Moves = np.zeros([6])

    # Set the possible moves available to each piece
    v_Moves[0] = [20, 10, 9, 11]                       # Pawn North
    v_Moves[1] = [-20, -10, -9, -11]                   # Pawn South
    v_Moves[2] = [21, 12, -8, -19, -21, -12, 8, 19]    # Knight
    v_Moves[3] = [11, -9, -11, 9]                      # Bishop
    v_Moves[4] = [10, 1, -10, -1]                      # Rook
    v_Moves[5] = [10, 11, 1, -9, -10, -11, -1, 9]      # Queen
    v_Moves[6] = [10, 11, 1, -9, -10, -11, -1, 9]      # King

    # Set the mode
    s_Piece = s_Piece.upper() # Side is not relevant to the legality of the move

    # Convert the coordinates into the move value
    #i_Move = coordToValue(v_Board, s_Piece, s_Start, s_End)

    if (s_Piece == "P"):
        legal = Pawn(b_First,v_Board,i_Move,v_Moves[0],s_End)
    elif (s_Piece == "O"):
        legal = Pawn(b_First,v_Board,i_Move,v_Moves[1],s_End)
    elif (s_Piece == "N"):
        legal = Knight(b_First,v_Board,i_Move,v_Moves[2],s_End)
    elif (s_Piece == "B"):
        legal = Bishop(b_First,v_Board,i_Move,v_Moves[3],s_Start,s_End)
    elif (s_Piece == "R"):
        legal = Rook(b_First,v_Board,i_Move,v_Moves[4],s_End)
    elif (s_Piece == "Q"):
        legal = Queen(b_First,v_Board,i_Move,v_Moves[5],s_End)
    elif (s_Piece == "K"):
        legal = King(b_First,v_Board,i_Move,v_Moves[6],s_End) 
    return legal

def Pawn(b_First,v_Board,i_Move,v_Moves,s_End):
    # Pawns can only do the move once
    # Pawns can only move 2 spaces on their first move
    if (b_First==1):
        i_base = 0
    else:
        i_base = 1
    
    for i in range(i_base,4):
        if (i_Move == v_Moves[i]):
            # Check if this is taking a piece which is only valid diaginally
            if (i == 0 or i == 1):
                cMove = list(s_End)
                cMove[0].upper()
                cMove[0] = ord(cMove[0]) - 63
                cMove[1] = cMove[1] - 1
                if (v_Board[cMove[0],cMove[1]] != "."):
                    legalMove = 0
                    return legalMove
            legalMove = 1
            return legalMove
    legalMove = 0
    return legalMove
    
def Knight(b_First,v_Board,i_Move,v_Moves,s_End):
    # Knights can only do the move once
    for i in range(0,8):
        if (i_Move == v_Moves[i]):
            legalMove = 1
            return legalMove
    legalMove = 0
    return legalMove
    
def Bishop(b_First,v_Board,i_Move,v_Moves,s_Start,s_End):
    # Bishop can move any number of steps. Therefore the system can be any of the values
    # or any multiple of those values
    for i in range(0,4):
        if (i_Move / v_Moves[i] == int(abs(i_Move) / abs(v_Moves[i]))):
            # Is there a piece in the way
            for j in range(1,int(i_Move / v_Moves[i])+1):
                i_Value = coordMoveCheck(i_Move * (j / int(i_Move / v_Moves[i])))
                cStart = list(s_Start)
                cStart[0].upper()
                cStart[0] = ord(cStart[0]) - 63
                i_Xtmp = cStart[0] - i_Value[0]
                i_Ytmp = cStart[1] + i_Value[1]
                if (v_Board[i_Xtmp,i_Ytmp] != "."):
                    legalMove = 0
                    return legalMove
            legalMove = 1
            return legalMove
    legalMove = 0
    return legalMove
    
def Rook(b_First,v_Board,i_Move,v_Moves,s_Start,s_End):
    # Rook can move any number of steps. Therefore the system can be any of the values
    # or any multiple of those values
    for i in range(0,4):
        if (i_Move / v_Moves[i] == int(abs(i_Move) / abs(v_Moves[i]))):
            # Is there a piece in the way
            for j in range(1,int(i_Move / v_Moves[i])+1):
                i_Value = coordMoveCheck(i_Move * (j / int(i_Move / v_Moves[i])))
                cStart = list(s_Start)
                cStart[0].upper()
                cStart[0] = ord(cStart[0]) - 63
                i_Xtmp = cStart[0] - i_Value[0]
                i_Ytmp = cStart[1] + i_Value[1]
                if (v_Board[i_Xtmp,i_Ytmp] != "."):
                    legalMove = 0
                    return legalMove
            legalMove = 1
            return legalMove
    legalMove = 0
    return legalMove
    
def Queen(b_First,v_Board,i_Move,v_Moves,s_Start,s_End):
    # Queen can move any number of steps. Therefore the system can be any of the values
    # or any multiple of those values
    for i in range(0,8):
        if (i_Move / v_Moves[i] == int(abs(i_Move) / abs(v_Moves[i]))):
            # Is there a piece in the way
            for j in range(1,int(i_Move / v_Moves[i])+1):
                i_Value = coordMoveCheck(i_Move * (j / int(i_Move / v_Moves[i])))
                cStart = list(s_Start)
                cStart[0].upper()
                cStart[0] = ord(cStart[0]) - 63
                i_Xtmp = cStart[0] - i_Value[0]
                i_Ytmp = cStart[1] + i_Value[1]
                if (v_Board[i_Xtmp,i_Ytmp] != "."):
                    legalMove = 0
                    return legalMove
            legalMove = 1
            return legalMove
    legalMove = 0
    return legalMove
    
def King(b_First,v_Board,i_Move,v_Moves,s_End):
    # Kings can only do the move once except when castling
    for i in range(0,8):
        if (i_Move == v_Moves[i]):
            legalMove = 1
            return legalMove
            
    # Castling
    # Has the king moved before
    #if (b_First == 1):
        # Identify the move
                
        
    legalMove = 0
    return legalMove

def coordMoveCheck(i_Value):
    # This function determines the offset in X and Y for a given move value
    # The incoming value will be a multiple of 1, 9, 10 or 11
    # The function will then supply the x and y offset
    i_XY = np.zeros([2])
    
    if (i_Value / 11 == int(i_Value / 11)):
        i_XY[0] = i_Value / 11
        i_XY[1] = i_Value / 11
    elif (i_Value / 10 == int(i_Value / 10)):
        i_XY[0] = i_Value / 10
        i_XY[1] = 0
    elif (i_Value / 9 == int(i_Value / 9)):
        i_XY[0] = i_Value / 9
        i_XY[1] = -i_Value / 9
    else:
        i_XY[0] = 0
        i_XY[1] = i_Value
    return i_XY

def resolveToNum(cStart,cEnd, posPieces):
    # This function converts the coordinates into a move value
    # Note that moving around the board (letters) are 10s
    # Moving between rings (numbers) are 1s
    # The value slightly depends on whether the move is made anti or clockwise
    i_Letters = 10*(cEnd[0] - cStart[0])
    i_Numbers = int(cEnd[1]) - int(cStart[1])
    i_Move = i_Letters + i_Numbers
    # If the move 50 or more then the move could be made in either direction
    # This will depend if there is a piece in the way of the move
    # If the move cannot be made due to a piece in the way try the other
    # direction. If this also can't be made return a value of 0 to force
    # an illegal move.
    #if (i_Move >= 50):
        #;fsdkajdf;ads
    return i_Move

###############################################################################
# Launch the code
main()
