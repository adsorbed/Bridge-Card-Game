from tkinter import *
from tkinter import ttk

import time

from card_deck import *


class Bridge_Game: # maybe this will just be the playing portion  of the game, separate class for bidding?
    def __init__(self, root: Tk, parent: ttk.Frame, hands, human="s", bot="random", practise=True):
        self.root = root
        self.parent = parent
        hands = map(sort_hand, hands)
        self.n, self.e, self.s, self.w = hands
        self.draw_hands()
        self.human = human # which player is the human. Always south for now
        self.bot = bot # AI for playing bridge. This will control the other hands
        self.practise = practise # TODO will reveal all the hands if true, does nothing for now

    def draw_hands(self):
        self.north_hand = ttk.Label(self.parent, text="n"+str(self.n))
        self.north_hand.grid(column=3,row=1,sticky=N)
        self.north_card_played = ttk.Label(self.parent, text="")
        self.north_card_played.grid(column=3,row=2,sticky=N)

        self.east_hand = ttk.Label(self.parent, text="e"+str(self.e))
        self.east_hand.grid(column=5,row=3,sticky=E)
        self.east_card_played = ttk.Label(self.parent, text="")
        self.east_card_played.grid(column=4,row=3,sticky=E)

        self.south_hand = ttk.Label(self.parent, text="s"+str(self.s))
        self.south_hand.grid(column=3,row=5,sticky=S)
        self.south_card_played = ttk.Label(self.parent, text="")
        self.south_card_played.grid(column=3,row=4,sticky=S)

        self.west_hand = ttk.Label(self.parent, text="w"+str(self.w))
        self.west_hand.grid(column=1,row=3,sticky=W)
        self.west_card_played = ttk.Label(self.parent, text="")
        self.west_card_played.grid(column=2,row=3,sticky=W)

        self.card_played = ttk.Entry(self.parent, width = 7)
        self.card_played.grid(column=3,row=6,sticky=S)

    def __getitem__(self, h):
        if h=="n":
            return self.n
        if h=="e":
            return self.e
        if h=="s":
            return self.s
        if h=="w":
            return self.w
        if h=="n hand":
            return self.north_hand
        if h=="e hand":
            return self.east_hand
        if h=="s hand":
            return self.south_hand
        if h=="w hand":
            return self.west_hand
        if h=="n card_played":
            return self.north_card_played
        if h=="e card_played":
            return self.east_card_played
        if h=="s card_played":
            return self.south_card_played
        if h=="w card_played":
            return self.west_card_played

    def play_card(self, player: str):
        # the human player will be south for now
        assert player in {"n","e","s","w"}
        print(player)
        print(self[player])
        
        if player == self.human:
            c = self.card_played.get()
            suit = c[-1]
            if c[0] in ["A","K","Q","J"]: 
                val = c[0]
            elif len(c) == 3:
                val = 10
            else: 
                val = int(c[0])
            c = Card(val, suit)
            if c in self[self.human]:
                self[self.human].remove(c)
                self.south_hand.config(text=str(self.s))
                self[player + " card_played"].config(text=str(c))
                self.root.update_idletasks()
                return
            else:
                raise Exception(f"{c} not in hand")
        else:
            c = random.choice(self[player])
            print(player + " card_played")
            self[player + " card_played"].config(text=str(c))
            self[player].remove(c)
            self[player+" hand"].config(text=str(self[player]))
            self.root.update_idletasks()
        print(self[player])
        print()
        return

    def order(self, lead):
        if lead == "s":
            return ["s","w","n","e"]
        if lead == "w":
            return ["w","n","e","s"]
        if lead == "n":
            return ["n","e","s","w"]
        if lead == "e":
            return ["e","s","w","n"]
        
    def play_trick(self, ord=["s","w","n","e"]):
        for player in ord:
            self.play_card(player)
            time.sleep(0.5)

        


# class Bot:
#     def __init__(self):
#         pass

#     def play_card(self, hand):
#         return random.choice(hand)

