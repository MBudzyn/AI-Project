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

    def get_missing_cards(self, hand: list['Card']) -> list['Card']:
        return [card for card in self.full_deck() if card not in hand]

    def get_all_poss_talons(self, hand: list['Card']) -> list[list['Card']]:
        res = []
        cards = self.get_missing_cards(hand)
        for i in range(len(cards) - 2):
            for j in range(i + 1, len(cards) - 1):
                for k in range(j + 1, len(cards)):
                    res.append([cards[i].__copy__(), cards[j].__copy__(), cards[k].__copy__()])
        return res


deck = Deck()
hand1, hand2, hand3, hand4 = deck.split_three_seven_seven_seven()
print([str(card) for card in hand1])
print([str(card) for card in hand2])
print([str(card) for card in hand3])
print([str(card) for card in hand4])
print([str(card) for card in deck.get_missing_cards(hand2)])
print(len(deck.get_all_poss_talons(hand2)))




