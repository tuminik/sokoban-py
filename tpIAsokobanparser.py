#!/usr/bin/env python
import sys

from state import SokobanState
from constantes import *

# Lista de caracteres permitidos dentro de un archivo
caracteres = [CHAR_WALL, 
              CHAR_SPACE, 
              CHAR_SPACE_S, 
              CHAR_PLAYER, 
              CHAR_PLAYER_S, 
              CHAR_BOX, 
              CHAR_BOX_S, 
              '\n',
			  '\t']

def imprimir(lista):
    for i in range(len(lista)):
        #for j in range(len(lista[i])):
            print lista[i]#[j]
            
def findPlayer(lista, fila, columna):
    for i in range(fila):
        if obtenerIndiceLinea(lista[i], columna, CHAR_PLAYER) != columna:
            return i, obtenerIndiceLinea(lista[i], columna, CHAR_PLAYER)
        if obtenerIndiceLinea(lista[i], columna, CHAR_PLAYER_S) != columna:
            return i, obtenerIndiceLinea(lista[i], columna, CHAR_PLAYER_S)
            
def cantidadChar(lista, fila, char):
    cantidad = 0
    for i in range(fila):
        cantidad += lista[i].count(char)
        
    return cantidad
    
def encuadrarLista(lista, columna):
    for i in range(len(lista)):
         for j in range(columna - len(lista[i])):
            lista[i].append(CHAR_WALL)
    return lista

def verificaPriUltFila(lista, fila):
    for i in range(len(lista[0])):
        if lista[0][i] != CHAR_WALL:
            lista[0][i] = CHAR_WALL
    for i in range(len(lista[fila - 1])):
        if lista[fila - 1][i] != CHAR_WALL:
            lista[fila - 1][i] = CHAR_WALL
    return lista

def obtenerIndiceLinea(linea, columna, char):
    try:
        return linea.index(char)
    except:
        return columna

def obtenerIndice(linea, columna):
    if obtenerIndiceLinea(linea, columna, CHAR_WALL) < obtenerIndiceLinea(linea, columna, CHAR_SPACE_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_WALL) < obtenerIndiceLinea(linea, columna, CHAR_PLAYER) \
    and obtenerIndiceLinea(linea, columna, CHAR_WALL) < obtenerIndiceLinea(linea, columna, CHAR_PLAYER_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_WALL) < obtenerIndiceLinea(linea, columna, CHAR_BOX_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_WALL) < obtenerIndiceLinea(linea, columna, CHAR_BOX):
        return obtenerIndiceLinea(linea, columna, CHAR_WALL)
    elif obtenerIndiceLinea(linea, columna, CHAR_SPACE_S) < obtenerIndiceLinea(linea, columna, CHAR_WALL) \
    and obtenerIndiceLinea(linea, columna, CHAR_SPACE_S) < obtenerIndiceLinea(linea, columna, CHAR_PLAYER) \
    and obtenerIndiceLinea(linea, columna, CHAR_SPACE_S) < obtenerIndiceLinea(linea, columna, CHAR_PLAYER_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_SPACE_S) < obtenerIndiceLinea(linea, columna, CHAR_BOX_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_SPACE_S) < obtenerIndiceLinea(linea, columna, CHAR_BOX):
        return obtenerIndiceLinea(linea, columna, CHAR_SPACE_S)
    elif obtenerIndiceLinea(linea, columna, CHAR_PLAYER) < obtenerIndiceLinea(linea, columna, CHAR_SPACE_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_PLAYER) < obtenerIndiceLinea(linea, columna, CHAR_WALL) \
    and obtenerIndiceLinea(linea, columna, CHAR_PLAYER) < obtenerIndiceLinea(linea, columna, CHAR_PLAYER_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_PLAYER) < obtenerIndiceLinea(linea, columna, CHAR_BOX_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_PLAYER) < obtenerIndiceLinea(linea, columna, CHAR_BOX):
        return obtenerIndiceLinea(linea, CHAR_PLAYER)
    elif obtenerIndiceLinea(linea, columna, CHAR_PLAYER_S) < obtenerIndiceLinea(linea, columna, CHAR_SPACE_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_PLAYER_S) < obtenerIndiceLinea(linea, columna, CHAR_PLAYER) \
    and obtenerIndiceLinea(linea, columna, CHAR_PLAYER_S) < obtenerIndiceLinea(linea, columna, CHAR_WALL) \
    and obtenerIndiceLinea(linea, columna, CHAR_PLAYER_S) < obtenerIndiceLinea(linea, columna, CHAR_BOX_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_PLAYER_S) < obtenerIndiceLinea(linea, columna, CHAR_BOX):
        return obtenerIndiceLinea(linea, columna, CHAR_PLAYER_S)
    elif obtenerIndiceLinea(linea, columna, CHAR_BOX_S) < obtenerIndiceLinea(linea, columna, CHAR_SPACE_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_BOX_S) < obtenerIndiceLinea(linea, columna, CHAR_PLAYER) \
    and obtenerIndiceLinea(linea, columna, CHAR_BOX_S) < obtenerIndiceLinea(linea, columna, CHAR_PLAYER_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_BOX_S) < obtenerIndiceLinea(linea, columna, CHAR_WALL) \
    and obtenerIndiceLinea(linea, columna, CHAR_BOX_S) < obtenerIndiceLinea(linea, columna, CHAR_BOX):
        return obtenerIndiceLinea(linea, columna, CHAR_BOX_S)
    elif obtenerIndiceLinea(linea, columna, CHAR_BOX) < obtenerIndiceLinea(linea, columna, CHAR_SPACE_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_BOX) < obtenerIndiceLinea(linea, columna, CHAR_PLAYER) \
    and obtenerIndiceLinea(linea, columna, CHAR_BOX) < obtenerIndiceLinea(linea, columna, CHAR_PLAYER_S) \
    and obtenerIndiceLinea(linea, columna, CHAR_BOX) < obtenerIndiceLinea(linea, columna, CHAR_WALL) \
    and obtenerIndiceLinea(linea, columna, CHAR_BOX) < obtenerIndiceLinea(linea, columna, CHAR_BOX_S):
        return obtenerIndiceLinea(linea, columna, CHAR_BOX)
    return len(linea)
    
