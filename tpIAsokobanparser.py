#!/usr/bin/env python
import sys

caracteres = ['#', ' ', '.', '@', '+', '$', '*', '\n']
global columna
columna = 0
global fila
fila = 0

def validaCaracteres(linea): #verifica si los caracteres extraidos del archivo son validos
	for i in range(len(linea)):
		if linea[i] not in caracteres:
			print linea[i], i #imprime el caracter invalido y la posicion
			sys.exit("algun caracter no es aceptado")#al no ser validos detiene la ejecucion
			
def imprimir(lista):
	for i in range(len(lista)):
		#for j in range(len(lista[i])):
			print lista[i]#[j]
		
def obtieneTamFilCol(linea): #obtiene las dimensiones del mapa
	global columna
	global fila
	if len(linea) > columna: #obtiene la columna
		columna = len(linea)
				
	fila += 1 #obtiene la fila
	
def obtenerIndice(linea):
    try:
        if linea.index('#') < linea.index('.') and linea.index('#') < linea.index('@') and linea.index('#') < linea.index('+') and linea.index('#') < linea.index('*') and linea.index('#') < linea.index('$'):
            return linea.index('#')
        elif linea.index('.') < linea.index('#') and linea.index('.') < linea.index('@') and linea.index('.') < linea.index('+') and linea.index('.') < linea.index('*') and linea.index('.') < linea.index('$'):
            return linea.index('.')
        elif linea.index('@') < linea.index('.') and linea.index('@') < linea.index('#') and linea.index('@') < linea.index('+') and linea.index('@') < linea.index('*') and linea.index('@') < linea.index('$'):
            return linea.index('@')
        elif linea.index('+') < linea.index('.') and linea.index('+') < linea.index('@') and linea.index('+') < linea.index('#') and linea.index('+') < linea.index('*') and linea.index('+') < linea.index('$'):
            return linea.index('+')
        elif linea.index('*') < linea.index('.') and linea.index('*') < linea.index('@') and linea.index('*') < linea.index('+') and linea.index('*') < linea.index('#') and linea.index('*') < linea.index('$'):
            return linea.index('*')
        elif linea.index('$') < linea.index('.') and linea.index('$') < linea.index('@') and linea.index('$') < linea.index('+') and linea.index('$') < linea.index('#') and linea.index('$') < linea.index('*'):
            return linea.index('$')
    except:
        return False
def rellenarEspaciosBlancos(linea):
	linea2 = []
	linea2 = list(linea)
	linea2[len(linea2) - 1] = '#'
	for i in range(obtenerIndice(linea)):#(linea.index('#'))
		linea2[i] = '#'
	return linea2
	
def encuadrarLista(lista):
    for i in range(len(lista)):
        for j in range(columna - len(lista[i])):
            lista[i].append('#')
    return lista
    
def verificaPriUltFila(lista):
	for i in range(len(lista[0])):
		if lista[0][i] != '#':
			lista[0][i] = '#'
	for i in range(len(lista[fila - 1])):
		if lista[fila - 1][i] != '#':
			lista[fila - 1][i] = '#'
	return lista

def obtenerMapa():
	lista =[]
	with open('workfile', 'r') as f: #abre y cierra el archivo apropiadamente incluso si se genero una excepcion
		for linea in f:
			validaCaracteres(linea)
			obtieneTamFilCol(linea)
			lista.append(rellenarEspaciosBlancos(linea)) #carga linea por linea el archivo a la lista
	f.closed
	return verificaPriUltFila(encuadrarLista(lista))
		
#main
if __name__ == "__main__":
	imprimir(obtenerMapa())
	print fila, columna
	
