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
    playerX = -1
    playerY = -1
    
    # Listas con las coordenadas de las cajas
    boxes = []
    
    # Variable de depuracion
    steps = 0
    pushes = 0
    h = -1
    
    ###########################################################################
    # Constructor de la clase
    ###########################################################################
    
    # Genera un nuevo estado a partir de un mapeo
    def __init__(self, map):
        self.matrix = copy.deepcopy(map)
        
        """
        #self.matrixX = 0
        #self.matrixY = 0
        x = 0
        for column in map:
            y = 0
            for item in column:
                if item == CHAR_PLAYER or item == CHAR_PLAYER_S:
                    self.playerX = x
                    self.playerY = y
                y += 1
                
                # verifica el tamanho de la matriz
                if self.matrixY < y + 1:
                    self.matrixY = y
            x += 1
            
            # verifica el tamanho de la matriz
            if self.matrixX < x + 1:
                self.matrixX = x
        """
        
        self.boxes = ListBoxes(self)
        self.steps = 0
        self.pushes = 0
    
    # Crea una copia del estado actual
    def clone(self):
        newState = SokobanState(self.matrix)
        newState.playerX = self.playerX
        newState.playerY = self.playerY
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
    
    def canMoveDir(self, x, y):
        pos1 = self.getItemR(x, y)           # Adelante
        pos2 = self.getItemR(2 * x, 2 * y)   # a 2 pasos
        
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
    def isForbidenPosition(self, x, y, move):
        direction = getMoveDirection(move)
        
        pos1 = self.getItem(x, y)
        if pos1 == CHAR_SPACE_S or pos1 == CHAR_BOX_S or pos1 == CHAR_PLAYER_S:
            #si esta es una posicion final, se puede dejar la caja
            return False
        
        if direction == MOVE_UP:
            pos2 = self.getItem(x, y - 1) #arriba
            pos3 = self.getItem(x - 1, y) #izquierda
            pos4 = self.getItem(x + 1, y) #derecha
        elif direction == MOVE_DOWN:
            pos2 = self.getItem(x, y + 1) #abajo
            pos3 = self.getItem(x - 1, y) #izquierda
            pos4 = self.getItem(x + 1, y) #derecha
        elif direction == MOVE_LEFT:
            pos2 = self.getItem(x - 1, y) #izquierda
            pos3 = self.getItem(x, y + 1) #abajo
            pos4 = self.getItem(x, y - 1) #arriba
        elif direction == MOVE_RIGHT:
            pos2 = self.getItem(x + 1, y) #derecha
            pos3 = self.getItem(x, y + 1) #abajo
            pos4 = self.getItem(x, y - 1) #arriba
        
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
            return self.canMoveReverseDir(0, -1, pull)
        elif direction == MOVE_DOWN:
            return self.canMoveReverseDir(0, 1, pull)
        elif direction == MOVE_LEFT:
            return self.canMoveReverseDir(-1, 0, pull)
        elif direction == MOVE_RIGHT:
            return self.canMoveReverseDir(1, 0, pull)
        else:
            return False        
    
    def canMoveReverseDir(self, x, y, pull):
        pos0 = self.getItemR(-x, -y) # Adelante
        pos2 = self.getItemR(x, y)   # Atras
    
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
            if direction == MOVE_UP:
                self.movePlayerDir(0, -1)
            elif direction == MOVE_DOWN:
                self.movePlayerDir(0, 1)
            elif direction == MOVE_LEFT:
                self.movePlayerDir(-1, 0)
            elif direction == MOVE_RIGHT:
                self.movePlayerDir(1, 0)  
            else:
                raise Exception("Movimiento invalido")
            
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
            errorMsg += " desde " + printCoords(self.playerX, self.playerY)
            errorMsg = "MovePlayer: " + errorMsg
            raise Exception(errorMsg, ex)
    
    # Realiza los cambios en el laberinto para mover al jugador
    def movePlayerDir(self, x, y):
        # Validacion para detectar movimientos invalidos
        if (x == 0 and y == 0) or (x != 0 and y != 0) or (x > 1 or x < -1) or (y > 1 or y < -1):
            raise Exception("MovePlayerDir: direccion [" + str(x) + "," + str(y) + "] invalida")
        
        try:
            pos0 = self.getItemR(0, 0)           # Posicion del jugador
            pos1 = self.getItemR(x, y)           # Adelante
            
            
            if pos1 == CHAR_WALL:
                return False # No se puede mover al jugador a una pared
            
            # si a 1 paso hay una caja, se debe empujarla a 2 pasos
            if pos1 == CHAR_BOX or pos1 == CHAR_BOX_S: 
                pos2 = self.getItemR(2 * x, 2 * y)   # a 2 pasos
                
                if pos2 == CHAR_SPACE: # Espacio vacio
                    self.setItemR(2 * x, 2 * y, CHAR_BOX) #Mover la caja al espacio
                elif pos2 == CHAR_SPACE_S: # Espacio vacio de meta
                    self.setItemR(2 * x, 2 * y, CHAR_BOX_S) #Mover la caja a la meta
                else: #otro elemento no vacio
                    return False #No se puede mover la caja a un lugar no vacio
            
            # Determina como escribir al jugador
            if pos1 == CHAR_BOX or pos1 == CHAR_SPACE: #espacio normal
                self.setItemR(x, y, CHAR_PLAYER) 
            elif pos1 == CHAR_BOX_S or pos1 == CHAR_SPACE_S: #meta
                self.setItemR(x, y, CHAR_PLAYER_S)
            else:
                return False # Si para por aqui, hay error en el programa
            
            # determina que colocar en la posicion original del jugador
            if pos0 == CHAR_PLAYER_S:
                self.setItemR(0, 0, CHAR_SPACE_S)
            elif pos0 == CHAR_PLAYER:
                self.setItemR(0, 0, CHAR_SPACE)
            else:
                return False # Si pasa por aqui hay error en el programa
            
            # Actualizar la ubicacion del jugador
            self.playerX += x
            self.playerY += y
        except Exception as ex:
            errorMsg = "MovePlayerDir: Error al mover jugador"
            raise Exception(errorMsg, ex)
    
    ###########################################################################
    # Movimiento del jugador en reversa
    ###########################################################################
    
    # Decide a que direccion mover al jugador en reversa
    def movePlayerReverse(self, move, pull):
        direction = getMoveDirecion(move)
        if direction == MOVE_UP:
            r = self.movePlayerDir(0, -1, pull)
        elif direction == MOVE_DOWN:
            r = self.movePlayerDir(0, 1, pull)
        elif direction == MOVE_LEFT:
            r = self.movePlayerDir(-1, 0, pull)
        elif direction == MOVE_RIGHT:
            r = self.movePlayerDir(1, 0, pull)
        else:
            return False
         
        if r:
            self.boxesX, self.boxesY = ListBoxes(self)
            self.steps += 1
            if isPushingBox(move):
                self.pushes += 1
    
    # Realiza los cambios en el laberinto para mover al jugador en reversa
    def movePlayerDirReverse(self, x, y, pull):
        # Validacion para detectar movimientos invalidos
        if (x == 0 and y == 0) \
        or (x != 0 and y != 0) \
        or (x > 1 or x < -1) \
        or (y > 1 or y < -1):
            return False
        
        pos0 = self.getItemR(-x, -y)    # Adelante
        pos1 = self.getItemR(0, 0)      # Posicion del jugador
        pos2 = self.getItemR(x, y)      # Atras
        
        if pos0 == CHAR_WALL or pos0 == CHAR_BOX or pos0 == CHAR_BOX_S:
            return False # No se puede mover al jugador a una pared
        
        # Determina que colocar en pos2
        if pull:
            if pos2 == CHAR_BOX:
                self.setItemR(x, y, CHAR_SPACE) #Mover la caja
            elif pos2 == CHAR_BOX_S:
                self.setItemR(x, y, CHAR_SPACE_S) #Mover la caja
            else: #otro elemento no vacio
                return False #No se puede mover la caja a un lugar no vacio
            
        # Determina como escribir pos0
        if pos0 == CHAR_SPACE: #espacio normal
            self.setItemR(-x, -y, CHAR_PLAYER) 
        elif pos0 == CHAR_SPACE_S: #meta
            self.setItemR(-x, -y, CHAR_PLAYER_S)
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
        self.playerX -= x
        self.playerY -= y
    
    ###########################################################################
    # Super movimiento
    ###########################################################################
    def superMovePlayer(self, movement):
        x, y, move = movement
        
        if self.playerX != x or self.playerY != y:
            steps = countSteps(self, x, y)
            
            here = self.getItemR(0, 0)
            there = self.getItem(x, y)
            
            if here == CHAR_PLAYER:
                self.setItemR(0, 0, CHAR_SPACE)
            elif here == CHAR_PLAYER_S:
                self.setItemR(0, 0, CHAR_SPACE_S)
            else:
                errorMsg = "Jugador no presente en la posicion actual"
                raise Exception(errorMsg)
            
            if there == CHAR_SPACE:
                self.setItem(x, y, CHAR_PLAYER)
            elif there == CHAR_SPACE_S:
                self.setItem(x, y, CHAR_PLAYER_S)
            else:
                errorMsg = "Jugador no puede moverse a posicion de destino" + chr(10) + "Desde " + printCoords(self.playerX, self.playerY) + " hasta " + printCoords(x, y)
                raise Exception(errorMsg)
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
    def getItem(self, x, y):
        if validPosition(self, x, y):
            return self.matrix[x][y]
        else:
            #manejar error de coordenadas incorrectas
            errorMsg = "GetItem: Coordenadas " + printCoords(x, y) + " invalidas"
            raise Exception(errorMsg)
            
    def setItem(self, x, y, value):
        if validPosition(self, x, y):
            if self.matrix[x][y] == CHAR_WALL:
                errorMsg = "No se puede modificar pared en " + printCoords(x, y) + "!"
                errorMsg += "\nJugador en " + printCoords(self.playerX, self.playerY) + "\n"
                #errorMsg += "".join(printTable(self.matrix, "Error"))
                raise Exception(errorMsg)
            self.matrix[x][y] = value
        else:
            #manejar error de coordenadas incorrectas
            errorMsg = "SetItem: Coordenadas " + printCoords(x, y) + " invalidas"
            raise Exception(errorMsg)
    
    #######################################################
    # Propiedad ItemR:
    # Obtiene o establece un item del laberinto
    # en posicion relativa al jugador
    #######################################################
    def getItemR(self, x, y):
        return self.getItem(self.playerX + x, self.playerY + y)
    def setItemR(self, x, y, value):
        self.setItem(self.playerX + x, self.playerY + y, value)
    
    ######################################
    # Sobrecarga de __eq__ y __hash__ 
    # para comparacion de estados
    ######################################
    def __eq__(self, other):
        if other is self:
            #si tienen la misma posicion de memoria
            return True
        if isinstance(other, SokobanState):
            if self.playerX != other.playerX or self.playerY != other.playerY:
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
        h = h ^ hash(self.playerX)
        h = h ^ hash(self.playerY)
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
def validPosition(state, x, y):
    return (0 <= x and x < state.matrixX) and (0 <= y and y < state.matrixY)

