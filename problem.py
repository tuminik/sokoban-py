#!/usr/bin/env python

import sys
import copy

from ai import Problem

from constantes import *
from debug import *
from heuristic import SokobanHeuristic
from state import countSteps

###############################################################################
#                                 Sokoban Problem                             #
###############################################################################

class SokobanProblem(Problem):      #hereda la clase Problem de ai.py
    
    expanded = 0
    toexpand = 0
    
    #recibe la tabla de juego y construye
    def _init_(self):
        self.initial=self
        self.expanded = 1
        self.toexpand = 0
    
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
        row, col = state.playerRow, state.playerCol             #encontrar donde esta el jugador
        #listMoves = generateMoves(state, listMoves)     #puede moverse????  
        listMoves = generatePushes(state, True)
        self.toexpand -= 1
        self.expanded += 1

        if sys.argv[1]=="-v":
            state.printTableDebug()
            print "Nodos a expandir: ", self.toexpand

        if not listMoves:                               #si la lista esta vacia, no hay movimientos posibles por ende no posibles sucesores
            return []                                   #retorna lista vacia la funcion sucesor
        else:                                           #si la lista tiene algo!!
            
            # Por cada movimiento posible
            for movement in listMoves:
                newState = state.clone()                #generar nuevo estado
                try:
                    #newState.movePlayer(movement)           #mueve el jugador    
                    newState.superMovePlayer(movement)
                    listStates.append(newState)             #agregar estado a la lista
                    self.toexpand += 1
                except Exception as ex:
                    print ex
                    newState = False
            
            if sys.argv[1]=="-v":
                print "Nodos a expandir: ", self.toexpand
                raw_input()
            
            lista = []
            for i in range(len(listMoves)):
                #arma una lista de pares por ejemplo [(A,B),(C,D)]
                lista.append((listMoves[i-1], listStates[i-1]))
            return lista
            
            #en este caso un par de movimiento col la tabla que se movio
    
    def h(self, node):
        return SokobanHeuristic(node.state)

    def path_cost(self, c, state1, action, state2):
        return countSteps(state1, state2.playerRow, state2.playerCol) + 1
        
###############################################################################
# Generacion de movimientos para un solo paso
###############################################################################
def generateMoves(state, listMoves):
    listMoves = generateMove(state, listMoves, 1, 0)
    listMoves = generateMove(state, listMoves, 0, 1)
    listMoves = generateMove(state, listMoves, -1, 0)
    listMoves = generateMove(state, listMoves, 0, -1)
    return listMoves

def generateMove(state, listMoves, row, col):
    try:
        pos0 = state.getItemR(0, 0)           # Determino lo que hay a 0 pasos
        pos1 = state.getItemR(row, col)           # Determino lo que hay a 1 paso
        pos2 = state.getItemR(2 * row, 2 * col)   # Determino lo que hay a 2 pasos
    
        if row == 1 and col == 0:
            movement = MOVE_RIGHT
        elif row == -1 and col == 0:
            movement = MOVE_LEFT
        elif row == 0 and col == 1:
            movement = MOVE_DOWN
        elif row == 0 and col == -1:
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
    row = 0
    for i in table:
        col = 0
        for j in i:
            if j == '$':
                table[row][col] = ' '
            col += 1
        row += 1
    row = 0
    for i in table:
        col = 0
        for j in i:
            if j == '.':
                table[row][col] = '$'
            col += 1
        row += 1
    return goal

###############################################################################
# Busqueda de cajas que pueden ser alcanzadas para empujar
# desde la posicion actual
###############################################################################
def findReachableBoxes(state, push):
    startRow, startCol = state.playerRow, state.playerCol
    table = copy.deepcopy(state.matrix)
    
    if sys.argv[1] == "-v":
        printTable(table, "")
    
    here = table[startRow][startCol]
    if here == CHAR_PLAYER:
        table[startRow][startCol] = CHAR_SPACE
    elif here == CHAR_PLAYER_S:
        table[startRow][startCol] = CHAR_SPACE_S
    
    boxes = []
    boxes = testReachableBoxes(boxes, table, startRow, startCol, push)
    
    if sys.argv[1] == "-v":
        printTable(table, "")
    
    return boxes

def testReachableBoxes(boxes, table, row, col, push):
    here = table[row][col]
    
    #marco este lugar como visitado
    if here == CHAR_SPACE:
        table[row][col] = CHAR_PLAYER
    elif here == CHAR_SPACE_S:
        table[row][col] = CHAR_PLAYER_S
    
    #prueba si hay cajas a mover en cada direccion
    boxes = testReachableBoxesDir(boxes, table, row, col, 0, -1, push) #UP
    boxes = testReachableBoxesDir(boxes, table, row, col, 0, 1, push)  #DOWN
    boxes = testReachableBoxesDir(boxes, table, row, col, -1, 0, push) #LEFT
    boxes = testReachableBoxesDir(boxes, table, row, col, 1, 0, push)  #RIGHT
    
    return boxes

def testReachableBoxesDir(boxes, table, row, col, relRow, relCol, push):
    pos1 = table[row + relRow][col + relCol]
    move = 0
    
    if pos1 == CHAR_BOX or pos1 == CHAR_BOX_S:
        if push: #empujar
            pos2 = table[row + 2 * relRow][col + 2 * relCol]
        else: #estirar
            pos2 = table[row - relRow][col - relCol]
        
        if pos2 == CHAR_SPACE or pos2 == CHAR_SPACE_S \
        or pos2 == CHAR_PLAYER or pos2 == CHAR_PLAYER_S:
            move = PUSH_BOX
            if push: #empujar
                move = move | getMove(relRow, relCol)
                boxes.append((row, col, move))
            else: #estirar
                move = move | getMove(-relRow, -relCol)
                boxes.append((row - relRow, col - relCol, move))
    elif pos1 == CHAR_SPACE or pos1 == CHAR_SPACE_S:
        #hace la recursion de la busqueda
        boxes = testReachableBoxes(boxes, table, row + relRow, col + relCol, push)
    
    return boxes
