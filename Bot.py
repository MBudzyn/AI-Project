import random

from typeguard import *
from Card import Card
from Player import Player
from GlobalVariables import *
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
        if cards_in_meld_suite == 2 and probabilities[f">={points + BOT_SKILL_POINTS}"] > 45:
            return True
        if cards_in_meld_suite == 3 and probabilities[f">={points + BOT_SKILL_POINTS}"] > 40:
            return True
        if cards_in_meld_suite >= 4 and probabilities[f">={points + BOT_SKILL_POINTS}"] > 35:
            return True
        return probabilities[f">={points}"] > 50

    def begin_of_playing_round(self):
        self.guaranteed_winners = self.define_guaranteed_winners()
        self.melds = self.define_melds_on_hand()



    def define_guaranteed_winners2(self, cards_played: list['Card'], trump) -> list['Card']:
        res = []
        f_res = []
        not_played = [card for card in self.cards_manipulator.full_deck() if card not in cards_played]
        if trump is None or not [card for card in not_played if card.suit == trump]:
            s_cards = sorted([card for card in not_played if card.suit == "S"], key = lambda x: x.value, reverse = True)
            c_cards = sorted([card for card in not_played if card.suit == "C"], key = lambda x: x.value, reverse = True)
            d_cards = sorted([card for card in not_played if card.suit == "D"], key = lambda x: x.value, reverse = True)
            h_cards = sorted([card for card in not_played if card.suit == "H"], key = lambda x: x.value, reverse = True)

            if s_cards:
                res.append(s_cards[0])
            if c_cards:
                res.append(c_cards[0])
            if d_cards:
                res.append(d_cards[0])
            if h_cards:
                res.append(h_cards[0])
            for card in res:
                if card in self.hand:
                    f_res.append(card)
            return f_res
        else:
            res = [sorted([card for card in not_played if card.suit == trump], key = lambda x: x.value, reverse = True)[0]]
            for card in res:
                if card in self.hand:
                    f_res.append(card)
            return f_res


    def define_guaranteed_winners(self) -> list['Card']: # nie dziala w trakcie rozgrywki tylko przed jej rozpoczęciem
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

    def play_not_first_card(self, first_card, second_card, trump, played_cards=[]) -> 'Card':
        possible_moves = self.possible_moves(first_card, second_card, trump)
        if len(possible_moves) == 1:
            c = possible_moves[0]
            self.hand.remove(c)
            return c
        else:
            guaranteed_winners = self.define_guaranteed_winners2(played_cards, trump)
            if first_card in guaranteed_winners:
                if self.cards_manipulator.all_in_same_suit(possible_moves):
                    c = min(possible_moves)
                    self.hand.remove(c)
                    return c
                else:
                    c = random.choice(possible_moves)
                    self.hand.remove(c)
                    return c # zamienić na monte carlo
            else:
                if second_card is not None:
                    if second_card.can_beat(first_card, trump):
                        greater = second_card
                    else:
                        greater = first_card
                    for card in possible_moves:
                        if card.can_beat(greater, trump):
                            self.hand.remove(card)
                            return card
                else:
                    for card in possible_moves:
                        if card.can_beat(first_card, trump):
                            self.hand.remove(card)
                            return card
        c = random.choice(possible_moves)
        self.hand.remove(c)
        return c # zamienić na monte carlo






    def play_card(self, first_card, second_card, trump, played_cards=[]) -> 'Card':
        if played_cards is None:
            played_cards = []
        if first_card is None:
            return self.play_first_card2(played_cards, trump)
        else:
            return self.play_not_first_card(first_card, second_card, trump, played_cards)


    def play_first_card2(self, played_cards, trump) -> 'Card':
        guaranteed_winners = self.define_guaranteed_winners2(played_cards, trump)
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
            return self.hand.pop() # zamienić na monte carlo












