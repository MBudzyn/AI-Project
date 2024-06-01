from typeguard import *
from Card import Card
from Player import Player
@typechecked
class Bot(Player):
    def __init__(self):
        super().__init__()
        self.guaranteed_winners = []
        self.melds = set()

    def decide_to_play_or_pass(self, points: int) -> bool:
        cards_in_meld_suite = self.cards_in_meld_suite()
        probabilities = self.cards_manipulator.get_dict_of_probabilities(self.hand)
        print(probabilities)
        if cards_in_meld_suite == 2 and probabilities[f">={points}"] > 45:
            return True
        if cards_in_meld_suite == 3 and probabilities[f">={points}"] > 40:
            return True
        if cards_in_meld_suite >= 4 and probabilities[f">={points}"] > 35:
            return True
        return probabilities[f">={points}"] > 50

    def begin_of_playing_round(self):
        self.guaranteed_winners = self.define_guaranteed_winners()
        self.melds = self.define_melds_on_hand()


    def define_guaranteed_winners(self) -> list['Card']: # dokladnie sprawdzic czy dziala bez bledow
        guaranteed_winners = self.cards_manipulator.guaranteed_winners(self.hand)
        res = []
        for card in self.hand:
            if guaranteed_winners[card.suit][card.quality] == 1:
                res.append(card)
        return res

    def define_melds_on_hand(self)-> set[str]:
        melds = set()
        res = [card for card in self.hand if self.is_melding(card)]
        if len(res) < 2:
            return set()
        for i in range(len(res) - 1):
            for j in range(i + 1, len(res)):
                if res[i].is_meld(res[j]):
                    melds.add(res[i].suit)
        return melds

    def discard_two_cards(self) -> list['Card']:

        to_discard = []
        sorted_hand = sorted(self.hand, key = lambda x: x.value)
        for card in sorted_hand:
            if card in self.guaranteed_winners or card.suit in self.melds:
                continue
            else:
                to_discard.append(card)
                self.hand.remove(card)
                if len(to_discard) == 2:
                    return to_discard

        self.hand = sorted_hand[2:]
        return sorted_hand[:2]

    def play_card(self, card1, card2, trump) -> 'Card':
        guaranteed_winners = self.define_guaranteed_winners()
        melds = self.define_melds_on_hand()
        if guaranteed_winners:
            self.hand.remove(guaranteed_winners[0])
            return guaranteed_winners[0]
        elif melds:
            for card in self.hand:
                if card.suit in melds and card.is_part_of_meld():
                    self.hand.remove(card)
                    return card
        else:
            return self.hand.pop()












