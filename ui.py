from easygui import ccbox
from easygui import codebox
import Tkinter as tkinter
import tkMessageBox as messagebox
import sys
from sokoban import main
from ai import Problem
from ai import astar_search
from ai import iterative_deepening_search
from ai import depth_first_tree_search
from ai import depth_first_graph_search
from ai import breadth_first_tree_search
from ai import breadth_first_graph_search
from ai import depth_limited_search
from utils import infinity
import sys
from tpIAsokobanparser import obtenerMapa
import copy
printTableFather=False
import time
from sokoban import generateGoalState
from sokoban import SokobanProblem
from sokoban import printTable
MONOSPACE_FONT_SIZE     =  10


table1 = [[' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '\n'], 
                [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', '\n'],
                [' ', ' ', ' ', ' ', '#', '$', ' ', ' ', '#', '\n'], 
                [' ', ' ', '#', '#', '#', ' ', ' ', '$', '#', '#', '#', '\n'], 
                [' ', ' ', '#', ' ', ' ', '$', ' ', ' ', '$', ' ', '#', '\n'], 
                ['#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', '\n'],
                ['#', ' ', ' ', ' ', '#', ' ', '#', '#', '#', ' ', '#', '#', ' ', ' ', '.', '.', '#', '\n'], 
                ['#', ' ', '$', ' ', ' ', '$', ' ', ' ', ' ', ' ', ' ', ' ', '@', ' ', '.', '.', '#', '\n'],
                ['#', '#', '#', '#', '#', ' ', '#', '#', '#', '#', ' ', '#', ' ', ' ', '.', '.', '#', '\n'], 
                [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '\n'],
                [' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', '\n']]

table2 = [[' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '\n'], 
                [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', '\n'],
                [' ', ' ', ' ', ' ', '#', '$', ' ', ' ', '#', '\n'], 
                [' ', ' ', '#', '#', '#', ' ', ' ', '$', '#', '#', '#', '\n'], 
                [' ', ' ', '#', ' ', ' ', '$', ' ', ' ', '$', ' ', '#', '\n'], 
                ['#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', '\n'],
                ['#', ' ', ' ', ' ', '#', ' ', '#', '#', '#', ' ', '#', '#', '@', ' ', '.', '.', '#', '\n'], 
                ['#', ' ', '$', ' ', ' ', '$', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '.', '.', '#', '\n'],
                ['#', '#', '#', '#', '#', ' ', '#', '#', '#', '#', ' ', '#', ' ', ' ', '.', '.', '#', '\n'], 
                [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '\n'],
                [' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', '\n']]


class tables():
    tabs= []
    cont=0
    excTime=""
    

def tableToStr(tableS):
    tableR=[]
    for i in tableS:
        tableR.append("".join(i))
        tableR.append("\n")
    return tableR



    

def callmove(i):
    def wrap():
        move(i)
    return wrap


def printText(text, eTime , textArea):
    try:
        text = "".join(text)  # convert a list or a tuple to a string
    except:
        sys.exit(16)
    textArea.configure(state=tkinter.NORMAL) 
    textArea.delete(1.0, tkinter.END)
    textArea.insert(tkinter.END,"SOKOBAN\n\n", "normal")    
    textArea.insert(tkinter.END,text, "normal")
    textArea.insert(tkinter.END,eTime, "normal")
    textArea.configure(state=tkinter.DISABLED)


def changeTable(textA, tables):
    tables.cont=tables.cont+1 
    if tables.cont >= len(tables.tabs):
        messagebox.showinfo("END", "BINGO!")
        tables.cont=0
    else:   
        text = tableToStr(tables.tabs[tables.cont])
        printText(text, tables.excTime ,  textA)
    return

def table(textA,  table):
    def wrap():
        changeTable( textA, table)
    return wrap
    
TOP = "top"
YES = True
BOTH = "both"
BOTTOM = "bottom"
NO = False
X = "x"
root = tkinter.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root_width    = int((screen_width * 0.8))
btnframe = tkinter.Frame(root)
btnframe.pack(side=TOP, expand=YES, fill=BOTH)

character_width = int((root_width * 0.6) / MONOSPACE_FONT_SIZE)
textArea = tkinter.Text(root,height=25,width=character_width, padx="1m", pady="1m")
textArea.pack(side=tkinter.LEFT, fill=BOTH, expand=YES)

newbtn = tkinter.Button(root, command=table(textArea, tables), text="NEXT STEP")
newbtn.pack(side=BOTTOM, expand=NO, fill=X)






def main():
    if len(sys.argv)==2 or len(sys.argv)==3:

        if sys.argv[1]=="-v":
            printTableFather = True
            initial = obtenerMapa(sys.argv[2])
        else:
            initial = obtenerMapa(sys.argv[1])
            
        goal = generateGoalState(initial) #encontrar el estado final
        sokoban = SokobanProblem(initial, goal) 
        
        x1= time.strftime('%S')
        
        pathS = astar_search(sokoban).path()
        
        x2= time.strftime('%S')
        timediff = int(x2) - int(x1)
        
        #Genera la secuencia de estados
        path = [node.state for node in pathS]
        states = []
        
        for state in path:
            states.append(state)
        
        i = len(states) - 1
        while i >= 0:
            printTable(states[i].matrix, "")
            tables.tabs.append(states[i].matrix)
            print
            i -= 1
        tables.excTime= 'Tiempo:', timediff,'segundos'
        print 'Tiempo:', timediff,'segundos'
        
    else:
        if len(sys.argv)<2:
            print "Debe recibir el nombre del archivo..."
        if len(sys.argv)>3:
            print "Demasiados arguementos..."
    
    text = tableToStr(tables.tabs[0])
    tables.cont=+1
    printText(text,tables.excTime, textArea)
    root.mainloop()

if __name__ == "__main__":
    main()
