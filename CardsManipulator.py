from typeguard import *
from Card import Card

@typechecked
class CardsManipulator:
    def __init__(self):
        pass
    def full_deck(self) -> list['Card']:
        res = []
        for rank in ["N", "T", "J", "Q", "K", "A"]:
            for suit in ["H", "D", "C", "S"]:
                res.append(Card(rank, suit))
        return res

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
