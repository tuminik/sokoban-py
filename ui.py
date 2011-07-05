from easygui import ccbox
from easygui import codebox
import Tkinter as tkinter
import tkMessageBox

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



def tableToStr(tableS):
    tableR=[]
    for i in tableS:
        tableR.append("".join(i))
    return tableR

def table(box):
    box(msg = "Tabla Prueba", title="Tabla", text=tableToStr(table2))
    #ccbox(msg="Shall I continue?", title=" ", choices=("Continue", "Cancel"), image=None)
    
    

def callmove(i):
    def wrap():
        move(i)
    return wrap

TOP = "top"
YES = True
BOTH = "both"
BOTTOM = "bottom"
NO = False
X = "x"
root = tkinter.Tk()
btnframe = tkinter.Frame(root)
btnframe.pack(side=TOP, expand=YES, fill=BOTH)
newbtn = tkinter.Button(root, command=table, text="NEW GAME")
newbtn.pack(side=BOTTOM, expand=NO, fill=X)
box = codebox(msg = "Tabla Prueba", title="Tabla", text=tableToStr(table1))
box.confiure(state=NORMAL)


"""
for i in tablePrueba:
    buttons = [tkinter.Button(btnframe, text=i, width=40, height=3) for i in tablePrueba]
for i, button in enumerate(buttons):
    button["command"] = callmove(i)
    button.grid(row=i//1, column=i%1, sticky="")


if 1: # TODO: add switch for this
    m = 0
    buttons[m]["state"] = "disabled"
    buttons[m]["text"] = "O"
    board[m] = -1
"""

root.mainloop()
print table
