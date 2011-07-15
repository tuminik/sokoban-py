#!/usr/bin/env python

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
    return r

def getGoalSpots(move):
    r = move & 56
    return r

