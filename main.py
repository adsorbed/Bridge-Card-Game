from card_deck import *

def main():
    d = Deck()
    print(d)
    x = d.deal()
    print(x[2])
    d.shuffle()
    x = d.deal()
    print(x[2])

main()
