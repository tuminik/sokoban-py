from easygui import ccbox
from easygui import codebox
import Tkinter as tkinter
import tkMessageBox as messagebox
import sys
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
    tabs= [table1,table2]
    cont=0
    

def tableToStr(tableS):
    tableR=[]
    for i in tableS:
        tableR.append("".join(i))
    return tableR



    

def callmove(i):
    def wrap():
        move(i)
    return wrap


def printText(text,textArea):
    try:
        text = "".join(text)  # convert a list or a tuple to a string
    except:
        sys.exit(16)
    textArea.configure(state=tkinter.NORMAL) 
    textArea.delete(1.0, tkinter.END)
    textArea.insert(tkinter.END,"SOKOBAN\n\n", "normal")    
    textArea.insert(tkinter.END,text, "normal")
    textArea.configure(state=tkinter.DISABLED)


def changeTable(textA, tables):
    tables.cont=+1 
    text = tableToStr(tables.tabs[tables.cont])
    printText(text,textA)
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

text = tableToStr(tables.tabs[0])
tables.cont=+1
printText(text,textArea)

root.mainloop()

