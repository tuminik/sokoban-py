#!/usr/bin/env python

import sys
import copy

from ai import Problem

from constantes import *
from heuristic import SokobanHeuristic

###############################################################################
#                                 Sokoban Problem                             #
###############################################################################

class SokobanProblem(Problem):      #hereda la clase Problem de ai.py
    
    expanded = 0
    
    #recibe la tabla de juego y construye
    def _init_(self):
        self.initial=self
        self.expanded = 0
    
    def goal_test(self, state):
        boxes=0
        boxes_s=0
        spaces_s=0
        
        for column in state.matrix:
            for position in column:
                if position == CHAR_BOX:
                    boxes += 1
                #elif position == CHAR_BOX_S:
                #    boxes_s += 1
                elif position == CHAR_SPACE_S:
                    spaces_s += 1
        
        if boxes == 0 and spaces_s == 0:
            return True
        else:
            return False
    
    def successor(self, state):                         #funcion sucesora
        listMoves=[]                                    #lista para posibles movimientos
        listStates=[]                                   #lista para posibles estados de la tabla
        x, y = state.playerX, state.playerY             #encontrar donde esta el jugador
        listMoves = generateMoves(state, listMoves)     #puede moverse????  
        #listMoves = generatePushes(state, True)
        self.expanded += 1
        if not listMoves:                               #si la lista esta vacia, no hay movimientos posibles por ende no posibles sucesores
            return []                                   #retorna lista vacia la funcion sucesor
        else:                                           #si la lista tiene algo!!
            
            # Por cada movimiento posible
            for movement in listMoves:
                newState = state.clone()                #generar nuevo estado
                newState.movePlayer(movement)           #mueve el jugador    
                #newState.superMovePlayer(movement)
                listStates.append(newState)             #agregar estado a la lista
            
            if sys.argv[1]=="-v":
                #printTable(state.matrix, "padre")
                state.printTableDebug()
                raw_input()
            
            lista = []
            for i in range(len(listMoves)):
                #arma una lista de pares por ejemplo [(A,B),(C,D)]
                lista.append((listMoves[i-1], listStates[i-1]))
            return lista
            
            #en este caso un par de movimiento y la tabla que se movio
    
    def h(self, node):
        return SokobanHeuristic(node.state)

###############################################################################
# Generacion de movimientos para un solo paso
###############################################################################
def generateMoves(state, listMoves):
    listMoves = generateMove(state, listMoves, 1, 0)
    listMoves = generateMove(state, listMoves, 0, 1)
    listMoves = generateMove(state, listMoves, -1, 0)
    listMoves = generateMove(state, listMoves, 0, -1)
    return listMoves

def generateMove(state, listMoves, x, y):
    try:
        pos0 = state.getItemR(0, 0)           # Determino lo que hay a 0 pasos
        pos1 = state.getItemR(x, y)           # Determino lo que hay a 1 paso
        pos2 = state.getItemR(2 * x, 2 * y)   # Determino lo que hay a 2 pasos
    
        if x == 1 and y == 0:
            movement = MOVE_RIGHT
        elif x == -1 and y == 0:
            movement = MOVE_LEFT
        elif x == 0 and y == 1:
            movement = MOVE_DOWN
        elif x == 0 and y == -1:
            movement = MOVE_UP
        else:
            return listMoves
        
        # Verifica si el jugador esta sobre una posicion de meta
        if pos0 == CHAR_PLAYER_S:
            movement = movement | POS0_SPOT
        
        # Verifica si el siguiente espacio es un lugar de meta
        if pos1 == CHAR_BOX_S or pos1 == CHAR_SPACE_S:
            movement = movement | POS1_SPOT
        
        # Si el siguiente espacio contiene una caja
        if pos1 == CHAR_BOX or pos1 == CHAR_BOX_S:
            movement = movement | PUSH_BOX
            
            if pos2 == CHAR_SPACE_S:
                movement = movement | POS1_SPOT
            elif pos2 == CHAR_SPACE:
                movement = movement
            else:
                return listMoves
        
        if state.canMove(movement):
            listMoves.append(movement)
        
        return listMoves
    except:
        return listMoves

###############################################################################
# Generacion de movimientos, donde solo importa empujar las cajas
###############################################################################
def generatePushes(state, push):
    listPushes = findReachableBoxes(state, push)
    print "Cajas encontradas:" + str(len(listPushes))
    return listPushes
        
###############################################################################
# Genera un estado donde todas las cajas estan en su posicion
###############################################################################
def generateGoalState(state):
    goal = state.clone()
    table = goal.matrix
    x = 0
    for i in table:
        y = 0
        for j in i:
            if j == '$':
                table[x][y] = ' '
            y += 1
        x += 1
    x = 0
    for i in table:
        y = 0
        for j in i:
            if j == '.':
                table[x][y] = '$'
            y += 1
        x += 1
    return goal

###############################################################################
# Busqueda de cajas que pueden ser alcanzadas para empujar
# desde la posicion actual
###############################################################################
def findReachableBoxes(state, push):
    startX, startY = state.playerX, state.playerY
    table = copy.deepcopy(state.matrix)
    
    if table[startX][startY] == CHAR_PLAYER:
        table[startX][startY] = CHAR_SPACE
    elif table[startX][startY] == CHAR_PLAYER_S:
        table[startX][startY] = CHAR_SPACE_S
    
    boxes = []
    boxes = testReachableBoxes(boxes, table, startX, startY, push)
    
    return boxes

def testReachableBoxes(boxes, table, x, y, push):
    here = table[x][y]
    
    #marco este lugar como visitado
    if here == CHAR_SPACE:
        table[x][y] = CHAR_PLAYER
    elif here == CHAR_SPACE_S:
        table[x][y] = CHAR_PLAYER_S
    
    #prueba si hay cajas a mover en cada direccion
    boxes = testReachableBoxesDir(boxes, table, x, y, 0, -1, push) #UP
    boxes = testReachableBoxesDir(boxes, table, x, y, 0, 1, push)  #DOWN
    boxes = testReachableBoxesDir(boxes, table, x, y, -1, 0, push) #LEFT
    boxes = testReachableBoxesDir(boxes, table, x, y, 1, 0, push)  #RIGHT
    
    return boxes

def testReachableBoxesDir(boxes, table, x, y, relX, relY, push):
    pos1 = table[x + relX][y + relY]
    move = 0
    
    if pos1 == CHAR_BOX or pos1 == CHAR_BOX_S:
        if push: #empujar
            pos2 = table[x + 2 * relX][y + 2 * relY]
        else: #estirar
            pos2 = table[x - relX][y - relY]
        
        if pos2 == CHAR_SPACE or pos2 == CHAR_SPACE_S \
        or pos2 == CHAR_PLAYER or pos2 == CHAR_PLAYER_S:
            move = PUSH_BOX
            if push: #empujar
                move = move | getMoveFromRel(relX, relY)
                boxes.append((x, y, move))
            else: #estirar
                move = move | getMoveFromRel(-relX, -relY)
                boxes.append((x - relX, y - relY, move))
    elif pos1 == CHAR_SPACE or pos1 == CHAR_SPACE_S:
        #hace la recursion de la busqueda
        boxes = testReachableBoxes(boxes, table, x + relX, y + relY, push)
    
    return boxes
