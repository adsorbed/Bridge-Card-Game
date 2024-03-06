from tkinter import *
from tkinter import ttk

import time

from card_deck import *

class Bridge_Bidding:
    def __init__(self, root: Tk, parent: ttk.Frame, hands, dealer = "s", human="s", bot="random",   practise=True) -> None:
        self.root = root
        self.parent = parent
        hands = map(sort_hand, hands)
        self.n, self.e, self.s, self.w = hands
        self.draw_hands()
        self.all_bids = self.generate_all_bids()
        self.available_bids = self.all_bids # they start off equal, the available bids will shrink as the bidding goes higher
        self.dealer = dealer
        self.bidding_order = self.find_order_of_bidding()
        self.bidding_column, self.bidding_row = 2, 7 # these are the position of the top left corner of the bidding area
        self.draw_bid_history()
        self.human = human # which player is the human. Always south for now
        self.human_has_chosen_a_bid = BooleanVar()
        self.human_has_chosen_a_bid.set(False)
        self.bot = bot # AI for playing bridge. This will control the other hands
        self.practise = practise # TODO will reveal all the hands if true, does nothing for now

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

        self.human_bid = ttk.Entry(self.parent, width = 7)
        self.human_bid.grid(column=3,row=6,sticky=N)
        self.human_bid_button = ttk.Button(self.parent, text="Make Bid", command=self.get_human_bid)
        self.human_bid_button.grid(column=4,row=6,sticky=N)

    def generate_all_bids(self):
        self.suits = ["C","D","H","S","NT"]
        self.values = [1,2,3,4,5,6,7]
        bids = []
        for v in self.values:
            for s in self.suits:
                bids.append(str(v)+s)
        bids.extend(["pass"]) # TODO add double and redouble, then change the perform_auction function to correctly handle logic for these
        print(bids)
        return bids
            
    def draw_bid_history(self):
        c, r =  self.bidding_column, self.bidding_row 
        
        s, w, n, e = [self.bidding_order[player] for player in ["s","w","n","e"]] # this allows me to draw the players in order of bidding
        self.north_bids = ttk.Label(self.parent, text="N")
        self.north_bids.grid(column=c+n,row=r)
        self.east_bids = ttk.Label(self.parent, text="E")
        self.east_bids.grid(column=c+e,row=r)
        self.south_bids = ttk.Label(self.parent, text="S")
        self.south_bids.grid(column=c+s,row=r)
        self.west_bids = ttk.Label(self.parent, text="W")
        self.west_bids.grid(column=c+w,row=r)

    def find_order_of_bidding(self):
        if self.dealer == "s":
            return {"s":0,"w":1,"n":2,"e":3}
        if self.dealer == "w":
            return {"w":0,"n":1,"e":2,"s":3}
        if self.dealer == "n":
            return {"n":0,"e":1,"s":2,"w":3}
        if self.dealer == "e":
            return {"e":0,"s":1,"w":2,"n":3}
        
    def get_human_bid(self):
        self.human_has_chosen_a_bid.set(True)

    def make_bid(self, player):
        if player == self.human:
            print("Waiting for human bid input")
            self.root.wait_variable(self.human_has_chosen_a_bid)
            print("finished waiting")
            b = self.human_bid.get()
            if b in self.available_bids:
                return b
            else: # TODO make human try again if they input an invalid bid
                print(f"{b} not in a valid bid")
                return
        else:
            b = random.choice(self.available_bids)
            return b


    def perform_auction(self):
        passed_out = False
        self.bid_history = []
        bidding_round = 0 # used to draw the new bids to the correct row
        while not passed_out:
            for player in self.bidding_order:
                # First, check if we the last 3 bids were passes:
                if len(self.bid_history) > 3 and self.bid_history[-3:] == ["pass","pass","pass"]:
                    passed_out = True
                    break
                # Get the player's bid
                bid = self.make_bid(player)
                self.bid_history.append(bid)
                if bid != "pass":
                    highest_bidder = player
                    bid_height = self.all_bids.index(bid) # all future bids must be higher than this bid
                    self.available_bids = self.all_bids[bid_height+1:]
                c, r = self.bidding_column+self.bidding_order[player], self.bidding_row+1+bidding_round # where to draw new bid
                ttk.Label(self.parent, text=bid).grid(column=c,row=r)
                self.root.update_idletasks()
            bidding_round += 1
        final_bid = self.bidding_history[-4]
        tricks_to_be_made = int(final_bid[0]) + 6
        
        trumps = final_bid[1:]
        
        return (tricks_to_be_made, trumps, highest_bidder)

        

