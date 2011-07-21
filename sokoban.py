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
from problem import SokobanProblem
from problem import generateGoalState

from tpIAsokobanparser import obtenerMapa

printTableFather = False

def main():
    columna = 0
    fila = 0
    if len(sys.argv)==2 or len(sys.argv)==3:
        if sys.argv[1]=="-v":
            printTableFather = True
            initial = obtenerMapa(sys.argv[2], fila, columna)
        else:
            initial = obtenerMapa(sys.argv[1], fila, columna)
            
        goal = generateGoalState(initial) #encontrar el estado final
        sokoban = SokobanProblem(initial, goal) 
        
        x1= time.strftime('%S')
        
        search = astar_search(sokoban)
        
        if search:
            pathS = search.path()
            
            x2= time.strftime('%S')
            timediff = int(x2) - int(x1)
            
            #Genera la secuencia de estados
            path = [node.state for node in pathS]
            states = []
            
            for state in path:
                states.append(state)
            
            i = len(states) - 1
            while i >= 0:
                states[i].printTable()
                print
                i -= 1
                
            print 'Tiempo:', timediff,'segundos'
        else:
            print "No se pudo encontrar la solucion al problema"
    else:
        if len(sys.argv)<2:
            print "Debe recibir el nombre del archivo..."
        if len(sys.argv)>3:
            print "Demasiados arguementos..."

if __name__ == "__main__":
    main()

#depth_first_graph_search(sokoban)
#depth_limited_search(sokoban)
#iterative_deepening_search(sokoban)
