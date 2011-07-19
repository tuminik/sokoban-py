#!/usr/bin/env python

import copy
from constantes import *

class sokobanState:

    # Variables que definen las dimensiones del laberinto
    matrixX=0
    matrixY=0
    matrix=[]
    
    # Variable para ayudar a ubicar rapidamente la posicion del jugador
    playerX=-1
    playerY=-1
    
    # Genera un nuevo estado a partir de un mapeo
    def __init__(self, map):
        self.matrix = copy.deepcopy(map)
        self.matrixX = 0
        self.matrixY = 0
        
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

    def clone(self):
        newState = sokobanState(self.matrix)
        return newState
    
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
            
    def canMoveReverse(self, move, pull):
        direction = getMoveDirection(move)
        if direction == MOVE_UP:
            return self.canMoveDirReverse(0, -1, pull)
        elif direction == MOVE_DOWN:
            return self.canMoveDirReverse(0, 1, pull)
        elif direction == MOVE_LEFT:
            return self.canMoveDirReverse(-1, 0, pull)
        elif direction == MOVE_RIGHT:
            return self.canMoveDirReverse(1, 0, pull)
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
            
    def canMoveDirReverse(self, x, y, pull):
        pos0 = self.getItemR(-x, -y) # Adelante
        pos2 = self.getItemR(x, y)   # Atras
    
        if pos0 == CHAR_SPACE or pos0 == CHAR_SPACE_S:
            if not pull:
                return True
            if pull and (pos2 == CHAR_BOX or pos2 == CHAR_BOX_S):
                return True
        else:
            return False
    
    # Decide a que direccion mover al jugador
    def movePlayer(self, move):
        direction = getMoveDirection(move)
        if direction == MOVE_UP:
            return self.movePlayerDir(0, -1)
        elif direction == MOVE_DOWN:
            return self.movePlayerDir(0, 1)
        elif direction == MOVE_LEFT:
            return self.movePlayerDir(-1, 0)
        elif direction == MOVE_RIGHT:
            return self.movePlayerDir(1, 0)  
        else:
            return False
    
    # Decide a que direccion mover al jugador en reversa
    def movePlayerReverse(self, move, pull):
        direction = getMoveDirecion(move)
        if direction == MOVE_UP:
            return self.movePlayerDir(0, -1, pull)
        elif direction == MOVE_DOWN:
            return self.movePlayerDir(0, 1, pull)
        elif direction == MOVE_LEFT:
            return self.movePlayerDir(-1, 0, pull)
        elif direction == MOVE_RIGHT:
            return self.movePlayerDir(1, 0, pull)
        else:
            return False
    
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
            self.setItem(0, 0, CHAR_SPACE_S)
        elif pos0 == CHAR_PLAYER:
            self.setItemR(0, 0, CHAR_SPACE)
        else:
            return False # Si pasa por aqui hay error en el programa
        
        # Actualizar la ubicacion del jugador
        self.playerX += x
        self.playerY += y
    
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

    # Obtiene el valor de un item dentro del laberinto
    def getItem(self, x, y):
        if self.validPosition(x, y):
            return self.matrix[x][y]
        else:
            #manejar error de coordenadas incorrectas
            return False
    
    def __getItem__(self, x):
        return self.matrix[x]
    
    # Obtiene el valor de una posicion relativa al jugador
    def getItemR(self, x, y):
        return self.getItem(self.playerX + x, self.playerY + y)
    
    # Establece el valor de un item dentro del laberinto
    def setItem(self, x, y, value):
        if self.validPosition(x, y):
            self.matrix[x][y] = value
        else:
            return False
            #manejar error de coordenadas incorrectas
    
    # Establece el valor de una posicion relativa al jugador
    def setItemR(self, x, y, value):
        self.setItem(self.playerX + x, self.playerY + y, value)
    
    # Verifica si las coordenadas proporcionadas se encuentran dentro
    # de los limites del laberinto
    def validPosition(self, x, y):
        return (0 <= x and x < self.matrixX) and (0 <= y and y < self.matrixY)
    
# Busca el jugador dentro del laberinto
def findPlayer(state):
    x=0
    for i in state.matrix:
        y=0
        for j in i:
            if j == CHAR_PLAYER or j == CHAR_PLAYER_S:
                return x, y
            y+=1
        x+=1
    return False, False
