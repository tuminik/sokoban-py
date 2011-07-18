#!/usr/bin/env python

from ai import Problem
from ai import astar_search
from ai import iterative_deepening_search
from ai import depth_first_tree_search
from ai import depth_first_graph_search
from ai import breadth_first_tree_search
from ai import breadth_first_graph_search
from ai import depth_limited_search
from utils import infinity
import sys
from tpIAsokobanparser import obtenerMapa
import copy
printTableFather=False
import time

from constantes import *
from state import sokobanState

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
        
        listMoves.append(movement)
        
        return listMoves
    except:
        return listMoves
        
###############################################################################
#                                 Sokoban Problem                             #
###############################################################################

class SokobanProblem(Problem):      #hereda la clase Problem de ai.py
    
    #recibe la tabla de juego y construye
    def _init_(self):
        self.initial=self
    
    def goal_test(self, state):
        listPlaces=[]
        listBoxes=[]
        listPlaces = findPlaces(listPlaces, self.initial)
        listBoxes = findBoxesPlaced(listBoxes, state)
        if not listBoxes:
            return False
        for i in listBoxes:
                xB, yB = i
                for j in listPlaces:
                    xP, yP = j
                    if xB != xP or yB != yP:
                        return False
        return True
    
    def successor(self, state):                         #funcion sucesora
        listMoves=[]                                    #lista para posibles movimientos
        listStates=[]                                   #lista para posibles estados de la tabla
        x, y = state.playerX, state.playerY             #encontrar donde esta el jugador
        listMoves = generateMoves(state, listMoves)     #puede moverse????  
        if not listMoves:                               #si la lista esta vacia, no hay movimientos posibles por ende no posibles sucesores
            return []                                   #retorna lista vacia la funcion sucesor
        else:                                           #si la lista tiene algo!!
            
            # Por cada movimiento posible
            for movement in listMoves:
                newState = state.clone()                #generar nuevo estado
                newState.movePlayer(movement)           #mueve el jugador    
                listStates.append(newState)             #agregar estado a la lista
            
            if sys.argv[1]=="-v":
                printTable(state.matrix, "padre")
                raw_input()
            return [(moveA, wichMove(moveA, listStates, listMoves)) for moveA in listMoves] #arma una lista de pares por ejemplo [(A,B),(C,D)]
            #en este caso un par de movimiento y la tabla que se movio
    
    def h(self, node):
        c = 0
        listBoxes = []
        listPlaces = []
        if node.state:
            #x, y = findPlayer(node.state.table)
            listBoxes = findBoxes(listBoxes, node.state)
            listPlaces = findPlaces(listPlaces, node.state)
            for i in listBoxes:
                xB, yB = i
                c += distancePlayerToBox(node.state.playerX, node.state.playerY, xB, yB)
                for j in listPlaces:
                    xP, yP = j
                    c += distancePlacesToBoxes(xP, yP, xB, yB)
        if findBlockedBoxes(listBoxes, node.state):
            return infinity
        return c

def wichMove(moveA, listStates, listMoves):
    try:
        return listStates[listMoves.index(moveA)]
    except:
        return []

def findBoxes(listBoxes, state):
    x=0
    for i in state.matrix:
        y=0
        for j in i:
            if j=='$':
                listBoxes.append((x, y))
            y+=1
        x+=1
    return listBoxes

def findPlaces(listPlaces, state):
    x=0
    for i in state.matrix:
        y=0
        for j in i:
            if j=='.':
                listPlaces.append((x, y))
            y+=1
        x+=1
    return listPlaces
    
def findBoxesPlaced(listBoxes, state):
    x=0
    for i in state.matrix:
        y=0
        for j in i:
            if j=='*':
                listBoxes.append((x, y))
            y+=1
        x+=1
    return listBoxes

def findBlockedBoxes(listBoxes, state):
    table = state.matrix
    for i in listBoxes:
        x, y=i
        if table[x+1][y]=='#' and table[x][y+1]=='#':
            return True
        if table[x+1][y]=='#' and table[x][y-1]=='#':
            return True
        if table[x-1][y]=='#' and table[x][y-1]=='#':
            return True
        if table[x-1][y]=='#' and table[x][y+1]=='#':
            return True
    return False

# Genera un estado donde todas las cajas estan en su posicion
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

def distancePlayerToBox(xPlayer, yPlayer, xBox, yBox):
    return abs(xPlayer - xBox) + abs(yPlayer - yBox) + 1
    
def distancePlacesToBoxes(xPlace, yPlace, xBox, yBox):
    return abs(xPlace - xBox) + abs(yPlace - yBox)+5
    
def printTable(tab, label):
    print "-----------", label                            
    for i in tab:
        print "".join(i)
    print "-----------", label

def main():
    if len(sys.argv)==2 or len(sys.argv)==3:

        if sys.argv[1]=="-v":
            printTableFather = True
            initial = obtenerMapa(sys.argv[2])
        else:
            initial = obtenerMapa(sys.argv[1])
            
        goal = generateGoalState(initial) #encontrar el estado final
        sokoban = SokobanProblem(initial, goal) 
        
        x1= time.strftime('%S')
        
        pathS = astar_search(sokoban).path()
        
        x2= time.strftime('%S')
        timediff = int(x2) - int(x1)
        
        #Genera la secuencia de estados
        path = [node.state for node in pathS]
        states = []
        
        for state in path:
            states.append(state)
        
        i = len(states) - 1
        while i >= 0:
            printTable(states[i].matrix, "")
            print
            i -= 1
            
        print 'Tiempo:', timediff,'segundos'
        
    else:
        if len(sys.argv)<2:
            print "Debe recibir el nombre del archivo..."
        if len(sys.argv)>3:
            print "Demasiados arguementos..."

if __name__ == "__main__":
    main()

#depth_first_graph_search(sokoban)
#depth_limited_search(sokoban)
#iterative_deepening_search(sokoban)
