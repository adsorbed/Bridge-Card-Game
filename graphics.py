from tkinter import *
from tkinter import ttk

import time

from card_deck import *
from bridge import *

# def play_trick(bridge_game):
#     c = card_played.get()
#     print(b.s)
#     bridge_game.play_card("s", c)
#     print(b.s)
#     south_hand.config(text="s"+str(b.s))

    #ttk.Label(mainframe, text="s"+str(b.s)).grid(column=2,row=3,sticky=S)


d = Deck()
d.shuffle()
hands = d.deal()


root = Tk()
root.title("Bridge")
mainframe = ttk.Frame(root, padding="20")
mainframe.grid(column=0, row=0)
b = Bridge_Game(root, mainframe, hands)

#b.game()


# card_played = ttk.Entry(mainframe, width = 7)
# card_played.grid(column=3,row=6,sticky=S)



root.mainloop()



