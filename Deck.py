from typeguard import *
from Card import Card
from random import shuffle

@typechecked
class Deck:
    def __init__(self):
        self.cards: list['Card'] = self.full_deck()

    def full_deck(self) -> list['Card']:
        res = []
        for rank in ["N", "T", "J", "Q", "K", "A"]:
            for suit in ["H", "D", "C", "S"]:
                res.append(Card(rank, suit))
        return res

    def _shuffle(self):
        shuffle(self.cards)

    def split_three_seven_seven_seven(self) -> tuple[list['Card'], list['Card'], list['Card'], list['Card']]:
        self._shuffle()
        return self.cards[:3], self.cards[3:10], self.cards[10:17], self.cards[17:]



deck = Deck()
hand1, hand2, hand3, hand4 = deck.split_three_seven_seven_seven()
print([str(card) for card in hand1])
print([str(card) for card in hand2])
print([str(card) for card in hand3])
print([str(card) for card in hand4])




