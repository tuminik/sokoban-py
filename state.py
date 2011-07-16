#!/usr/bin/env python

class state:

    # Variables que definen las dimensiones del laberinto
    matrixX=0
    matrixY=0
    matrix=[]
    
    # Variable para ayudar a ubicar rapidamente la posicion del jugador
    playerX=-1
    playerY=-1
    
    def __init__(self, prevState, move):
        # Copia las dimensiones del laberinto
        self.matrixX = prevState.matrixX
        self.matrixY = prevState.matrixY
        
        # Copia la matriz que representa el laberinto
        self.matrix = copy.deepcopy(prevState.matrix)
        
        # Copia la posicion actual del jugador
        self.playerX = prevState.playerX
        self.playerY = prevState.playerY
        
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
        else
            return False
    
    # Realiza los cambios en el laberinto para mover al jugador hacia arriba
    def movePlayerDir(self, x, y):
        # Validacion para detectar movimientos invalidos
        if (x == 0 and y == 0) or (x != 0 and y != 0) or (x > 1 or x < -1) or (y > 1 or y < -1):
            return False
        
        if pos1 == CHAR_WALL:
            return False # No se puede mover al jugador a una pared

        
        pos0 = self.getItemR(0, 0)           # Determino lo que hay a 0 pasos
        pos1 = self.getItemR(x, y)           # Determino lo que hay a 1 paso
        pos2 = self.getItemR(2 * x, 2 * y)   # Determino lo que hay a 2 pasos
        
        # si a 1 paso hay una caja, se debe empujarla a 2 pasos
        if pos1 == CHAR_BOX or pos1 == CHAR_BOX_S: 
                    
            if pos2 == CHAR_SPACE: # Espacio vacio
                self.setItemR(2 * x, 2 * y, CHAR_BOX) #Mover la caja al espacio
            elif pos2 == CHAR_SPACE_S: # Espacio vacio de meta
                self.setItemR(2 * x, 2 * y, CHAR_BOX_S) #Mover la caja a la meta
            else #otro elemento no vacio
                return False #No se puede mover la caja a un lugar no vacio
        
        # Determina como escribir al jugador
        if pos1 == CHAR_BOX or pos1 == CHAR_SPACE: #espacio normal
            self.setItemR(x, y, CHAR_PLAYER) 
        elif pos1 == CHAR_BOX_S or pos1 == CHAR_SPACE_S: #meta
            self.setItemR(x, y, CHAR_PLAYER_S)
        else
            return False # Si para por aqui, hay error en el programa
    
        # determina que colocar en la posicion original del jugador
        if pos0 == CHAR_PLAYER_S:
            self.setItem(0, 0, CHAR_SPACE_S)
        elif pos0 == CHAR_PLAYER:
            self.setItemR(0, 0, CHAR_SPACE)
        else
            return False # Si pasa por aqui hay error en el programa
    
        # Actualizar la ubicacion del jugador
        self.playerX += x
        self.playerY += y
    
    
    # Obtiene el valor de un item dentro del laberinto
    def getItem(self, x, y):
        if self.validPosition(x, y)
            return self.matrix[x][y]
        else
            #manejar error de coordenadas incorrectas
            return False
    
	def __getItem__(self, x):
	    return self.matrix[x]
	
    # Obtiene el valor de una posicion relativa al jugador
    def getItemR(self, x, y):
        return self.getItem(self.playerX + x, self.playerY + y)
    
    # Establece el valor de un item dentro del laberinto
    def setItem(self, x, y, value):
        if self.validPosition(x, y)
            self.matrix[x][y] = value
        else
            #manejar error de coordenadas incorrectas
    
    # Establece el valor de una posicion relativa al jugador
    def setItemR(self, x, y, value):
        self.setItem(self.playerX + x, self.playerY + y, value)
    
    # Verifica si las coordenadas proporcionadas se encuentran dentro
    # de los limites del laberinto
    def validPosition(self, x, y):
        return (0 <= x and x < self.matrixX) and (0 <= y and y < self.matrixY)
    