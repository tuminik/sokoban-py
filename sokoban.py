#!/usr/bin/env python

import sys
import copy
import time

from ai import Problem
from ai import astar_search
from ai import iterative_deepening_search
from ai import depth_first_tree_search
from ai import depth_first_graph_search
from ai import breadth_first_tree_search
from ai import breadth_first_graph_search
from ai import depth_limited_search

from constantes import *

from heuristic import SokobanHeuristic
from state import SokobanState
from state import generateStates
from problem import SokobanProblem
from problem import generateGoalState

from tpIAsokobanparser import obtenerMapa

def main():
    columna = 0
    fila = 0
    if len(sys.argv)==2 or len(sys.argv)==3:
        if Debug():
            initial = obtenerMapa(sys.argv[2], fila, columna)
        else:
            initial = obtenerMapa(sys.argv[1], fila, columna)
        
        goal = generateGoalState(initial) #encontrar el estado final
        sokoban = SokobanProblem(initial, goal) 
        
        #Mide el tiempo antes de iniciar la busqueda
        x1= time.time()
        
        search = astar_search(sokoban)
        
        #Mide el tiempo al finalizar la busqueda
        x2= time.time()
        timediff = x2 - x1 #Saca la diferencia de tiempo
        
        if search:
            pathS = search.path()
            
            #Genera la secuencia de estados
            path = [node.state for node in pathS]
            states = []
            
            for state in path:
                if len(states) > 0:
                    #Verifica si hay mas de un paso entre dos estados
                    prev = states[len(states) - 1]
                    if distance(prev.playerRow, prev.playerCol, state.playerRow, state.playerCol) > 1:
                        #Genera los estados intermedios
                        states = generateStates(states, prev, state)
                
                #Agrega el nuevo estado a la lista
                states.append(state)
            
            #Saca la lista de estados, revirtiendo el orden
            i = len(states) - 1
            while i >= 0:
                states[i].printTable()
                print
                i -= 1
        else:
            print "No se pudo encontrar la solucion al problema"
        
        print 'Tiempo:', round(timediff,4),'segundos'
        print "Nodos expandidos:", sokoban.expanded
    else:
        if len(sys.argv) < 2:
            print "Debe recibir el nombre del archivo..."
        if len(sys.argv) > 3:
            print "Demasiados arguementos..."

if __name__ == "__main__":
    main()

#depth_first_graph_search(sokoban)
#depth_limited_search(sokoban)
#iterative_deepening_search(sokoban)
