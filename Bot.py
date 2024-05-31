from typeguard import *
from Card import Card
from CardsManipulator import CardsManipulator
from Player import Player
@typechecked
class Bot(Player):
    def __init__(self):
        super().__init__()

    def redraw(self) -> bool:
        if not self.correct_hand():
            return True

    def decide_to_play_or_pass(self, points: int) -> bool:
        cards_in_meld_suite = self.cards_in_meld_suite()
        probabilities = self.cards_manipulator.get_dict_of_probabilities(self.hand)
        if cards_in_meld_suite == 2 and probabilities[f">={points}"] > 45:
            return True
        if cards_in_meld_suite == 3 and probabilities[f">={points}"] > 40:
            return True
        if cards_in_meld_suite >= 4 and probabilities[f">={points}"] > 35:
            return True
        return probabilities[f">={points}"] > 50



