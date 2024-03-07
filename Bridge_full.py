from tkinter import *
from tkinter import ttk
from time import sleep
from card_deck import *
from bridge_bots import random_bot
"""
Anatomy of the Bridge class:

* initialization using input hands and dealer
* helper methods for internals of Bridge Class
* Drawing methods for the bidding section of the game
* bidding system
* drawing methods for the card-playing part of the game
* card trick system
* handling the end of the game

These bullet points will be separated with a line of #s, i.e. 
##############################################################################
"""

class Bridge:
    def __init__(self, root: Tk, parent: ttk.Frame, hands, dealer = "s", human="s", bot=random_bot, practise=True) -> None:
        self.root = root
        self.parent = parent
        hands = map(sort_hand, hands)
        self.n, self.e, self.s, self.w = hands
        self.human = human # which player is the human. Always south for now
        self.bot = bot
        self.assign_bots()
        self.practise = practise # TODO will reveal all the hands if true, does nothing for now
        self.draw_hands()
        self.all_bids = self.generate_all_bids()
        self.available_bids = self.all_bids # they start off equal, the available bids will shrink as the bidding goes higher
        self.dealer = dealer
        self.bidding_order = self.find_order_of_bidding()
        self.bidding_column, self.bidding_row = 2, 7 # these are the position of the top left corner of the bidding area
        self.draw_bid_history()
        
        self.human_has_chosen = BooleanVar()
        self.human_has_chosen.set(False)
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_human_input)
        self.bot = bot # AI for playing bridge. This will control the other hands
        

##############################################################################

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
        if h=="n_bot":
            return self.n_bot
        if h=="e_bot":
            return self.e_bot
        if h=="s_bot":
            return self.s_bot
        if h=="w_bot":
            return self.w_bot
        
        
    def generate_all_bids(self):
        self.suits = ["C","D","H","S","NT"]
        self.values = [1,2,3,4,5,6,7]
        bids = []
        for v in self.values:
            for s in self.suits:
                bids.append(str(v)+s)
        bids.extend(["pass"]) # TODO add double and redouble, then change the perform_auction function to correctly handle logic for these
        return bids
    
    def find_order_of_bidding(self):
        if self.dealer == "s":
            return {"s":0,"w":1,"n":2,"e":3}
        if self.dealer == "w":
            return {"w":0,"n":1,"e":2,"s":3}
        if self.dealer == "n":
            return {"n":0,"e":1,"s":2,"w":3}
        if self.dealer == "e":
            return {"e":0,"s":1,"w":2,"n":3}
        
    def order_of_play(self, lead):
        if lead == "s":
            return ["s","w","n","e"]
        if lead == "w":
            return ["w","n","e","s"]
        if lead == "n":
            return ["n","e","s","w"]
        if lead == "e":
            return ["e","s","w","n"]
        
    def assign_bots(self):
        if self.human != "s":
            self.s_bot = self.bot(self.s, "s") # possibly issues about passing by reference
        if self.human != "w":
            self.w_bot = self.bot(self.w, "w")
        if self.human != "n":
            self.n_bot = self.bot(self.n, "n")
        if self.human != "e":
            self.e_bot = self.bot(self.e, "e")

        
##############################################################################
    
    def draw_hands(self):
        self.north_hand = ttk.Label(self.parent, text="n"+str(self.n))
        if self.practise == True or self.human == "n":
            self.north_hand.grid(column=3,row=1,sticky=N)
        self.north_card_played = ttk.Label(self.parent, text="")
        self.north_card_played.grid(column=3,row=2,sticky=S)

        self.east_hand = ttk.Label(self.parent, text="e"+str(self.e))
        if self.practise == True or self.human == "e":
            self.east_hand.grid(column=5,row=3,sticky=E)
        self.east_card_played = ttk.Label(self.parent, text="")
        self.east_card_played.grid(column=4,row=3,sticky=W)

        self.south_hand = ttk.Label(self.parent, text="s"+str(self.s))
        if self.practise == True or self.human == "s":
            self.south_hand.grid(column=3,row=5,sticky=S)
        self.south_card_played = ttk.Label(self.parent, text="")
        self.south_card_played.grid(column=3,row=4,sticky=S)

        self.west_hand = ttk.Label(self.parent, text="w"+str(self.w))
        if self.practise == True or self.human == "w":
            self.west_hand.grid(column=1,row=3,sticky=W)
        self.west_card_played = ttk.Label(self.parent, text="")
        self.west_card_played.grid(column=2,row=3,sticky=E)      

        self.human_input = ttk.Entry(self.parent, width = 7)
        self.human_input.grid(column=3,row=6,sticky=N)
        self.human_input_button = ttk.Button(self.parent, text="Make Bid", command=self.confirm_human_input)
        self.human_input_button.grid(column=4,row=6,sticky=N)

    def confirm_human_input(self):
        self.human_has_chosen.set(True)

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

    def draw_dummy_hand(self):
        if self.dummy == self.human or self.practise:
            return
        if self.dummy == "n":
            
            self.north_hand.grid(column=3,row=1,sticky=N)
            
        if self.dummy == "e":
            self.east_hand = ttk.Label(self.parent, text="e"+str(self.e))
            self.east_hand.grid(column=5,row=3,sticky=E)
            self.east_card_played = ttk.Label(self.parent, text="")
            self.east_card_played.grid(column=4,row=3,sticky=W)
        if self.dummy == "s":
            self.south_hand = ttk.Label(self.parent, text="s"+str(self.s))
            self.south_hand.grid(column=3,row=5,sticky=S)
            self.south_card_played = ttk.Label(self.parent, text="")
            self.south_card_played.grid(column=3,row=4,sticky=S)
        if self.dummy == "w":
            self.west_hand = ttk.Label(self.parent, text="w"+str(self.w))
            self.west_hand.grid(column=1,row=3,sticky=W)
            self.west_card_played = ttk.Label(self.parent, text="")
            self.west_card_played.grid(column=2,row=3,sticky=E) 

