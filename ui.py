from easygui import ccbox
import Tkinter as tkinter
import tkMessageBox

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
"""
for i in range(0, 26):
    buttons = [tkinter.Button(btnframe, text=i, width=10, height=5) for i in range(27)]
for i, button in enumerate(buttons):
    button["command"] = callmove(i)
    button.grid(row=i//3, column=i%3, sticky="N"+"E"+"W"+"S")
 

if 1: # TODO: add switch for this
    m = 0
    buttons[m]["state"] = "disabled"
    buttons[m]["text"] = "O"
    board[m] = -1

"""

root.mainloop()
