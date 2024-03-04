from card_deck import *
from bridge import *

# d = Deck()
# hands = d.deal()
# b = Bridge_Game(hands)
# print(b.s)
# b.play_card("s", "AD")
# print(b.s)
# b.play_card("s", "2D")
# print(b.s)


class test_class:
    def __init__(self,val) -> None:
        self.val = val

    def __getitem__(self, v):
        if v == "val":
            return self.val

c = test_class(5)
print(c["val"])
print(c["asd"])

print(max(6,None))