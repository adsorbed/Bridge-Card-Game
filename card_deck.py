import random

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

    def __str__(self) -> str:
        return str(self.val) + str(self.suit)
    
    def __repr__(self) -> str:
        return str(self.val) + str(self.suit)

class Deck:
    def __init__(self):
        self.suits = ["S","H","D","C"]
        self.values = ["A","K","Q","J",10,9,8,7,6,5,4,3,2]
        self.cards = []
        for s in self.suits:
            for v in self.values:
                self.cards.append(Card(s, v))
        
    def __repr__(self) -> str:
        return str([str(card) for card in self.cards])
    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return (self.cards[:13], self.cards[13:26], self.cards[26:39], self.cards[39:52])

