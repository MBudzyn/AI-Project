from typeguard import *
from Card import Card


@typechecked
class Player:
    def __init__(self):
        self.hand: list['Card'] = []
        self.played: list['Card'] = []
        self.trick_pile: list['Card'] = []
        self.other_players: list['Player'] = []

    def calculate_act_score(self) -> int:
        return sum([card.value for card in self.trick_pile])

    def have_eighteen(self) -> bool:
        return self.calculate_act_score() >= 18

    def have_meld(self) -> bool:
        tmp = [card for card in self.hand if card.is_part_of_meld()]
        if len(tmp) < 2:
            return False

        return any([tmp[i].is_meld(tmp[j]) for i in range(len(tmp) - 1) for j in range(i + 1, len(tmp))])

    def correct_hand(self) -> bool:
        return self.have_eighteen() and (not self.have_meld())
