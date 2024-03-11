from tkinter import *
from tkinter import ttk

import time

from card_deck import *
from bridge_card_part import *
from bridge_bidding import *
from Bridge_full import *
from Bridge_with_canvas import *

d = Deck()
d.shuffle()
hands = d.deal()

def main_card():
    root = Tk()
    root.title("Bridge")
    mainframe = ttk.Frame(root, padding="20")
    mainframe.grid(column=0, row=0)
    b = Bridge_Game(root, mainframe, hands)
    b.game()
    root.mainloop()


def main_bidding():
    root = Tk()
    root.title("Bridge Bidding")
    mainframe = ttk.Frame(root, padding="20")
    mainframe.grid(column=0, row=0)
    b = Bridge_Bidding(root, mainframe, hands)
    b.perform_auction()
    root.mainloop()

def main_full():
    root = Tk()
    root.title("Bridge")
    mainframe = ttk.Frame(root, width = 500, height = 500)
    mainframe.pack_propagate(False)
    mainframe.grid(column=0, row=0)
    b = Bridge(root, mainframe, hands, practise=False, fast_mode=True)
    b.play()
    root.mainloop()

def main_full_canvas():

    b = Bridge_canvas(hands, practise=False, fast_mode=True)
    #b.play()
    b.root.mainloop()

#main_full()

main_full_canvas()