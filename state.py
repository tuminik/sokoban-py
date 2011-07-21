#!/usr/bin/env python

import copy
from constantes import *
from debug import *

class sokobanState:
    
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
    boxesX = []
    boxesY = []
    
    # Variable de depuracion
    steps = 0
    
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
        
        self.boxesX, self.boxesY = ListBoxes(self)
        self.steps = 0
    
    # Crea una copia del estado actual
    def clone(self):
        newState = sokobanState(self.matrix)
        newState.playerX = self.playerX
        newState.playerY = self.playerY
        newState.matrixX = self.matrixX
        newState.matrixY = self.matrixY
        newState.steps = self.steps
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
            
            self.boxesX, self.boxesY = ListBoxes(self)
            self.steps += 1
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
            
            raise Exception(errorMsg, ex)
    
    # Realiza los cambios en el laberinto para mover al jugador
    def movePlayerDir(self, x, y):
        # Validacion para detectar movimientos invalidos
        if (x == 0 and y == 0) or (x != 0 and y != 0) or (x > 1 or x < -1) or (y > 1 or y < -1):
            return False
        
        pos0 = self.getItemR(0, 0)           # Posicion del jugador
        pos1 = self.getItemR(x, y)           # Adelante
        pos2 = self.getItemR(2 * x, 2 * y)   # a 2 pasos
        
        if pos1 == CHAR_WALL:
            return False # No se puede mover al jugador a una pared
        
        # si a 1 paso hay una caja, se debe empujarla a 2 pasos
        if pos1 == CHAR_BOX or pos1 == CHAR_BOX_S: 
                    
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
            errorMsg = "GetItem: Coordenadas " + ImprimirCoordenadas(x, y) + " invalidas"
            raise Exception(errorMsg)
    def setItem(self, x, y, value):
        if validPosition(self, x, y):
            if self.matrix[x][y] == CHAR_WALL:
                errorMsg = "No se puede modificar pared en " + ImprimirCoordenadas(x, y) + "!"
                errorMsg += "\nJugador en " + ImprimirCoordenadas(self.playerX, self.playerY) + "\n"
                #errorMsg += "".join(printTable(self.matrix, "Error"))
                raise Exception(errorMsg)
            self.matrix[x][y] = value
        else:
            #manejar error de coordenadas incorrectas
            errorMsg = "SetItem: Coordenadas " + ImprimirCoordenadas(x, y) + " invalidas"
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
        if isinstance(other, sokobanState):
            if self.playerX != other.playerX or self.playerY != other.playerY:
                #si el jugador no esta en el mismo lugar
                return False
            else:
                if len(self.boxesX) != len(other.boxesX) \
                or len(self.boxesY) != len(other.boxesY):
                    #si no hay la misma cantidad de cajas
                    return False
                else:
                    for x in range(len(self.boxesX)):
                        for y in range(len(self.boxesY)):
                            if self.boxesX[x] != other.boxesX[x] \
                            or self.boxesY[y] != other.boxesY[y]:
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
        for boxX in self.boxesX:
            h = h ^ hash(boxX)
        for boxY in self.boxesY:
            h = h ^ hash(boxY)
        return h
    
    def printTable(self):
        for i in self.matrix:
            print "".join(i)
    
    def printTableDebug(self):
        print "Steps:" , self.steps
        for i in self.matrix:
            print "".join(i)
    
##############################################
# Funciones varias
##############################################

# Verifica si las coordenadas proporcionadas se encuentran dentro
# de los limites del laberinto
def validPosition(state, x, y):
    return (0 <= x and x < state.matrixX) and (0 <= y and y < state.matrixY)

# Genera una lista de las coordenadas de las cajas en el laberinto
def ListBoxes(state):
    xlist=[]
    ylist=[]
    x=0
    for column in state.matrix:
        y=0
        for position in column:
            if position == CHAR_BOX or position == CHAR_BOX_S:
                xlist.append(x)
                ylist.append(y)
            y += 1
        x += 1
    
    return xlist, ylist

def ImprimirCoordenadas(x, y):
    return "[" + str(x) + "," + str(y) + "]"

def ImprimirDireccion(move):
    direction = getMoveDirection(move)
    if direction == MOVE_UP:
        return "UP"
    elif direction == MOVE_DOWN:
        return "DOWN"
    elif direction == MOVE_LEFT:
        return "LEFT"
    elif direction == MOVE_RIGHT:
        return "RIGHT"
    else:
        return "INVALIDO"
