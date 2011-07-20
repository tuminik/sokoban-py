#!/usr/bin/env python
import sys
from state import sokobanState

caracteres = ['#', ' ', '.', '@', '+', '$', '*', '\n']
			
def imprimir(lista):
	for i in range(len(lista)):
		#for j in range(len(lista[i])):
			print lista[i]#[j]
			
def findPlayer(lista, fila, columna, char):
	for i in range(fila):
		if obtenerIndiceLinea(lista[i], columna, char) != columna:
			return i, obtenerIndiceLinea(lista[i], columna, char)
			
def cantidadChar(lista, fila, char):
	cantidad = 0
	for i in range(fila):
		cantidad += lista[i].count(char)
		
	return cantidad
	
def encuadrarLista(lista, columna):
    for i in range(len(lista)):
         for j in range(columna - len(lista[i])):
            lista[i].append('#')
    return lista

def verificaPriUltFila(lista, fila):
	for i in range(len(lista[0])):
		if lista[0][i] != '#':
			lista[0][i] = '#'
	for i in range(len(lista[fila - 1])):
		if lista[fila - 1][i] != '#':
			lista[fila - 1][i] = '#'
	return lista

def obtenerIndiceLinea(linea, columna, char):
	try:
		return linea.index(char)
	except:
		return columna

def obtenerIndice(linea, columna):
	if obtenerIndiceLinea(linea, columna, '#') < obtenerIndiceLinea(linea, columna, '.') \
	and obtenerIndiceLinea(linea, columna, '#') < obtenerIndiceLinea(linea, columna, '@') \
	and obtenerIndiceLinea(linea, columna, '#') < obtenerIndiceLinea(linea, columna, '+') \
	and obtenerIndiceLinea(linea, columna, '#') < obtenerIndiceLinea(linea, columna, '*') \
	and obtenerIndiceLinea(linea, columna, '#') < obtenerIndiceLinea(linea, columna, '$'):
		return obtenerIndiceLinea(linea, columna, '#')
	elif obtenerIndiceLinea(linea, columna, '.') < obtenerIndiceLinea(linea, columna, '#') \
	and obtenerIndiceLinea(linea, columna, '.') < obtenerIndiceLinea(linea, columna, '@') \
	and obtenerIndiceLinea(linea, columna, '.') < obtenerIndiceLinea(linea, columna, '+') \
	and obtenerIndiceLinea(linea, columna, '.') < obtenerIndiceLinea(linea, columna, '*') \
	and obtenerIndiceLinea(linea, columna, '.') < obtenerIndiceLinea(linea, columna, '$'):
		return obtenerIndiceLinea(linea, columna, '.')
	elif obtenerIndiceLinea(linea, columna, '@') < obtenerIndiceLinea(linea, columna, '.') \
	and obtenerIndiceLinea(linea, columna, '@') < obtenerIndiceLinea(linea, columna, '#') \
	and obtenerIndiceLinea(linea, columna, '@') < obtenerIndiceLinea(linea, columna, '+') \
	and obtenerIndiceLinea(linea, columna, '@') < obtenerIndiceLinea(linea, columna, '*') \
	and obtenerIndiceLinea(linea, columna, '@') < obtenerIndiceLinea(linea, columna, '$'):
		return obtenerIndiceLinea(linea, '@')
	elif obtenerIndiceLinea(linea, columna, '+') < obtenerIndiceLinea(linea, columna, '.') \
	and obtenerIndiceLinea(linea, columna, '+') < obtenerIndiceLinea(linea, columna, '@') \
	and obtenerIndiceLinea(linea, columna, '+') < obtenerIndiceLinea(linea, columna, '#') \
	and obtenerIndiceLinea(linea, columna, '+') < obtenerIndiceLinea(linea, columna, '*') \
	and obtenerIndiceLinea(linea, columna, '+') < obtenerIndiceLinea(linea, columna, '$'):
		return obtenerIndiceLinea(linea, columna, '+')
	elif obtenerIndiceLinea(linea, columna, '*') < obtenerIndiceLinea(linea, columna, '.') \
	and obtenerIndiceLinea(linea, columna, '*') < obtenerIndiceLinea(linea, columna, '@') \
	and obtenerIndiceLinea(linea, columna, '*') < obtenerIndiceLinea(linea, columna, '+') \
	and obtenerIndiceLinea(linea, columna, '*') < obtenerIndiceLinea(linea, columna, '#') \
	and obtenerIndiceLinea(linea, columna, '*') < obtenerIndiceLinea(linea, columna, '$'):
		return obtenerIndiceLinea(linea, columna, '*')
	elif obtenerIndiceLinea(linea, columna, '$') < obtenerIndiceLinea(linea, columna, '.') \
	and obtenerIndiceLinea(linea, columna, '$') < obtenerIndiceLinea(linea, columna, '@') \
	and obtenerIndiceLinea(linea, columna, '$') < obtenerIndiceLinea(linea, columna, '+') \
	and obtenerIndiceLinea(linea, columna, '$') < obtenerIndiceLinea(linea, columna, '#') \
	and obtenerIndiceLinea(linea, columna, '$') < obtenerIndiceLinea(linea, columna, '*'):
		return obtenerIndiceLinea(linea, columna, '$')
	
def rellenarEspaciosBlancos(columna, linea):
	linea2 = []
	linea2 = list(linea)
	linea2[len(linea2) - 1] = '#'
	for i in range(obtenerIndice(linea, columna)):
		linea2[i] = '#'
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
    if cantidadChar(lista, fila, '.') != cantidadChar(lista, fila, '$'):
        sys.exit("La cantidad de cajas no coincide con la cantidad de lugares, Arreglelo!!")
    elif not cantidadChar(lista, fila, '.'):
        sys.exit("No se encontraron ni cajas, ni lugares, Arreglelo!!")
    if not cantidadChar(lista, fila, '@'):
        sys.exit("No se encuentra al jugador, Agreguelo!!")
    elif cantidadChar(lista, fila, '@') > 1:
        sys.exit("Existe mas de un jugador, Agreguelo!!")
    else:
        lista = verificaPriUltFila(encuadrarLista(lista, columna), fila)
    #try
    estado = sokobanState(lista)
    estado.matrixX = fila
    estado.matrixY = columna
    estado.playerX, estado.playerY = findPlayer(lista, fila, columna, '@')
    return estado
    #except:   
    #    return lista

#main
#if __name__ == "__main__":
#a = obtenerMapa("workfile")
#print a
#    #imprimir(obtenerMapa("workfile"))
#    print fila, columna
    
