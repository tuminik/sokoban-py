# debug.py

from constantes import *

def printTable(table, label):
    row = 0
    col = 0
    print "-----------", label
    for row in table:
        print "".join(row)
    print "-----------", label

def printDirection(move):
    direction = getMoveDirection(move)
    if direction == MOVE_UP:
        return "[UP]"
    elif direction == MOVE_DOWN:
        return "[DOWN]"
    elif direction == MOVE_LEFT:
        return "[LEFT]"
    else:
        return "[RIGHT]"

def printRelCoord(row, col):
    if (row == 0 and col == 0) or (row != 0 and col != 0) or (row > 1 or row < -1) or (col > 1 or col < -1):
        return "[INVALID MOVE]"
    
    if row == 0:
        if col > 0:
            return "[RIGHT]"
        else:
            return "[LEFT]"
    elif row > 0:
        return "[DOWN]"
    else:
        return "[UP]"

def printCoords(row, col):
    return "[" + str(row) + "," + str(col) + "]"