def rellenarEspaciosBlancos(columna, linea):
    linea2 = []
    linea2 = list(linea)
    linea2[len(linea2) - 1] = CHAR_WALL
    for i in range(obtenerIndice(linea, columna)):
        linea2[i] = CHAR_WALL
    return linea2
    
def obtieneTamFilCol(columna, fila, linea): #obtiene las dimensiones del mapa
    if len(linea) > columna: #obtiene la columna
        columna = len(linea)
                
    fila += 1 #obtiene la fila
    return fila, columna
    
def validaCaracteres(linea): #verifica si los caracteres extraidos del archivo son validos
    for i in range(len(linea)):
        if linea[i] not in caracteres:
            print linea[i], i #imprime el caracter invalido y la posicion
            sys.exit("algun caracter no es aceptado, Arreglelo!!")#al no ser validos detiene la ejecucion

def obtenerMapa(filename, fila, columna):
    lista =[]
    with open(filename, 'r') as f: #abre y cierra el archivo apropiadamente incluso si se genero una excepcion
        for linea in f:
            validaCaracteres(linea)
            fila, columna = obtieneTamFilCol(columna, fila, linea)
            lista.append(rellenarEspaciosBlancos(columna, linea)) #carga linea por linea el archivo a la lista
    f.closed
    if cantidadChar(lista, fila, CHAR_SPACE_S) + cantidadChar(lista, fila, CHAR_PLAYER_S) != cantidadChar(lista, fila, CHAR_BOX):
        sys.exit("La cantidad de cajas no coincide con la cantidad de lugares, Arreglelo!!")
    elif not cantidadChar(lista, fila, CHAR_SPACE_S):
        sys.exit("No se encontraron ni cajas, ni lugares, Arreglelo!!")
    if not (cantidadChar(lista, fila, CHAR_PLAYER) + cantidadChar(lista, fila, CHAR_PLAYER_S)):
        sys.exit("No se encuentra al jugador, Agreguelo!!")
    elif cantidadChar(lista, fila, CHAR_PLAYER) > 1 or cantidadChar(lista, fila, CHAR_PLAYER_S) > 1 \
    or cantidadChar(lista, fila, CHAR_PLAYER) + cantidadChar(lista, fila, CHAR_PLAYER_S) > 1:
        sys.exit("Existe mas de un jugador, Agreguelo!!")
    else:
        lista = verificaPriUltFila(encuadrarLista(lista, columna), fila)
    #try
    estado = SokobanState(lista)
    estado.matrixX = fila
    estado.matrixY = columna
    estado.playerRow, estado.playerCol = findPlayer(lista, fila, columna)
    return estado
    #except:   
    #    return lista

#main
#if __name__ == "__main__":
#a = obtenerMapa("workfile")
#print a
#    #imprimir(obtenerMapa("workfile"))
#    print fila, columna
