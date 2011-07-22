#!/usr/bin/env python

import copy

from utils import FIFOQueue

from constantes import *
from debug import *
from heuristic import SokobanHeuristic

class SokobanState:
    
    ###########################################################################
    # Declaracion de variables
    ###########################################################################
    
    # Variables que definen las dimensiones del laberinto
    matrixX = 0
    matrixY = 0
    matrix = []
    
    # Variable para ayudar a ubicar rapidamente la posicion del jugador
    playerRow = -1
    playerCol = -1
    
    # Listas con las coordenadas de las cajas
    boxes = []
    
    # Variable de depuracion
    steps = 0
    pushes = 0
    h = -1
    
    
    playerCount = 0
    boxCount = 0
    endBoxCount = 0
    placeCount = 0
    
    ###########################################################################
    # Constructor de la clase
    ###########################################################################
    
    # Genera un nuevo estado a partir de un mapeo
    def __init__(self, map):
        self.matrix = copy.deepcopy(map)        
        
        self.playerCount = 0
        self.boxCount = 0
        self.endBoxCount = 0
        self.placeCount = 0
        for column in map:
            for item in column:
                if item == CHAR_PLAYER or item == CHAR_PLAYER_S:
                    self.playerCount += 1
                    if item == CHAR_PLAYER_S:
                        self.placeCount += 1
                elif item == CHAR_BOX:
                    self.boxCount += 1
                elif item == CHAR_BOX_S:
                    self.endBoxCount += 1
                elif item == CHAR_SPACE_S:
                    self.placeCount += 1
        
        if self.playerCount > 1:
            errorMsg = "__init__: estado con mas de un jugador."
            raise Exception(errorMsg)
        
        if self.boxCount != self.placeCount:
            errorMsg = "__init__: cantidad de cajas no coincide con lugares."
            raise Exception(errorMsg)
            
        self.boxes = ListBoxes(self)
        self.steps = 0
        self.pushes = 0
    
    # Crea una copia del estado actual
    def clone(self):
        newState = SokobanState(self.matrix)
        newState.playerRow = self.playerRow
        newState.playerCol = self.playerCol
        newState.matrixX = self.matrixX
        newState.matrixY = self.matrixY
        newState.steps = self.steps
        newState.pushes = self.pushes
        return newState
    
    ###################################
    # Validaciones para movimiento
    ###################################
    def canMove(self, move):
        direction = getMoveDirection(move)
        if direction == MOVE_UP:
            return self.canMoveDir(0, -1)
        elif direction == MOVE_DOWN:
            return self.canMoveDir(0, 1)
        elif direction == MOVE_LEFT:
            return self.canMoveDir(-1, 0)
        elif direction == MOVE_RIGHT:
            return self.canMoveDir(1, 0)
        else:
            return False
    
    def canMoveDir(self, row, col):
        pos1 = self.getItemR(row, col)           # Adelante
        pos2 = self.getItemR(2 * row, 2 * col)   # a 2 pasos
        
        if pos1 == CHAR_BOX or pos1 == CHAR_BOX_S:
            if pos2 == CHAR_SPACE or pos2 == CHAR_SPACE_S:
                return True
            else:
                return False
        elif pos1 == CHAR_SPACE or pos1 == CHAR_SPACE_S:
            return True
        else:
            return False
    
    # Verifica si al mover una caja, esta quedara en una esquina
    def isForbidenPosition(self, row, col, move):
        direction = getMoveDirection(move)
        
        pos1 = self.getItem(row, col)
        if pos1 == CHAR_SPACE_S or pos1 == CHAR_BOX_S or pos1 == CHAR_PLAYER_S:
            #si esta es una posicion final, se puede dejar la caja
            return False
        
        if direction == MOVE_UP:
            pos2 = self.getItem(row - 1, col) #arriba
            pos3 = self.getItem(row, col - 1) #izquierda
            pos4 = self.getItem(row, col + 1) #derecha
        elif direction == MOVE_DOWN:
            pos2 = self.getItem(row + 1, col) #abajo
            pos3 = self.getItem(row, col - 1) #izquierda
            pos4 = self.getItem(row, col + 1) #derecha
        elif direction == MOVE_LEFT:
            pos2 = self.getItem(row, col - 1) #izquierda
            pos3 = self.getItem(row + 1, col) #abajo
            pos4 = self.getItem(row - 1, col) #arriba
        elif direction == MOVE_RIGHT:
            pos2 = self.getItem(row, col + 1) #derecha
            pos3 = self.getItem(row + 1, col) #abajo
            pos4 = self.getItem(row - 1, col) #arriba
        
        if pos2 == CHAR_WALL:
            if pos3 == CHAR_WALL or pos4 == CHAR_WALL:
                return True
            else:
                return False
        else:
            return False
    
    ###############################################
    # Validaciones para movimiento en reversa
    ###############################################
    
    def canMoveReverse(self, move, pull):
        direction = getMoveDirection(move)
        if direction == MOVE_UP:
            return self.canMoveReverseDir(-1, 0, pull)
        elif direction == MOVE_DOWN:
            return self.canMoveReverseDir(1, 0, pull)
        elif direction == MOVE_LEFT:
            return self.canMoveReverseDir(0, -1, pull)
        elif direction == MOVE_RIGHT:
            return self.canMoveReverseDir(0, 1, pull)
        else:
            return False        
    
    def canMoveReverseDir(self, row, col, pull):
        pos0 = self.getItemR(-row, -col) # Adelante
        pos2 = self.getItemR(row, col)   # Atras
    
        if pos0 == CHAR_SPACE or pos0 == CHAR_SPACE_S:
            if not pull:
                return True
            if pull and (pos2 == CHAR_BOX or pos2 == CHAR_BOX_S):
                return True
        else:
            return False
    
    ###########################################################################
    # Movimientos del jugador
    ###########################################################################
        
    # Decide a que direccion mover al jugador
    def movePlayer(self, move):
        try:
            direction = getMoveDirection(move)
            row, col = getDir(direction)
            self.movePlayerDir(row, col)
            
            self.boxes = ListBoxes(self)
            self.steps += 1
            if isPushingBox(move):
                self.pushes += 1
        except Exception as ex:
            if direction == MOVE_UP:
                errorMsg = "Error al mover al jugador hacia arriba[" + str(move) + "]"
            elif direction == MOVE_DOWN:
                errorMsg = "Error al mover al jugador hacia abajo[" + str(move) + "]"
            elif direction == MOVE_LEFT:
                errorMsg = "Error al mover al jugador hacia izquierda[" + str(move) + "]"
            elif direction == MOVE_RIGHT:
                errorMsg = "Error al mover al jugador hacia derecha[" + str(move) + "]"
            else:
                errorMsg = "Error al mover[" + str(move) + "]"
            errorMsg += " desde " + printCoords(self.playerRow, self.playerCol)
            errorMsg = "MovePlayer: " + errorMsg
            raise Exception(errorMsg, ex)
    
    # Realiza los cambios en el laberinto para mover al jugador
    def movePlayerDir(self, row, col):
        # Validacion para detectar movimientos invalidos
        if (row == 0 and col == 0) or (row != 0 and col != 0) or (row > 1 or row < -1) or (col > 1 or col < -1):
            raise Exception("MovePlayerDir: direccion [" + str(row) + "," + str(col) + "] invalida")
        
        try:
            pos0 = self.getItemR(0, 0)           # Posicion del jugador
            pos1 = self.getItemR(row, col)           # Adelante
            
            
            if pos1 == CHAR_WALL:
                return False # No se puede mover al jugador a una pared
            
            # si a 1 paso hay una caja, se debe empujarla a 2 pasos
            if pos1 == CHAR_BOX or pos1 == CHAR_BOX_S: 
                pos2 = self.getItemR(2 * row, 2 * col)   # a 2 pasos
                
                if pos2 == CHAR_SPACE: # Espacio vacio
                    self.setItemR(2 * row, 2 * col, CHAR_BOX) #Mover la caja al espacio
                elif pos2 == CHAR_SPACE_S: # Espacio vacio de meta
                    self.setItemR(2 * row, 2 * col, CHAR_BOX_S) #Mover la caja a la meta
                else: #otro elemento no vacio
                    return False #No se puede mover la caja a un lugar no vacio
            
            # determina que colocar en la posicion original del jugador
            if pos0 == CHAR_PLAYER_S:
                self.setItemR(0, 0, CHAR_SPACE_S)
            elif pos0 == CHAR_PLAYER:
                self.setItemR(0, 0, CHAR_SPACE)
            else:
                return False # Si pasa por aqui hay error en el programa
            
            # Determina como escribir al jugador
            if pos1 == CHAR_BOX or pos1 == CHAR_SPACE: #espacio normal
                self.setItemR(row, col, CHAR_PLAYER) 
            elif pos1 == CHAR_BOX_S or pos1 == CHAR_SPACE_S: #meta
                self.setItemR(row, col, CHAR_PLAYER_S)
            else:
                return False # Si para por aqui, hay error en el programa
            
            # Actualizar la ubicacion del jugador
            self.playerRow += row
            self.playerCol += col
        except Exception as ex:
            errorMsg = "MovePlayerDir: Error al mover jugador"
            raise Exception(errorMsg, ex)
    
    ###########################################################################
    # Movimiento del jugador en reversa
    ###########################################################################
    
    # Decide a que direccion mover al jugador en reversa
    def movePlayerReverse(self, move, pull):
        direction = getMoveDirecion(move)
        row, col = getDir(direction)
        self.movePlayerDir(row, col, pull)
         
        self.boxesX, self.boxesY = ListBoxes(self)
        self.steps += 1
        if isPushingBox(move):
            self.pushes += 1
    
    # Realiza los cambios en el laberinto para mover al jugador en reversa
    def movePlayerDirReverse(self, row, col, pull):
        # Validacion para detectar movimientos invalidos
        if (row == 0 and col == 0) \
        or (row != 0 and col != 0) \
        or (row > 1 or row < -1) \
        or (col > 1 or col < -1):
            return False
        
        pos0 = self.getItemR(-row, -col)    # Adelante
        pos1 = self.getItemR(0, 0)          # Posicion del jugador
        pos2 = self.getItemR(row, col)      # Atras
        
        if pos0 == CHAR_WALL or pos0 == CHAR_BOX or pos0 == CHAR_BOX_S:
            return False # No se puede mover al jugador a una pared
        
        # Determina que colocar en pos2
        if pull:
            if pos2 == CHAR_BOX:
                self.setItemR(row, col, CHAR_SPACE) #Mover la caja
            elif pos2 == CHAR_BOX_S:
                self.setItemR(row, col, CHAR_SPACE_S) #Mover la caja
            else: #otro elemento no vacio
                return False #No se puede mover la caja a un lugar no vacio
            
        # Determina como escribir pos0
        if pos0 == CHAR_SPACE: #espacio normal
            self.setItemR(-row, -col, CHAR_PLAYER) 
        elif pos0 == CHAR_SPACE_S: #meta
            self.setItemR(-row, -col, CHAR_PLAYER_S)
        else:
            return False # Si para por aqui, hay error en el programa
        
        # determina que colocar en pos1
        if pull:
            if pos1 == CHAR_PLAYER_S:
                self.setItem(0, 0, CHAR_BOX_S)
            elif pos1 == CHAR_PLAYER:
                self.setItemR(0, 0, CHAR_BOX)
            else:
                return False # Si pasa por aqui hay error en el programa
        else:
            if pos1 == CHAR_PLAYER_S:
                self.setItem(0, 0, CHAR_SPACE_S)
            elif pos1 == CHAR_PLAYER:
                self.setItemR(0, 0, CHAR_SPACE)
            else:
                return False # Si pasa por aqui hay error en el programa
        
        # Actualizar la ubicacion del jugador
        self.playerRow -= row
        self.playerCol -= col
    
    ###########################################################################
    # Super movimiento
    ###########################################################################
    def superMovePlayer(self, movement):
        row, col, move = movement
        
        if self.playerRow != row or self.playerCol != col:
            steps = countSteps(self, row, col)
            
            here = self.getItemR(0, 0)
            there = self.getItem(row, col)
            
            if here == CHAR_PLAYER:
                self.setItemR(0, 0, CHAR_SPACE)
            elif here == CHAR_PLAYER_S:
                self.setItemR(0, 0, CHAR_SPACE_S)
            else:
                errorMsg = "Jugador no presente en la posicion actual"
                raise Exception(errorMsg)
            
            if there == CHAR_SPACE:
                self.setItem(row, col, CHAR_PLAYER)
            elif there == CHAR_SPACE_S:
                self.setItem(row, col, CHAR_PLAYER_S)
            else:
                errorMsg = "Jugador no puede moverse a posicion de destino" + chr(10) + "Desde " + printCoords(self.playerRow, self.playerCol) + " hasta " + printCoords(row, col)
                raise Exception(errorMsg)

            self.playerRow = row
            self.playerCol = col
        else:
            steps = 0
        
        self.steps += steps
        
        self.movePlayer(move)
        
    ###########################################################################
    # Super movimiento en reversa
    ###########################################################################
    
    
    #######################################################
    # Propiedad Item:
    # Obtiene o establece un item del laberinto
    # con posicion absoluta
    #######################################################
    def getItem(self, row, col):
        if validPosition(self, row, col):
            return self.matrix[row][col]
        else:
            #manejar error de coordenadas incorrectas
            errorMsg = "GetItem: Coordenadas " + printCoords(row, col) + " invalidas"
            raise Exception(errorMsg)
            
    def setItem(self, row, col, value):
        if validPosition(self, row, col):
            pos0 = self.matrix[row][col]
            
            if pos0 == CHAR_PLAYER or pos0 == CHAR_PLAYER_S:
                #print "chau"
                self.playerCount -= 1
            if pos0 == CHAR_WALL:
                errorMsg = "SetItem: No se puede modificar pared en " + printCoords(row, col) + "!"
                errorMsg += "\nJugador en " + printCoords(self.playerRow, self.playerCol) + "\n"
                #errorMsg += "".join(printTable(self.matrirow, "Error"))
                raise Exception(errorMsg)
            if (value == CHAR_PLAYER or value == CHAR_PLAYER_S):
                if self.playerCount > 0:
                    errorMsg = "SetItem: No puede haber mas de un jugador en el laberinto."
                    raise Exception(errorMsg)
                else:
                    #print "hola"
                    self.playerCount += 1
            self.matrix[row][col] = value
        else:
            #manejar error de coordenadas incorrectas
            errorMsg = "SetItem: Coordenadas " + printCoords(row, col) + " invalidas"
            raise Exception(errorMsg)
    
    #######################################################
    # Propiedad ItemR:
    # Obtiene o establece un item del laberinto
    # en posicion relativa al jugador
    #######################################################
    def getItemR(self, row, col):
        return self.getItem(self.playerRow + row, self.playerCol + col)
    def setItemR(self, row, col, value):
        self.setItem(self.playerRow + row, self.playerCol + col, value)
    
    ######################################
    # Sobrecarga de __eq__ col __hash__ 
    # para comparacion de estados
    ######################################
    def __eq__(self, other):
        if other is self:
            #si tienen la misma posicion de memoria
            return True
        if isinstance(other, SokobanState):
            if self.playerRow != other.playerRow or self.playerCol != other.playerCol:
                #si el jugador no esta en el mismo lugar
                return False
            else:
                if len(self.boxes) != len(other.boxes):
                    #si no hay la misma cantidad de cajas
                    return False
                else:
                    for i in range(len(self.boxes)):
                        if self.boxes[i][0] != other.boxes[i][0] \
                        or self.boxes[i][1] != other.boxes[i][1]:
                            #posicion de caja no coincide
                            return False
                    return True
        else:
            #si no corresponde a la misma clase
            return False
    def __hash__(self):
        h = hash(self.matrixX)
        h = h ^ hash(self.matrixY)
        h = h ^ hash(self.playerRow)
        h = h ^ hash(self.playerCol)
        for box in self.boxes:
            h = h ^ hash(box[0])
            h = h ^ hash(box[1])
        return h
    
    ###########################################
    # Funciones auxiliares de depuracion
    ###########################################
    def printTable(self):
        print "Steps: ", self.steps, " Pushes: ", self.pushes
        for i in self.matrix:
            print "".join(i)
    
    def printTableDebug(self):
        self.h = SokobanHeuristic(self)
        print "Steps:", self.steps, " Pushes: ", self.pushes, " Heuristic:", self.h
        for i in self.matrix:
            print "".join(i)
    
