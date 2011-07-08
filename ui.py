from easygui import ccbox
from easygui import codebox
import Tkinter as tkinter
import tkMessageBox
import sys
MONOSPACE_FONT_SIZE     =  10
tableCounter = 0

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

def table():
    
    tableCounter=tableCounter+1
    return
    

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
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root_width    = int((screen_width * 0.8))
btnframe = tkinter.Frame(root)
btnframe.pack(side=TOP, expand=YES, fill=BOTH)
newbtn = tkinter.Button(root, command=table, text="NEXT STEP")
newbtn.pack(side=BOTTOM, expand=NO, fill=X)
character_width = int((root_width * 0.6) / MONOSPACE_FONT_SIZE)
textArea = tkinter.Text(root,height=25,width=character_width, padx="1m", pady="1m")
textArea.pack(side=tkinter.LEFT, fill=BOTH, expand=YES)
text = tableToStr(table1)
try:
    text = "".join(text)  # convert a list or a tuple to a string
except:
    sys.exit(16)
textArea.insert(tkinter.END,"SOKOBAN\n\n", "normal")    
textArea.insert(tkinter.END,text, "normal")
textArea.configure(state=tkinter.DISABLED)


root.mainloop()

