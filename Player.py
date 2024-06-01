from typeguard import *
from Card import Card
from CardsManipulator import CardsManipulator
import random
from GlobalVariables import *

@typechecked
class Player:
    def __init__(self):
        self.hand: list['Card'] = []
        self.trick_pile: list['Card'] = []
        self.other_players: list['Player'] = []
        self.played: list['Card'] = []
        self.cards_manipulator = CardsManipulator()
        self.actual_value_in_auction = 0 # pamietac zeby aktualizowac
        self.sum_of_points = 0
        self.is_declarer = False
        self.declaration_history: list[list[int]] = []
        self.trump = None

    def set_hand(self, hand: list['Card']):
        self.hand = hand

    def add_card_to_hand(self, card: 'Card'):
        self.hand.append(card)

    def add_cards_to_trick_pile(self, cards: list['Card']):
        self.trick_pile += cards

    def calculate_act_score(self) -> int:
        return sum([card.value for card in self.trick_pile])

    def is_melding(self, card: 'Card') -> bool:
        return card.is_part_of_meld() and any([card.is_meld(other) for other in self.hand if other != card])

    def calculate_act_hand(self) -> int:
        return sum([card.value for card in self.hand])

    def have_eighteen(self) -> bool:
        return self.calculate_act_hand() >= 18

    def have_meld(self) -> bool:
        tmp = [card for card in self.hand if card.is_part_of_meld()]
        if len(tmp) < 2:
            return False

        return any([tmp[i].is_meld(tmp[j]) for i in range(len(tmp) - 1) for j in range(i + 1, len(tmp))])

    def cards_in_meld_suite(self):
        counter = 0
        if not self.have_meld():
            return 0
        tmp = [card for card in self.hand if card.is_part_of_meld()]
        suites = set([card.suit for card in tmp])
        for card in self.hand:
            if card.suit in suites:
                counter += 1
        return counter

    def redraw(self) -> bool:
        return not self.correct_hand()

    def possible_moves(self, first_card ,second_card, trump) -> list['Card']:
        if first_card is None:
            return self.hand
        if second_card is not None:
            if first_card.suit == second_card.suit:
                card_to_compare = max(first_card, second_card)
            elif second_card.suit == trump:
                card_to_compare = second_card
            else:
                card_to_compare = first_card
        else:
            card_to_compare = first_card
        in_suit = [card for card in self.hand if card.suit == first_card.suit]
        if in_suit:
            greater = [card for card in in_suit if card.can_beat(card_to_compare,trump)]
            if greater:
                return greater
            return in_suit
        else:
            greater = [card for card in self.hand if card.can_beat(card_to_compare,trump)]
            if greater:
                return greater
            else:
                return self.hand

    def play_card(self, first_card, second_card, trump) -> 'Card':
        c = random.choice(self.possible_moves(first_card = first_card, second_card = second_card, trump = trump))
        self.hand.remove(c)
        self.played.append(c)
        return c

    def discard_two_cards(self) -> list['Card']:
        pom = random.sample(self.hand, 2)
        self.hand = [card for card in self.hand if card not in pom]
        return pom

    def decide_to_play_or_pass(self, points: int) -> bool:
        return random.choice([True] * PROBABILITY_TO_PLAY_FOR_RANDOM +
                             [False] * (100 - PROBABILITY_TO_PLAY_FOR_RANDOM))

    def correct_hand(self) -> bool:
        return self.have_eighteen()