##############################################
# Funciones varias
##############################################

# Verifica si las coordenadas proporcionadas se encuentran dentro
# de los limites del laberinto
def validPosition(state, row, col):
    return (0 <= row and row < state.matrixX) and (0 <= col and col < state.matrixY)

def validRelPosition(state, row, col):
    if row == 0 and (col == 1 or col == -1) \
    or col == 0 and (row == 1 or row == -1):
        return True
    else:
        return False
    
# Genera una lista de las coordenadas de las cajas en el laberinto
def ListBoxes(state):
    list=[]
    
    try:
        col=0
        for column in state.matrix:
            row=0
            for position in column:
                if position == CHAR_BOX or position == CHAR_BOX_S:
                    list.append((row, col))
                row += 1
            col += 1
    except Exception as ex:
        errorMsg = "Error al listar las cajas en el laberinto"
        raise Exception(errorMsg, ex)
    
    return list

###############################################################################
# Funcion para generar la cuenta de pasos para que el jugador se desplace
# entre dos posiciones
###############################################################################
def countSteps(state, endRow, endCol):
    startRow = state.playerRow
    startCol = state.playerCol
    
    if startRow == endRow and startCol == endCol:
        return 0
    
    if distance(startRow, startCol, endRow, endCol) > 1:
        table = copy.deepcopy(state.matrix)
        
        here = table[startRow][startCol]
        there = table[endRow][endCol]
        
        #Marca la meta
        table[endRow][endCol] = 'X'
        posQueue = FIFOQueue()
        if here == CHAR_PLAYER:
            table[startRow][startCol] = CHAR_SPACE
        elif here == CHAR_PLAYER_S:
            table[startRow][startCol] = CHAR_SPACE_S
        else:
            errorMsg = "Solo se puede contar pasos desde la posicion del jugador."
            errorMsg += " Aqui" + printCoords(state.playerRow, state.playerCol) + ": \"" + here + "\""
            errorMsg += " Alla" + printCoords(endRow, endCol) + ": \"" + there + "\""
            raise Exception(errorMsg)
    
        posQueue = countStepsRec(table, posQueue, startRow, startCol, endRow, endCol, 0)
    
        while len(posQueue) > 0:
            #printTable(table, str(len(posQueue)))

            currentRow, currentCol, c = posQueue.pop()
            
            #si llegamos a la posicion final
            if table[currentRow][currentCol] == 'X':
                #retornar la cantidad de pasos dados
                return c
        
            posQueue = countStepsRec(table, posQueue, currentRow, currentCol, endRow, endCol, c)
    
        errorMsg = "No se puede mover desde " + printCoords(startRow, startCol) \
                + " hasta " + printCoords(endRow, endCol) + "."
        raise Exception(errorMsg)
    else:
        return 1
    
