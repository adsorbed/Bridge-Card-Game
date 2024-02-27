from tkinter import *
from tkinter import ttk

from card_deck import *


d = Deck()
d.shuffle()
n, e, s, w = d.deal()

root = Tk()
root.title("Bridge")
mainframe = ttk.Frame(root, padding="20")
mainframe.grid(column=0, row=0, sticky=(N,E,S,W))

#ttk.Label(mainframe, text="          sdfdfsdfsdf               ").grid(column=2,row=2)
ttk.Label(mainframe, text="n"+str(n)).grid(column=2,row=1)
ttk.Label(mainframe, text="e"+str(e)).grid(column=3,row=2)
ttk.Label(mainframe, text="s"+str(s)).grid(column=2,row=3)
ttk.Label(mainframe, text="w"+str(w)).grid(column=1,row=2)


root.mainloop()