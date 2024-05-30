from typeguard import *

rank_value_dict = {'N': 0, 'T': 10, 'J': 2, 'Q': 3, 'K': 4, 'A': 11}


@typechecked
class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
        self.value = rank_value_dict[rank]

    def is_part_of_meld(self) -> bool:
        return self.rank in ['Q', 'K']

    def is_meld(self, card2: 'Card'):
        return self.is_part_of_meld() and card2.is_part_of_meld() and \
            self.rank != card2.rank and self.suit == card2.suit