def countStepsRec(table, posQueue, currentRow, currentCol, endRow, endCol, steps):
    here = table[currentRow][currentCol]
    
    # Marco esta posicion como visitada
    if here == CHAR_SPACE:
        table[currentRow][currentCol] = CHAR_PLAYER
    elif here == CHAR_SPACE_S:
        table[currentRow][currentCol] = CHAR_PLAYER_S
    else:
        return posQueue
    
    #verifico lo que hay alrededor
    up = table[currentRow - 1][currentCol]
    down = table[currentRow + 1][currentCol]
    left = table[currentRow][currentCol - 1]
    right = table[currentRow][currentCol + 1]
    
    if up == 'X' or down == 'X' or left == 'X' or right == 'X':
        posQueue = FIFOQueue()
        posQueue.append((endRow, endCol, steps + 1))
    else:
        #si se puede avanzar, poner las nuevas posiciones en la cola
        if up == CHAR_SPACE or up == CHAR_SPACE_S:
            posQueue.append((currentRow - 1, currentCol, steps + 1))
        if down == CHAR_SPACE or down == CHAR_SPACE_S:
            posQueue.append((currentRow + 1, currentCol, steps + 1))
        if left == CHAR_SPACE or left == CHAR_SPACE_S:
            posQueue.append((currentRow, currentCol - 1, steps + 1))
        if right == CHAR_SPACE or right == CHAR_SPACE_S:
            posQueue.append((currentRow, currentCol + 1, steps + 1))
    
    return posQueue

###############################################################################
# Funcion que genera los estados intermedios entre dos pasos
###############################################################################
def generateStates(states, prev, next):
    a = 0
    
    return states

