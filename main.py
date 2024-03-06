from tkinter import *
from tkinter import ttk

import time

from card_deck import *
from bridge_card_part import *
from bridge_bidding import *

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

main_bidding()

