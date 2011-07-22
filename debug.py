# debug.py

from constantes import *

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

def printRelCoord(x, y):
    if (x == 0 and y == 0) or (x != 0 and y != 0) or (x > 1 or x < -1) or (y > 1 or y < -1):
        return "[INVALID MOVE]"
    
    if x == 0:
        if y > 0:
            return "[DOWN]"
        else:
            return "[UP]"
    elif x > 0:
        return "[RIGHT]"
    else:
        return "[LEFT]"

def printCoords(x, y):
    return "[" + str(x) + "," + str(y) + "]"
