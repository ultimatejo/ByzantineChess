"""
@author: JAT
Title: Byzantine Chess Model

Version Tracking:
v1.0 - Initial Release
v1.1 - Corrected the coordinate converison into a move bug for upper and lower case    
v1.2 - Add help menu and the legal move review
v1.3 - Split into classes and files to facilitate the AI development
"""

import tkinter as tk
import math as m
import numpy as np
import legalMoves_1 as lg
import AI_1 as ai

###############################################################################
# Global references
CodeVersion = 'BC-v1.3'
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
    global CodeVersion    
    root = tk.Tk()
    root.iconbitmap('BZ-Icon.ico')
    root.title("Byzantine Chess Game - %s" % CodeVersion)
    # Add main containers
    addMoveFrame(root,tk.TOP)
    addCanvas(root,1200,850,tk.TOP)
    # Add menu
    menuBar = tk.Menu(root)
    fileMenu = tk.Menu(menuBar, tearoff = 0)
    fileMenu.add_command(label="New",command=newGame)
    fileMenu.add_command(label="Open",command=openFile)
    fileMenu.add_command(label="Save",command=saveFile)
    fileMenu.add_separator
    fileMenu.add_command(label="Exit",command=root.destroy)
    menuBar.add_cascade(label="File",menu=fileMenu)

    helpMenu = tk.Menu(menuBar, tearoff = 0)
    helpMenu.add_command(label="About",command=about)
    helpMenu.add_command(label="How to play",command=instructions)
    menuBar.add_cascade(label="Help",menu=helpMenu)
    
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
# Functions for GUI Actions.

# Reset the position of the game
def newGame():
    global posPieces
    global firstMove
    posPieces, firstMove = posStart(posPieces, firstMove)
    placePieces(posPieces)

# Open a previously saved game location
def openFile():
    global posPieces
    global firstMove
    f = open("SaveFile.bzc","r")
    counter = 0    
    for eachLine in f:
        substrs = eachLine.split(',')
        for j in range(0,4):        
            posPieces[counter,j] = substrs[2*j]
            firstMove[counter,j] = int(substrs[2*j + 1])
        counter = counter + 1
    placePieces(posPieces)    
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
            strToSave = strToSave + str(firstMove[i,j]) + ","
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
    cEnd = [str(element).lower() for element in cEnd]
        
    # Convert the alpha part into number
    cStart[0] = ord(cStart[0]) - 95
    cEnd[0] = ord(cEnd[0]) - 95
    cStart[1] = int(cStart[1])
    cEnd[1] = int(cEnd[1])    
    
    moveValue = lg.resolveToNum(cStart,cEnd,posPieces)   
    
    # Check if the move made is legal      
    isItLegal = lg.legalMove(posPieces[int(cStart[0]),int(cStart[1])-1],
                          firstMove[int(cStart[0]),int(cStart[1])-1],posPieces,
                          coordStart,coordEnd,moveValue)
    
    if (isItLegal == 0):
        illegalMove()
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

def about():    # Display the about box
    global root
    global CodeVersion
    t = tk.Toplevel(root)
    t.iconbitmap('BZ-Icon.ico')
    t.wm_title("About Byzantine Chess  - %s" % CodeVersion)
    l1 = tk.Label(t, text="This implentation of Byzantine Chess was written by ultimatejo")
    l1.pack(side="top", fill="both", expand=True)
    l2 = tk.Label(t, text="Source code available at https://github.com/ultimatejo/ByzantineChess")
    l2.pack(side="top", fill="both", expand=True)
    #path = os.path.basename(lg.__file__)
    #print (path)
    btn = tk.Button(t, text="Dismiss", command=t.destroy)
    btn.pack()
    
def illegalMove():  # Supply a warning message if the move is not legal
    global root
    global CodeVersion
    t = tk.Toplevel(root)
    t.iconbitmap('BZ-Icon.ico')
    t.wm_title("Illegal Move")
    l1 = tk.Label(t, text="This is not a legal move. Check your input coordinates")
    l1.pack(side="top", fill="both", expand=True)
    btn = tk.Button(t, text="OK", command=t.destroy)
    btn.pack()
    
def instructions(): # Display some instructions on how to use and play the game
    global root
    t = tk.Toplevel(root)
    t.iconbitmap('BZ-Icon.ico')
    t.wm_title("How to play Byzantine Chess")
    l = tk.Label(t, text="This is how to play")
    l.pack(side=tk.TOP, fill="both", expand=True)
    btn = tk.Button(t, text="Dismiss", command=t.destroy)
    btn.pack(side=tk.BOTTOM)
    S = tk.Scrollbar(t)
    T = tk.Text(t, height=15, width=80)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote = """Note:
        The pieces in Byzantine chess all move in the same way as they do in 
        regular chess. The key differences are that the pawns cannot be promoted
        and can only move in the starting direction."""
    T.insert(tk.END, quote)
    
###############################################################################
# Launch the code
main()