def validRelPosition(state, x, y):
    if x == 0 and (y == 1 or y == -1) \
    or y == 0 and (x == 1 or x == -1):
        return True
    else:
        return False
    
# Genera una lista de las coordenadas de las cajas en el laberinto
def ListBoxes(state):
    list=[]
    x=0
    
    try:
        for column in state.matrix:
            y=0
            for position in column:
                if position == CHAR_BOX or position == CHAR_BOX_S:
                    list.append((x, y))
                y += 1
            x += 1
    except Exception as ex:
        errorMsg = "Error al listar las cajas en el laberinto"
        raise Exception(errorMsg, ex)
    
    return list

def countSteps(state, endX, endY):
    startX = state.playerX
    startY = state.playerY
    
    if startX == endX and startY == endY:
        return 0
    
    table = copy.deepcopy(state.matrix)
    
    posQueue = FIFOQueue()
    if table[startX][startY] == CHAR_PLAYER:
        table[startX][startY] = CHAR_SPACE
    elif table[startX][startY] == CHAR_PLAYER_S:
        table[startX][startY] = CHAR_SPACE_S
    else:
        raise Exception("Solo se puede contar pasos desde la posicion del jugador. " + printCoords(state.playerX, state.playerY) + " -> " + printCoords(endX, endY))
    
    posQueue = countStepsRec(table, posQueue, startX, startY, endX, endY, 0)
    
    while len(posQueue) > 0:
        currentX, currentY, c = posQueue.pop()
        
        #si llegamos a la posicion final
        if currentX == endX and currentY == endY:
            #retornar la cantidad de pasos dados
            return c
        
        posQueue = countStepsRec(table, posQueue, currentX, currentY, endX, endY, c)
    
    errorMsg = "No se puede mover desde " + printCoords(startX, startY) + " hasta " + printCoords(endX, endY) + "."
    raise Exception(errorMsg)
    
def countStepsRec(table, posQueue, currentX, currentY, endX, endY, steps):
    here = table[currentX][currentY]
    
    # Marco esta posicion como visitada
    if here == CHAR_SPACE:
        table[currentX][currentY] = CHAR_PLAYER
    elif here == CHAR_SPACE_S:
        table[currentX][currentY] = CHAR_PLAYER_S
    else:
        return posQueue
    
    #verifico lo que hay alrededor
    up = table[currentX][currentY - 1]
    down = table[currentX][currentY + 1]
    left = table[currentX - 1][currentY]
    right = table[currentX + 1][currentY]
    
    #si se puede avanzar, poner las nuevas posiciones en la cola
    if up == CHAR_SPACE or up == CHAR_SPACE_S:
        posQueue.append((currentX, currentY - 1, steps + 1))
    if down == CHAR_SPACE or down == CHAR_SPACE_S:
        posQueue.append((currentX, currentY + 1, steps + 1))
    if left == CHAR_SPACE or left == CHAR_SPACE_S:
        posQueue.append((currentX - 1, currentY, steps + 1))
    if right == CHAR_SPACE or right == CHAR_SPACE_S:
        posQueue.append((currentX + 1, currentY, steps + 1))
    
    return posQueue
