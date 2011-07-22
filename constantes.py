#!/usr/bin/env python

import sys

###############################################################################
#                        Definicion de constantes                             #
###############################################################################

# Constantes que definen los tipos de movimiento
MOVE_RIGHT=0
MOVE_LEFT=1
MOVE_UP=2
MOVE_DOWN=3

# Constante que define si en el movimiento se esta moviendo una caja
PUSH_BOX=4

# Constantes que definen si una de las posiciones involucradas
# es posicion final
POS0_SPOT=8
POS1_SPOT=16
POS2_SPOT=32

# Valores mascara para extraer los valores deseados
MASK_DIRECTION=3
MASK_BOX=4
MASK_SPOT=56

# Constantes que definen los caracteres utilizados para representar
# los elementos del problema
CHAR_WALL='#'

CHAR_SPACE=' '
CHAR_SPACE_S='.'

CHAR_PLAYER='@'
CHAR_PLAYER_S='+'

CHAR_BOX='$'
CHAR_BOX_S='*'

NEWLINE=chr(10)

###############################################################################
#        Definicion de funciones para determinar el tipo de movimiento        #
###############################################################################

# Obtiene la direccion del mivimiento
def getMoveDirection(move):
    direction = move & MASK_DIRECTION
    return direction

# Determina si se esta moviendo una caja
def isPushingBox(move):
    r = move & 4
    return r == 4

def getGoalSpots(move):
    r = move & 56
    return r

def getMove(row, col):
    if col == 0 and row == -1:
        return MOVE_UP
    elif col == 0 and row == 1:
        return MOVE_DOWN
    elif col == -1 and row == 0:
        return MOVE_LEFT
    elif col == 1 and row == 0:
        return MOVE_RIGHT

def getDir(movement):
    move = getMoveDirection(movement)
    if move == MOVE_UP:
        row = -1
        col = 0
    elif move == MOVE_DOWN:
        row = 1
        col = 0
    elif move == MOVE_LEFT:
        row = 0
        col = -1
    elif move == MOVE_RIGHT:
        row = 0
        col = 1
    else:
        errorMsg = "GetDir: Movimiento invalido."
        raise Exception(errorMsg)

    return row, col

def distance(row1, col1, row2, col2):
    return abs(row1 - row2) + abs(col1 - col2)

def Debug():
    for arg in sys.argv:
        if arg == "-v":
            return True
    return False

def SuperMove():
    for arg in sys.argv:
        if arg == "-s":
            return True
    return False

def Reverse():
    for arg in sys.argv:
        if arg == "-r":
            return True
    return False

def Filename():
    for arg in sys.argv:
        if arg[0] != '-':
            return arg
    raise Exception("No se ha especificado archivo de entrada")
