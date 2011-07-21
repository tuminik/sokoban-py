# heuristic.py

from utils import infinity
from ai import Node

from constantes import *

def SokobanHeuristic(state):
    c = 0
    d = 0
    od = 0
    listBoxes = []
    listPlaces = []
    if state:
        #x, y = findPlayer(node.state.table)
        listBoxes = findBoxes(listBoxes, state)
        listPlaces = findPlaces(listPlaces, state)
        
        c = len(listBoxes) * 10
        
        for i in listBoxes:
            xB, yB = i
            c += distancePlayerToBox(state.playerX, state.playerY, xB, yB)
            
            od = 9999
            for j in listPlaces:
                xP, yP = j
                d = distancePlacesToBoxes(xP, yP, xB, yB)
                if od < d:
                    od = d
            if od != 9999:
                c += od
    if findBlockedBoxes(listBoxes, state):
        return infinity
    return c

##################################
# Funciones que buscan los elementos del laberinto
##################################

def findBoxes(listBoxes, state):
    x=0
    for i in state.matrix:
        y=0
        for j in i:
            if j == CHAR_BOX:
                listBoxes.append((x, y))
            y+=1
        x+=1
    return listBoxes

def findPlaces(listPlaces, state):
    x=0
    for i in state.matrix:
        y=0
        for j in i:
            if j == CHAR_SPACE_S:
                listPlaces.append((x, y))
            y+=1
        x+=1
    return listPlaces
    
def distancePlayerToBox(xPlayer, yPlayer, xBox, yBox):
    return abs(xPlayer - xBox) + abs(yPlayer - yBox) + 1
    
def distancePlacesToBoxes(xPlace, yPlace, xBox, yBox):
    return abs(xPlace - xBox) + abs(yPlace - yBox)+5
    
def findBoxesPlaced(listBoxes, state):
    x=0
    for i in state.matrix:
        y=0
        for j in i:
            if j == CHAR_BOX_S:
                listBoxes.append((x, y))
            y += 1
        x +=1 
    return listBoxes

def findBlockedBoxes(listBoxes, state):
    table = state.matrix
    for i in listBoxes:
        x, y=i
        if table[x+1][y]==CHAR_WALL and table[x][y+1]==CHAR_WALL:
            return True
        if table[x+1][y]==CHAR_WALL and table[x][y-1]==CHAR_WALL:
            return True
        if table[x-1][y]==CHAR_WALL and table[x][y-1]==CHAR_WALL:
            return True
        if table[x-1][y]==CHAR_WALL and table[x][y+1]==CHAR_WALL:
            return True
    return False

