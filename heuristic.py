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
        #row, col = findPlayer(node.state.table)
        listBoxes = findBoxes(listBoxes, state)
        listPlaces = findPlaces(listPlaces, state)
        
        c = len(listBoxes) * 10
        
        for i in listBoxes:
            rowB, colB = i
            c += distance(state.playerRow, state.playerCol, rowB, colB)
            
            od = 9999
            for j in listPlaces:
                rowP, colP = j
                d = distance(rowP, colP, rowB, colB)
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
    row = 0
    for i in state.matrix:
        col = 0
        for j in i:
            if j == CHAR_BOX:
                listBoxes.append((row, col))
            col += 1
        row += 1
    return listBoxes

def findPlaces(listPlaces, state):
    row = 0
    for i in state.matrix:
        col = 0
        for j in i:
            if j == CHAR_SPACE_S:
                listPlaces.append((row, col))
            col += 1
        row += 1
    return listPlaces
    
def findBoxesPlaced(listBoxes, state):
    row = 0
    for i in state.matrix:
        col = 0
        for j in i:
            if j == CHAR_BOX_S:
                listBoxes.append((row, col))
            col += 1
        row +=1 
    return listBoxes

def findBlockedBoxes(listBoxes, state):
    table = state.matrix
    for i in listBoxes:
        row, col=i
        if table[row+1][col]==CHAR_WALL and table[row][col+1]==CHAR_WALL:
            return True
        if table[row+1][col]==CHAR_WALL and table[row][col-1]==CHAR_WALL:
            return True
        if table[row-1][col]==CHAR_WALL and table[row][col-1]==CHAR_WALL:
            return True
        if table[row-1][col]==CHAR_WALL and table[row][col+1]==CHAR_WALL:
            return True
    return False

