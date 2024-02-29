import random

class Card:
    def __init__(self, val, suit):
        self.suit = suit
        self.val = val

    def __str__(self) -> str:
        return str(self.val) + str(self.suit)
    
    def __repr__(self) -> str:
        return str(self.val) + str(self.suit)
    
    def __eq__(self, other) -> bool:
        return (self.suit == other.suit) and (self.val == other.val)

class Deck:
    def __init__(self):
        self.suits = ["S","H","D","C"]
        self.values = ["A","K","Q","J",10,9,8,7,6,5,4,3,2]
        self.cards = []
        for s in self.suits:
            for v in self.values:
                self.cards.append(Card(v, s))
        
    def __repr__(self) -> str:
        return str([str(card) for card in self.cards])
    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return (self.cards[:13], self.cards[13:26], self.cards[26:39], self.cards[39:52])

def sort_hand(hand):
    # sorts the cards in a hand in descending order by suit and value. sorted is stable, so we can sot by value and then suit to correctly sort the hand
    def number_sort(card):
        value_picture_cards = {"A":14,"K":13,"Q":12,"J":11}
        return value_picture_cards.get(card.val, card.val)
    
    temp = sorted(hand, key=number_sort, reverse=True)

    def suit_sort(card):
        value_suits = {"S":4,"H":3,"D":2,"C":1}
        return value_suits[card.suit]
    
    return sorted(temp, key=suit_sort, reverse=True)
    



