from typeguard import *

rank_value_dict = {'N': 0, 'T': 10, 'J': 2, 'Q': 3, 'K': 4, 'A': 11}


@typechecked
class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
        self.value = rank_value_dict[rank]

    def __eq__(self, other: 'Card') -> bool:
        return self.rank == other.rank and self.suit == other.suit

    def is_part_of_meld(self) -> bool:
        return self.rank in ['Q', 'K']

    def is_meld(self, other: 'Card'):
        return self.is_part_of_meld() and other.is_part_of_meld() and \
            self.rank != other.rank and self.suit == other.suit
