from ai import Problem
from ai import astar_search
from ai import iterative_deepening_search
from ai import depth_first_tree_search
from tpIAsokobanparser import obtenerMapa
import copy

def findPlayer(state):
    x=0
    for i in state:
        y=0
        for j in i:
            if j=='@':
                return x, y
            y+=1
        x+=1
    return False, False

def canMove(x, y, listMoves,  state):
    try :
        if state[x+1][y]==' ':
            listMoves.append(0)
        if state[x-1][y]==' ':
            listMoves.append(1)
        if state[x][y+1]==' ':
            listMoves.append(2)
        if state[x][y-1]==' ':
            listMoves.append(3)
        if state[x+1][y]=='$' and state[x+2][y]==' ' :
            listMoves.append(4)  
        if state[x-1][y]=='$'and state[x-2][y]==' ' :
            listMoves.append(5)
        if state[x][y+1]=='$'and state[x][y+2]==' ' :
            listMoves.append(6)
        if state[x][y-1]=='$'and state[x][y-2]==' ' :
            listMoves.append(7)
        return listMoves
    except:
        return listMoves
        
def move(x, y,  listMoves, listStates,  state):
    stateS = copy.deepcopy(state)
    stateS[x][y]=' '
    try :
        for i in listMoves:
            if i==0:
                stateS[x+1][y]= '@'
                listStates.append(copy.deepcopy(stateS))     #copia la tabla y la agrega a la lista de posible movidas
                stateS[x+1][y]= ' '                                      #"cerar" la tabla
            if i==1:
                stateS[x-1][y]= '@'
                listStates.append(copy.deepcopy(stateS))
                stateS[x-1][y]= ' '
            if i==2:
                stateS[x][y+1]= '@'
                listStates.append(copy.deepcopy(stateS))
                stateS[x][y+1]= ' '
            if i==3:
                stateS[x][y-1]= '@'
                listStates.append(copy.deepcopy(stateS))
                stateS[x][y-1]= ' '
            if i==4:
                stateS[x+1][y]= '@'
                stateS[x+2][y]='$'
                listStates.append(copy.deepcopy(stateS))
                stateS[x+1][y]= ' '
                stateS[x+2][y]=' '
            if i==5:
                stateS[x-1][y]= '@'
                stateS[x-2][y]='$'
                listStates.append(copy.deepcopy(stateS))
                stateS[x-1][y]= ' '
                stateS[x-2][y]= ' '
            if i==6:
                stateS[x][y+1]= '@'
                stateS[x][y+2]='$'
                listStates.append(copy.deepcopy(stateS))
                stateS[x][y+1]= ' '
                stateS[x][y+2]= ' '
            if i==7:
                stateS[x][y-1]= '@'
                stateS[x][y-2]='$'
                listStates.append(copy.deepcopy(stateS))
                stateS[x][y-1]= ' '
                stateS[x][y-2]= ' '
        return listStates
    except:
        return  listStates
#funcion constructor
class sokobanProblem(Problem):      #hereda la clase Problem de ai.py
    def _init_(self):                                #constructor
        self.initial=self                               #recibe la tabla de juego y construye
    def successor(self, state):                 #funcion sucesora
        listMoves=[]                                #lista para posibles movimientos
        listStates=[]                               #lista para posibles estados de la tabla
        x, y = findPlayer(state)                #encontrar donde esta el jugador
        canMove(x, y,listMoves,  state)     #puede moverse????  
        if not listMoves:                             #si la lista esta vacia, no hay movimientos posibles por ende no posibles sucesores
            return []                                     #retorna lista vacia la funcion sucesor
        else:                                                 #si la lista tiene algo!!
            move(x, y, listMoves ,  listStates, state)      #con listMoves hago los posibles movimientos en listStates
            new =  copy.deepcopy(state)                     #debug
            print "-----------padre"                            
            for i in new:
                print "".join(i)
            print "-----------finpadre"                     #debug
#            print "-----------hijos"
#            for i in listStates:
#                for j in i:
#                    print "".join(j)
#            print "-----------finhijos"
            raw_input()                                                   #debug      
            return [(moveA, wichMove(moveA, listStates, listMoves)) for moveA in listMoves] #arma una lista de pares por ejemplo [(A,B),(C,D)]
            #en este caso un par de movimiento y la tabla que se movio
    def h(self):
        return 1


def wichMove(moveA, listStates, listMoves):
    try:
        return listStates[listMoves.index(moveA)]
    except:
        return []
        

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

def distPlayerToBox(state):
    return
    

goal = obtenerMapa("workfile")
initial = copy.deepcopy(goal) #copia real
goal = findGoalState(goal) #encontrar el estado final
sokoban = sokobanProblem(initial, goal) 
#depth_first_tree_search(sokoban).path()
iterative_deepening_search(sokoban)
