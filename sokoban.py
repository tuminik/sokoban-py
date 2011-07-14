from ai import Problem
from ai import astar_search
from ai import iterative_deepening_search
from ai import depth_first_tree_search
from ai import depth_first_graph_search
from ai import breadth_first_tree_search
from ai import breadth_first_graph_search
from ai import depth_limited_search
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
    tableS = Table()
    tableS.table= copy.deepcopy(state)
    tableS.table[x][y]=' '
    try :
        for i in listMoves:
            if i==0:
                tableS.table[x+1][y]= '@'
                listStates.append(copy.deepcopy(tableS))     #copia la tabla y la agrega a la lista de posible movidas
                tableS.table[x+1][y]= ' '                                      #"cerar" la tabla
            if i==1:
                tableS.table[x-1][y]= '@'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x-1][y]= ' '
            if i==2:
                tableS.table[x][y+1]= '@'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x][y+1]= ' '
            if i==3:
                tableS.table[x][y-1]= '@'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x][y-1]= ' '
            if i==4:
                tableS.table[x+1][y]= '@'
                tableS.table[x+2][y]='$'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x+1][y]= ' '
                tableS.table[x+2][y]=' '
            if i==5:
                tableS.table[x-1][y]= '@'
                tableS.table[x-2][y]='$'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x-1][y]= ' '
                tableS.table[x-2][y]= ' '
            if i==6:
                tableS.table[x][y+1]= '@'
                tableS.table[x][y+2]='$'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x][y+1]= ' '
                tableS.table[x][y+2]= ' '
            if i==7:
                tableS.table[x][y-1]= '@'
                tableS.table[x][y-2]='$'
                listStates.append(copy.deepcopy(tableS))
                tableS.table[x][y-1]= ' '
                tableS.table[x][y-2]= ' '
        return listStates
    except:
        return  listStates
#funcion constructor


class SokobanProblem(Problem):      #hereda la clase Problem de ai.py
    def _init_(self):
        self.initial=self                            #recibe la tabla de juego y construye
    def successor(self, state):                         #funcion sucesora
        listMoves=[]                                             #lista para posibles movimientos
        listStates=[]                                           #lista para posibles estados de la tabla
        x, y = findPlayer(state.table)                            #encontrar donde esta el jugador
        canMove(x, y,listMoves,  state.table)                 #puede moverse????  
        if not listMoves:                                           #si la lista esta vacia, no hay movimientos posibles por ende no posibles sucesores
            return []                                                   #retorna lista vacia la funcion sucesor
        else:                                                               #si la lista tiene algo!!
            move(x, y, listMoves ,  listStates, state.table)      #con listMoves hago los posibles movimientos en listStates
            new =  copy.deepcopy(state.table)                     #debug
            print "-----------padre"                            
            for i in new:
                print "".join(i)
            print "-----------finpadre"                     #debug
#            print "-----------hijos"
#            for i in listStates:
#                for j in i.table:
#                    print "".join(j)
#            print "-----------finhijos"
            raw_input()                                                   #debug      
            return [(moveA, wichMove(moveA, listStates, listMoves)) for moveA in listMoves] #arma una lista de pares por ejemplo [(A,B),(C,D)]
            #en este caso un par de movimiento y la tabla que se movio
    
    def h(self, node):
        c=0
        listBoxes=[]
        listPlaces=[]
        x, y = findPlayer(node.state.table)
        listBoxes = findBoxes(listBoxes, node.state.table)
        listPlaces = findPlaces(listPlaces, node.state.table)
        for i in listBoxes:
            xB, yB = i
            c+=distancePlayerToBox(x, y, xB, yB)
            for j in listPlaces:
                xP, yP = j
                c+=distancePlacesToBoxes(xP, yP, xB, yB)
#            if i[0]+1 == pos[0]:
#                c=+1
#            if i[0]-1 == pos[0]:
#                c=+1
#            if i[1]+1 == pos[1]:
#                c=+1
#            if i[1]-1 == pos[1]:
#                c=+1
        
        return c

def findBoxes(listBoxes, state):
    x=0
    for i in state:
        y=0
        for j in i:
            if j=='$':
                listBoxes.append((x, y))
            y+=1
        x+=1
    return listBoxes

def findPlaces(listPlaces, state):
    x=0
    for i in state:
        y=0
        for j in i:
            if j=='.':
                listPlaces.append((x, y))
            y+=1
        x+=1
    return listPlaces


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

def distancePlayerToBox(xPlayer, yPlayer, xBox, yBox):
    return abs(xPlayer-xBox)+abs(yPlayer-yBox)+1
    
    
def distancePlacesToBoxes(xPlace, yPlace, xBox, yBox):
    return abs(xPlace-xBox)+abs(yPlace-yBox)+5
    
class Table():
    table=[]

goal = Table()
goal.table = obtenerMapa("workfile")
initial = copy.deepcopy(goal) #copia real
goal = findGoalState(goal.table) #encontrar el estado final
sokoban = SokobanProblem(initial, goal) 
print astar_search(sokoban).path
#depth_first_graph_search(sokoban)
#depth_limited_search(sokoban)
#iterative_deepening_search(sokoban)
