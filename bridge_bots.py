from card_deck import *
import random
#from Bridge_full import Bridge

class bridge_bot:
    def __init__(self, bridge_game, hand: list, position: str, bidding_allowed=False):
        self.game = bridge_game
        self.hand = hand # after initialization, self.hand here and e.g. self.n will point to the same list
        self.position = position # i.e. "n" or "e"
        self.bidding_allowed = bidding_allowed # TODO purpose of this?????
        self.declarer = False

    def valid_cards(self, suit):
        cards = []
        for c in self.hand:
            if c.suit == suit:
                cards.append(c)
        if len(cards) == 0:
            return self.hand
        return cards

    def bot_make_bid(self, available_bids, bidding_history=[]):
        raise Exception("not implemented")

    def bot_play_card(self, lead_suit = ""):
        if lead_suit:
            playable_cards = self.valid_cards(lead_suit)
        if not lead_suit:
            playable_cards = self.hand
        
    def choose_dummy_card(self, dummy_hand, suit):
        raise Exception("not implemented")

class random_bot(bridge_bot):
    def __init__(self, bridge_game, hand: list, position: str, bidding_allowed=False):
        super().__init__(bridge_game, hand, position, bidding_allowed=False) # random_bot doesn't care about its position relative to declarer etc so just use ""

    def bot_make_bid(self, available_bids, bidding_history=[]):
        # Testing when the human is dummy:
        # if self.position in ["w", "e"]:
        #     return "PASS"
        # if self.position == "n":
        #     return "7NT"
        b = random.choice(available_bids)
        return b

    def bot_play_card(self, lead_suit = ""):
        if lead_suit:
            playable_cards = self.valid_cards(lead_suit)
        if not lead_suit:
            playable_cards = self.hand
        print(playable_cards)
        c = random.choice(playable_cards)
        print(c)
        return c

    def choose_dummy_card(self, dummy_position, lead_suit = ""):
        print(self.position)
        playable_cards = self.game.valid_cards(dummy_position, lead_suit)
        c = random.choice(playable_cards)
        return c