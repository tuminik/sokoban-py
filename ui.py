from easygui import ccbox
import Tkinter as tkinter
import tkMessageBox



tablePrueba = [[' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n'], 
[' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ')', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n'], 
[' ', ' ', ' ', ' ', '#', '$', ' ', ' ', '$', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '\n'], 
[' ', ' ', '#', '#', '#', ' ', ' ', '$', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', '\n'], 
[' ', ' ', '$', ' ', ' ', '$', ' ', ' ', '$', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '\n'], 
['#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', '\n'],
['#', ' ', '$', ' ', ' ', '$', ' ', ' ', ' ', ' ', ' ', ' ', '@', ' ', '.', '.', '#', '\n'], 
['#', '#', '#', '#', '#', ' ', '#', '#', '#', '#', ' ', '#', ' ', ' ', '.', '.', '#', '\n'], 
[' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '\n'], 
[' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', '\n']]





def table():
    ccbox(msg="Shall I continue?", title=" ", choices=("Continue", "Cancel"), image=None)
    

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

for i in tablePrueba:
    for j in i:
        buttons = [tkinter.Button(btnframe, text=j, width=5, height=3) for i in tablePrueba for j in i]
for i, button in enumerate(buttons):
    button["command"] = callmove(i)
    button.grid(row=i//17, column=i%17, sticky="")
"""

if 1: # TODO: add switch for this
    m = 0
    buttons[m]["state"] = "disabled"
    buttons[m]["text"] = "O"
    board[m] = -1

"""

root.mainloop()
print table
