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

from constantes import CHAR_PLAYER, CHAR_PLAYER_S


# Busca el jugador dentro del laberinto
def findPlayer(state):
    x=0
    for i in state:
        y=0
        for j in i:
            if j == CHAR_PLAYER or j == CHAR_PLAYER_S:
                return x, y
            y+=1
        x+=1
    return False, False

def canMove(x, y, listMoves,  state):
    try :
        if state[x+1][y]==' ':
            listMoves.append(0)
        if state[x-1][y]==' ':
            listMoves.append(1)
        if state[x][y+1]==' ':
            listMoves.append(2)
        if state[x][y-1]==' ':
            listMoves.append(3)
        if state[x+1][y]=='$' and state[x+2][y]==' ' :
            listMoves.append(4)  
        if state[x-1][y]=='$'and state[x-2][y]==' ' :
            listMoves.append(5)
        if state[x][y+1]=='$'and state[x][y+2]==' ' :
            listMoves.append(6)
        if state[x][y-1]=='$'and state[x][y-2]==' ' :
            listMoves.append(7)
        if state[x+1][y]=='$' and state[x+2][y]=='.' :
            listMoves.append(8)  
        if state[x-1][y]=='$'and state[x-2][y]=='.' :
            listMoves.append(9)
        if state[x][y+1]=='$'and state[x][y+2]=='.' :
            listMoves.append(10)
        if state[x][y-1]=='$'and state[x][y-2]=='.' :
            listMoves.append(11)
        return listMoves
    except:
        return listMoves
        
def move(x, y,  listMoves, listStates,  state):
    tableS = Table()
    tableS.table= copy.deepcopy(state)
    tableS.table[x][y]=' '
    try :
        for i in listMoves:
            if i==0:
                tableS.table[x+1][y]= '@'
                listStates.append(copy.deepcopy(tableS))     #copia la tabla y la agrega a la lista de posible movidas
                tableS.table[x+1][y]= ' '                                      #"cerar" la tabla
            if i==1:
                tableS.table[x-1][y]= '@'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x-1][y]= ' '
            if i==2:
                tableS.table[x][y+1]= '@'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x][y+1]= ' '
            if i==3:
                tableS.table[x][y-1]= '@'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x][y-1]= ' '
            if i==4:
                tableS.table[x+1][y]= '@'
                tableS.table[x+2][y]='$'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x+1][y]= ' '
                tableS.table[x+2][y]=' '
            if i==5:
                tableS.table[x-1][y]= '@'
                tableS.table[x-2][y]='$'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x-1][y]= ' '
                tableS.table[x-2][y]= ' '
            if i==6:
                tableS.table[x][y+1]= '@'
                tableS.table[x][y+2]='$'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x][y+1]= ' '
                tableS.table[x][y+2]= ' '
            if i==7:
                tableS.table[x][y-1]= '@'
                tableS.table[x][y-2]='$'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x][y-1]= ' '
                tableS.table[x][y-2]= ' '
            if i==8:
                tableS.table[x+1][y]= '@'
                tableS.table[x+2][y]='*'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x+1][y]= '.'
                tableS.table[x+2][y]= ' '
            if i==9:
                tableS.table[x-1][y]= '@'
                tableS.table[x-2][y]='*'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x-1][y]= '.'
                tableS.table[x-2][y]= ' '
            if i==10:
                tableS.table[x][y+1]= '@'
                tableS.table[x][y+2]='*'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x][y+1]= '.'
                tableS.table[x][y+2]= ' '
            if i==11:
                tableS.table[x][y-1]= '@'
                tableS.table[x][y-2]='*'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x][y-1]= '.'
                tableS.table[x][y-2]= ' '
        return listStates
    except:
        return  listStates
