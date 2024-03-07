from card_deck import *
import random
from Bridge_full import Bridge

class random_bot:
    def __init__(self, bridge_game: Bridge, hand: list, position: str, bidding_allowed=False):
        self.game = bridge_game
        self.hand = hand # after initialization, self.hand here and e.g. self.n will point to the same list
        self.position = position # i.e. "n" or "e"
        self.bidding_allowed = bidding_allowed
        self.declarer = False

    def bot_make_bid(self, available_bids, bidding_history=[]):
        b = random.choice(available_bids)
        return b

    def valid_cards(self, suit):
        cards = []
        for c in self.hand:
            if c.suit == suit:
                cards.append(c)
        if len(cards) == 0:
            return self.hand
        return cards

    def bot_play_card(self, lead_suit = ""):
        if lead_suit:
            playable_cards = self.valid_cards(lead_suit)
        if not lead_suit:
            playable_cards = self.hand
        c = random.choice(playable_cards)
        return c

    def choose_dummy_card(self, dummy_hand, suit):
        playable_cards = self.game.valid_cards(self.game.dummy, suit)
        c = random.choice(playable_cards)
        return c