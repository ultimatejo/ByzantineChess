"""
@author: JAT
Title: Byzantine Chess Model - Legal Moves

Version Tracking:
v1 - Initial Release
"""

import numpy as np
from collections import defaultdict as dd

def moves():
    # Value of 10 to change theta position row and 1 to radial position
    # Clockwise and outwards is +ve         
    # Set the possible moves available to each piece
    pawnAck = [-20, -10, -9, -11]                  # Pawn Anti clockwise -ve
    pawnCck = [20, 10, 9, 11]                      # Pawn Clockwise +ve
    knight = [21, 12, -8, -19, -21, -12, 8, 19]    # Knight
    bishop = [11, -9, -11, 9]                      # Bishop
    rook = [10, 1, -10, -1]                        # Rook
    queen = [10, 11, 1, -9, -10, -11, -1, 9]       # Queen
    king = [10, 11, 1, -9, -10, -11, -1, 9]        # King

    # Create a dictionary of legal moves
    moveList = dd(list)    
    moveList = {'R':rook, 'N':knight, 'B':bishop, 'Q':queen, 'K':king, 'O':pawnCck, 'P':pawnAck}
    return moveList

def legalMove(s_Piece, b_First, v_Board, s_Start, s_End, i_Move):
    # Import the dictionary of legal moves
    moveList = moves()  
    # Set the mode
    s_Piece = s_Piece.upper() # Side is not relevant to the legality of the move
    
    # Provide the second direction value for the move. This can only apply to moves that 
    # either cross the A-P boundary or that can be made in both directions (e.g. a move on 
    # the same ring)
    if (i_Move>0):
        i_Move2 = i_Move - 160
    else:
        i_Move2 = i_Move + 160
    # Convert the coordinates into the move value
    #i_Move = coordToValue(v_Board, s_Piece, s_Start, s_End)

    if (s_Piece == "P"):
        legal = Pawn(b_First,v_Board,i_Move,moveList.get(s_Piece),s_End)
        if (legal==0):
            legal = Pawn(b_First,v_Board,i_Move2,moveList.get(s_Piece),s_End)
    elif (s_Piece == "O"):
        legal = Pawn(b_First,v_Board,i_Move,moveList.get(s_Piece),s_End)
        if (legal==0):
            legal = Pawn(b_First,v_Board,i_Move2,moveList.get(s_Piece),s_End)
    elif (s_Piece == "N"):
        legal = Knight(b_First,v_Board,i_Move,moveList.get(s_Piece))
        if (legal==0):
            legal = Pawn(b_First,v_Board,i_Move2,moveList.get(s_Piece),s_End)
    elif (s_Piece == "B"):
        legal = Bishop(b_First,v_Board,i_Move,moveList.get(s_Piece),s_Start)
        if (legal==0):
            legal = Pawn(b_First,v_Board,i_Move2,moveList.get(s_Piece),s_End)
    elif (s_Piece == "R"):
        legal = Rook(b_First,v_Board,i_Move,moveList.get(s_Piece),s_Start)
        if (legal==0):
            legal = Pawn(b_First,v_Board,i_Move2,moveList.get(s_Piece),s_End)
    elif (s_Piece == "Q"):
        legal = Queen(b_First,v_Board,i_Move,moveList.get(s_Piece),s_Start)
        if (legal==0):
            legal = Pawn(b_First,v_Board,i_Move2,moveList.get(s_Piece),s_End)
    elif (s_Piece == "K"):
        legal = King(b_First,v_Board,i_Move,moveList.get(s_Piece),s_End)
        if (legal==0):
            legal = Pawn(b_First,v_Board,i_Move2,moveList.get(s_Piece),s_End)
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
                cMove = [str(element).lower() for element in cMove]
                cMove[0] = ord(cMove[0]) - 95
                cMove[1] = int(cMove[1]) - 1
                if (v_Board[cMove[0],cMove[1]] != "."):
                    legalMove = 0
                    return legalMove
            legalMove = 1
            return legalMove
    legalMove = 0
    return legalMove
    
def Knight(b_First,v_Board,i_Move,v_Moves):
    # Knights can only do the move once
    for i in range(0,8):
        if (i_Move == v_Moves[i]):
            legalMove = 1
            return legalMove
    legalMove = 0
    return legalMove
    
def Bishop(b_First,v_Board,i_Move,v_Moves,s_Start):
    # Bishop can move any number of steps. Therefore the system can be any of the values
    # or any multiple of those values
    for i in range(0,4):
        if (i_Move / v_Moves[i] == int(abs(i_Move) / abs(v_Moves[i]))):
            # Is there a piece in the way
            for j in range(1,int(i_Move / v_Moves[i])+1):
                i_Value = coordMoveCheck(i_Move * (j / int(i_Move / v_Moves[i])))
                cStart = list(s_Start)
                cStart = [str(element).lower() for element in cStart]                
                cStart[0] = ord(cStart[0]) - 95
                cStart[1] = int(cStart[1])-1
                i_Xtmp = cStart[0] + i_Value[0]
                i_Ytmp = cStart[1] + i_Value[1]
                if (v_Board[i_Xtmp,i_Ytmp] != "."):
                    legalMove = 0
                    return legalMove
            legalMove = 1
            return legalMove
    legalMove = 0
    return legalMove
    
def Rook(b_First,v_Board,i_Move,v_Moves,s_Start):
    # Rook can move any number of steps. Therefore the system can be any of the values
    # or any multiple of those values
    for i in range(0,4):
        if (i_Move / v_Moves[i] == int(abs(i_Move) / abs(v_Moves[i]))):
            # Is there a piece in the way
            for j in range(1,int(i_Move / v_Moves[i])+1):
                i_Value = coordMoveCheck(i_Move * (j / int(i_Move / v_Moves[i])))
                cStart = list(s_Start)
                cStart = [str(element).lower() for element in cStart]                
                cStart[0] = ord(cStart[0]) - 95
                cStart[1] = int(cStart[1])-1
                i_Xtmp = cStart[0] + i_Value[0]
                i_Ytmp = cStart[1] + i_Value[1]
                if (v_Board[i_Xtmp,i_Ytmp] != "."):
                    legalMove = 0
                    return legalMove
            legalMove = 1
            return legalMove
    legalMove = 0
    return legalMove
    
def Queen(b_First,v_Board,i_Move,v_Moves,s_Start):
    # Queen can move any number of steps. Therefore the system can be any of the values
    # or any multiple of those values
    for i in range(0,8):
        print ('Start here ' + str(i))
        print (i_Move / v_Moves[i])
        print (int(abs(i_Move) / abs(v_Moves[i])))
        if (i_Move / v_Moves[i] == int(abs(i_Move) / abs(v_Moves[i]))):
            # Is there a piece in the way
            for j in range(1,int(i_Move / v_Moves[i])+2):
                i_Value = coordMoveCheck(i_Move * (j / int(i_Move / v_Moves[i])))
                print (i_Value)           
                cStart = list(s_Start)
                cStart = [str(element).lower() for element in cStart]                
                cStart[0] = ord(cStart[0]) - 95
                cStart[1] = int(cStart[1])-1
                print (cStart)
                i_Xtmp = cStart[0] + i_Value[0]
                i_Ytmp = cStart[1] + i_Value[1]
                print (i_Value)                
                print (i_Xtmp)
                print (i_Ytmp)
                if (v_Board[i_Xtmp,i_Ytmp] != "."):
                    print ('error - ' + str(j))                    
                    legalMove = 0
                    return legalMove
            legalMove = 1
            return legalMove
    legalMove = 0
    return legalMove
    
def King(b_First,v_Board,i_Move,v_Moves):
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