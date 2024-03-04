from tkinter import *
from tkinter import ttk

import time

from card_deck import *


class Bridge_Game: # maybe this will just be the playing portion of the game, separate class for bidding?
    def __init__(self, root: Tk, parent: ttk.Frame, hands, trumps = "", human="s", bot="random", order = ["s","w","n","e"],  practise=True):
        self.root = root
        self.parent = parent
        hands = map(sort_hand, hands)
        self.n, self.e, self.s, self.w = hands
        self.trumps = trumps
        self.draw_hands()
        self.human = human # which player is the human. Always south for now
        self.bot = bot # AI for playing bridge. This will control the other hands
        self.order = order # the order of play in the next trick. Will depend on who is declarer
        self.ns_tricks = 0
        self.ew_tricks = 0
        self.human_has_chosen_a_card = BooleanVar()
        self.human_has_chosen_a_card.set(False)
        self.practise = practise # TODO will reveal all the hands if true, does nothing for now

    def draw_hands(self):
        self.north_hand = ttk.Label(self.parent, text="n"+str(self.n))
        self.north_hand.grid(column=3,row=1,sticky=N)
        self.north_card_played = ttk.Label(self.parent, text="")
        self.north_card_played.grid(column=3,row=2,sticky=S)

        self.east_hand = ttk.Label(self.parent, text="e"+str(self.e))
        self.east_hand.grid(column=5,row=3,sticky=E)
        self.east_card_played = ttk.Label(self.parent, text="")
        self.east_card_played.grid(column=4,row=3,sticky=W)

        self.south_hand = ttk.Label(self.parent, text="s"+str(self.s))
        self.south_hand.grid(column=3,row=5,sticky=S)
        self.south_card_played = ttk.Label(self.parent, text="")
        self.south_card_played.grid(column=3,row=4,sticky=S)

        self.west_hand = ttk.Label(self.parent, text="w"+str(self.w))
        self.west_hand.grid(column=1,row=3,sticky=W)
        self.west_card_played = ttk.Label(self.parent, text="")
        self.west_card_played.grid(column=2,row=3,sticky=E)

        self.human_card_played = ttk.Entry(self.parent, width = 7)
        self.human_card_played.grid(column=3,row=6,sticky=N)
        self.human_card_button = ttk.Button(self.parent, text="play card", command=self.get_human_card)
        self.human_card_button.grid(column=4,row=6,sticky=N)

        self.next_trick_button = ttk.Button(self.parent, text="next trick", command=self.play_trick)
        self.next_trick_button.grid(column=5,row=6)
        #self.root.bind("<Return>", self.play_trick)

        #self.
        #self.play_card = ttk.Button(self.parent, width=7, text="play card", command=)

    def get_human_card(self):
        self.human_has_chosen_a_card.set(True)

    def clear_played_cards(self):
        self.north_card_played.config(text="")
        self.east_card_played.config(text="")
        self.south_card_played.config(text="")
        self.west_card_played.config(text="")
        self.human_card_played.delete(0, 'end')

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
        
    def valid_cards(self, player, suit):
        cards = []
        for c in self[player]:
            if c.suit == suit:
                cards.append(c)
        if len(cards) == 0:
            return self[player]
        return cards

    def play_card(self, player: str, lead_suit = "") -> Card:
        # the human player will be south for now
        # lead_suit being empty indicates that this player has the lead
        print(player)
        print(self[player])
        if lead_suit:
            playable_cards = self.valid_cards(player, lead_suit)
        if not lead_suit:
            playable_cards = self[player]
        
        if player == self.human:
            print("Waiting?")
            self.root.wait_variable(self.human_has_chosen_a_card)
            print("finished waiting")
            c = self.human_card_played.get()
            print(c)
            suit = c[-1]
            if c[:-1] in {"J","Q","K","A"}:
                val =  {"J":11,"Q":12,"K":13,"A":14}[c[:-1]]
            else:
                val = int(c[:-1])
            c = Card(val, suit)
            if c in playable_cards:
                self[self.human].remove(c)
                self.south_hand.config(text=str(self.s))
                self[player + " card_played"].config(text=str(c))
                self.root.update_idletasks()
            else:
                print(f"{c} not in hand or not following suit")
                return self.play_card(self.human, lead_suit = lead_suit)
        else:
            c = random.choice(playable_cards)
            self[player + " card_played"].config(text=str(c))
            self[player].remove(c)
            self[player+" hand"].config(text=str(self[player]))
            self.root.update_idletasks()
        print(self[player])
        print()
        return c

    def order_of_play(self, lead):
        if lead == "s":
            return ["s","w","n","e"]
        if lead == "w":
            return ["w","n","e","s"]
        if lead == "n":
            return ["n","e","s","w"]
        if lead == "e":
            return ["e","s","w","n"]

    # def get_human_card(self, lead_suit = ""):
    #     while self.card_played.get() == "":
    #         time.sleep(1)

        c = self.card_played.get()
        print(c)
        suit = c[-1]
        if c[:-1] in {"J","Q","K","A"}:
            val =  {"J":11,"Q":12,"K":13,"A":14}[c[:-1]]
        else:
            val = int(c[:-1])
        c = Card(val, suit)
        if c in playable_cards:
            self[self.human].remove(c)
            self.south_hand.config(text=str(self.s))
            self[player + " card_played"].config(text=str(c))
            self.root.update_idletasks()
        else:
            raise Exception(f"{c} not in hand or not following suit")
        
    def play_trick(self):
        self.human_has_chosen_a_card.set(False)
        trick = []
        c = self.play_card(self.order[0])
        trick.append(c)
        suit = c.suit
        print("lead suit = ", suit)
        for player in self.order[1:]:
            time.sleep(1.5)
            trick.append(self.play_card(player, lead_suit = suit)) # note this calls the method, drawing the card to the table and also append the card played to the trick list
        time.sleep(1.5)
        # if self.order[0] == self.human:
        #     c = self.play_card(self.human)
        #     trick.append(c)
        #     suit = c.suit
        #     print("lead suit = ", suit)
        #     for player in self.order[1:]:
        #         time.sleep(1.5)
        #         trick.append(self.play_card(player, lead_suit = suit)) # note this calls the method, drawing the card to the table and also append the card played to the trick list
        # else:
        #     for player in self.order:
        #         if player == self.human:
        #             while 
        #         time.sleep(1.5)
        #         trick.append(self.play_card(player, lead_suit = suit)) # note this calls the method, drawing the card to the table and also append the card played to the trick list



        # now the players have played their cards, so we find out who won the trick:
        highest_trump = None
        highest_of_lead_suit = c
        winner = 0 # then order[winner] will be the winner of the trick
        for i, card in enumerate(trick): 
            if card.suit == self.trumps:
                if highest_trump == None or card.val > highest_trump.val:
                    highest_trump = card
                    winner = i
            if highest_trump == None:
                if card.suit == c.suit:
                    if card.val > highest_of_lead_suit.val:
                        highest_of_lead_suit = card
                        winner = i
        winning_player = self.order[winner]
        self.order = self.order_of_play(winning_player)
        if winning_player in ["n","s"]:
            self.ns_tricks += 1
        else:
            self.ew_tricks += 1
        time.sleep(3)
        self.clear_played_cards()
        print(trick)
        print(f"NS have {self.ns_tricks} tricks")
        print(f"EW have {self.ew_tricks} tricks")

    def game(self):
        for _ in range(13):
            self.play_trick()
        


# class Bot:
#     def __init__(self):
#         pass

#     def play_card(self, hand):
#         return random.choice(hand)