#funcion constructor

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
        listPlaces = findPlaces(listPlaces, self.initial.table)
        listBoxes = findBoxesPlaced(listBoxes, state.table)
        if not listBoxes:
            return False
        for i in listBoxes:
                xB, yB = i
                for j in listPlaces:
                    xP, yP = j
                    if xB!=xP or yB!=yP:
                        return False
        return True
    
    def successor(self, state):                              #funcion sucesora
        listMoves=[]                                         #lista para posibles movimientos
        listStates=[]                                        #lista para posibles estados de la tabla
        x, y = findPlayer(state.table)                       #encontrar donde esta el jugador
        canMove(x, y,listMoves,  state.table)                #puede moverse????  
        if not listMoves:                                    #si la lista esta vacia, no hay movimientos posibles por ende no posibles sucesores
            return []                                        #retorna lista vacia la funcion sucesor
        else:                                                #si la lista tiene algo!!
            move(x, y, listMoves ,  listStates, state.table) #con listMoves hago los posibles movimientos en listStates
            if printTableFather:
                printTable(state.table, "padre")
                raw_input()
            return [(moveA, wichMove(moveA, listStates, listMoves)) for moveA in listMoves] #arma una lista de pares por ejemplo [(A,B),(C,D)]
            #en este caso un par de movimiento y la tabla que se movio
    
    def h(self, node):
        c=0
        listBoxes=[]
        listPlaces=[]
        if node.state:
            x, y = findPlayer(node.state.table)
            listBoxes = findBoxes(listBoxes, node.state.table)
            listPlaces = findPlaces(listPlaces, node.state.table)
            for i in listBoxes:
                xB, yB = i
                c+=distancePlayerToBox(x, y, xB, yB)
                for j in listPlaces:
                    xP, yP = j
                    c+=distancePlacesToBoxes(xP, yP, xB, yB)
        if findBlockedBoxes(listBoxes, node.state.table):
            return infinity
        return c

def wichMove(moveA, listStates, listMoves):
    try:
        return listStates[listMoves.index(moveA)]
    except:
        return []

def findBoxes(listBoxes, state):
    x=0
    for i in state:
        y=0
        for j in i:
            if j=='$':
                listBoxes.append((x, y))
            y+=1
        x+=1
    return listBoxes

def findPlaces(listPlaces, state):
    x=0
    for i in state:
        y=0
        for j in i:
            if j=='.':
                listPlaces.append((x, y))
            y+=1
        x+=1
    return listPlaces
    
def findBoxesPlaced(listBoxes, state):
    x=0
    for i in state:
        y=0
        for j in i:
            if j=='*':
                listBoxes.append((x, y))
            y+=1
        x+=1
    return listBoxes

def findBlockedBoxes(listBoxes, table):
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
        



def findGoalState(table):
    x=0
    for i in table:
        y=0
        for j in i:
            if j=='$':
                table[x][y]=' '
            y+=1
        x+=1
    x=0
    for i in table:
        y=0
        for j in i:
            if j=='.':
                table[x][y]='$'
            y+=1
        x+=1
    return table

def distancePlayerToBox(xPlayer, yPlayer, xBox, yBox):
    return abs(xPlayer-xBox)+abs(yPlayer-yBox)+1
    
    
def distancePlacesToBoxes(xPlace, yPlace, xBox, yBox):
    return abs(xPlace-xBox)+abs(yPlace-yBox)+5
    
class Table():  #nuevo tipo de dato Table que formado por una lista
    table=[]        #no funciona la hastable si es solo con una tabla da un error de "unhashable type: list"
                        #entonces es necesario meter una lista dentro de una clase, se entiende que asi es mas formal y lleva un unico puntero
    
def printTable(tab, label):
    print "-----------", label                            
    for i in tab:
        print "".join(i)
    print "-----------", label
    


if len(sys.argv)==2 or len(sys.argv)==3:
    goal = Table()                                              #llamada al constuctor de Table
    if sys.argv[1]=="-v":
        printTableFather=True
        try:
            goal.table = obtenerMapa(sys.argv[2])
        except:
            print "El nombre del archivo es incorrecto"
            exit(0)

    else:
        try:
            goal.table = obtenerMapa(sys.argv[1])
        except:
            print "El nombre del archivo es incorrecto"
            exit(0)
    initial = copy.deepcopy(goal) #copia real
    goal.table = findGoalState(goal.table) #encontrar el estado final
    sokoban = SokobanProblem(initial, goal) 
    
    x1= time.strftime('%s')
    
    pathS = astar_search(sokoban).path()
    
    x2= time.strftime('%s')
    timediff = int(x2)-int(x1)
    
    
    path = [node.state for node in pathS] 
    for i in path:
        printTable(i.table, "")
        print
        
    print 'Tiempo:', timediff,'segundos'
    
else:
    if len(sys.argv)<2:
        print "Debe recibir el nombre del archivo..."
    if len(sys.argv)>3:
        print "Demasiados arguementos..."

    
#depth_first_graph_search(sokoban)
#depth_limited_search(sokoban)
#iterative_deepening_search(sokoban)
