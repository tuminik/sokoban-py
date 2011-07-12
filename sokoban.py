from ai import Problem
from ai import astar_search
from ai import iterative_deepening_search
from ai import depth_first_tree_search
from tpIAsokobanparser import obtenerMapa
import copy
import parser

def findPlayer(state):
    x=0
    for i in state:
        y=0
        for j in i:
            if j=='@':
                return x, y
            y+=1
        x+=1

def canMove(x, y, state):
    try :
        if state[x+1][y]==' ':
            return True, 1
        if state[x-1][y]==' ':
            return True, 2
        if state[x][y+1]==' ':
            return True, 3
        if state[x][y-1]==' ':
            return True, 4
        return False, 0
    except:
        return False, 0
        
def move(x, y, where, state):
    try :
        state[x][y]=' '
        if where==1:
            state[x+1][y]= '@'
            #return  "X+1", state
        if where==2:
            state[x-1][y]='@'
            #return "X-1", state
        if where==3:
            state[x][y+1]='@'
            #return "Y+1", state
        if where==4:
            state[x][y-1]='@'
            #return "Y-1", state
        return state
    except:
        return  state

class sokobanProblem(Problem):   #hereda la clase Problem de ai.py
    def _init_(self):
        self.initial=self
    def successor(self, state):
        x, y = findPlayer(state)
        canMoveBool,  canMoveWhere = canMove(x, y, state)
        if not canMoveBool:
            return []
        else:
            state = move(x, y, canMoveWhere, state)
            new =  copy.deepcopy(state)
            print "-----------"
            for i in new:
                print "".join(i)
            print "-----------"
            return [(canMoveWhere, new)]

def findGoalState(table):
    x=0
    for i in table:
        y=0
        for j in i:
            if j=='$':
                table[x][y]=' '
            y+=1
        x+=1
    x=0
    for i in table:
        y=0
        for j in i:
            if j=='.':
                table[x][y]='$'
            y+=1
        x+=1
    return table


goal = obtenerMapa("workfile")
initial = copy.deepcopy(goal) #copia real
goal = findGoalState(goal) #encontrar el estado final
sokoban = sokobanProblem(initial, goal) 
print [node.state for node in iterative_deepening_search(sokoban).path()]
#iterative_deepening_search(sokoban)