#######################################################################

    def make_bid(self, player):
        if player == self.human:
            print("Waiting for human bid input")
            self.root.wait_variable(self.human_has_chosen)
            print("finished waiting")
            b = self.human_input.get()
            b = b.upper()
            if b in self.available_bids:
                return b
            else: # TODO make human try again if they input an invalid bid
                print(f"{b} not in a valid bid")
                return
        else:
            #print(self.available_bids)
            b = self[player+"_bot"].bot_make_bid(self.available_bids, self.bid_history)
            return b

    def perform_auction(self):
        passed_out = False
        self.bid_history = []
        bidding_round = 0 # used to draw the new bids to the correct row
        while not passed_out:
            for player in self.bidding_order:
                sleep(1.5)
                # First, check if the last 3 bids were passes:
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

        final_bid = self.bid_history[-4]
        self.tricks_to_be_made = int(final_bid[0]) + 6
        self.trumps = final_bid[1:]
        self.declarer = highest_bidder
        self[player+"_bot"].declarer = True
        for player in self.bidding_order:
            if (self.bidding_order[player]+2)%4 == self.bidding_order[self.declarer]:
                self.dummy = player
            if (self.bidding_order[player]-1)%4 == self.bidding_order[self.declarer]:
                self.lead = player
        
        print("declarer, lead, dummy =", self.declarer, self.lead, self.dummy)
        #time.sleep(2)

#######################################################################
    
    def start_card_portion(self):
        self.draw_hands()
        self.order = self.order_of_play(self.lead) # the order of play in the next trick. Will depend on who is declarer
        self.ns_tricks = 0
        self.ew_tricks = 0
        self.human_has_chosen.set(False)
        self.redraw_after_bidding()

    def redraw_after_bidding(self):
        self.contract = ttk.Label(self.parent, text=f"Contract: {self.tricks_to_be_made-6}{self.trumps}")
        self.contract.grid(column=1,row=1,sticky=N)
        self.human_input_button.config(text="Play card")
        if self.practise:
            return
        # hide the bidding

    def clear_played_cards(self):
        self.north_card_played.config(text="")
        self.east_card_played.config(text="")
        self.south_card_played.config(text="")
        self.west_card_played.config(text="")
        self.human_input.delete(0, 'end')

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
            print("Waiting for human input")
            self.root.wait_variable(self.human_has_chosen)
            print("finished waiting")
            c = self.human_input.get()
            c = c.upper()
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
            c = self[player+"_bot"].bot_play_card(lead_suit = lead_suit)
            print(c)
            self[player].remove(c)
            if player == self.dummy or self.practise == True:
                self[player+" hand"].config(text=str(self[player]))
            self[player + " card_played"].config(text=str(c))
            
            
            self.root.update_idletasks()
        print(self[player])
        print()
        return c

    def play_trick(self, first_trick=False):
        self.human_has_chosen.set(False)
        trick = []
        sleep(1)
        c = self.play_card(self.order[0])
        trick.append(c)
        suit = c.suit
        print("lead suit = ", suit)
        if first_trick:
            self.draw_dummy_hand()
        for player in self.order[1:]:
            sleep(1.5)
            trick.append(self.play_card(player, lead_suit = suit)) # note this calls the method, drawing the card to the table and also append the card played to the trick list
        sleep(1.5)
        # now the players have played their cards, so we find out who won the trick:
        highest_trump = None
        highest_of_lead_suit = c
        winner = 0 # then order[winner] will be the winner of the trick
        for i, card in enumerate(trick): 
            if card.suit == self.trumps: # no card is of the suit "no trumps", so this code works for when the contract is no trumps.
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
        sleep(3)
        self.clear_played_cards()
        print(trick)
        print(f"NS have {self.ns_tricks} tricks")
        print(f"EW have {self.ew_tricks} tricks")

############################################################################################

    def play(self):
        self.perform_auction()
        self.start_card_portion()
        self.redraw_after_bidding()
        for i in range(13):
            print("--------------------------------------------------------------")
            print(f"Trick {i+1}")
            print("--------------------------------------------------------------")
            if i == 0:
                self.play_trick(first_trick=True)
            else:
                self.play_trick()
        end_game_popup = Toplevel(self.root)
        end_game_popup.title("End of Game")
        self.root.quit()
        