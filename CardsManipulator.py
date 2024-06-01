from typeguard import *
from Card import Card
from GlobalVariables import MELD_POINTS_DICT, POINTS_IN_ROUND
from Deck import Deck


@typechecked
class CardsManipulator:
    def __init__(self):
        self.deck = Deck()

    def full_deck(self) -> list['Card']:
        return self.deck.full_deck()
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

    def get_all_poss_hands(self, hand: list['Card']) -> list[list['Card']]:
        return [hand + talon for talon in self.get_all_poss_talons(hand)]

    def parse_pos_hand(self, pos_hand: list['Card']) -> dict[str, list[int]]:
        res = {"H": [0, 0, 0, 0, 0, 0], "D": [0, 0, 0, 0, 0, 0], "C": [0, 0, 0, 0, 0, 0], "S": [0, 0, 0, 0, 0, 0]}
        for card in pos_hand:
            res[card.suit][card.quality] += 1
        return res

    def guaranteed_winners(self, pos_hand: list['Card']) -> dict[str, list[int]]:
        parsed = self.parse_pos_hand(pos_hand)
        res = {"H": [0, 0, 0, 0, 0, 0], "D": [0, 0, 0, 0, 0, 0], "C": [0, 0, 0, 0, 0, 0], "S": [0, 0, 0, 0, 0, 0]}
        for k, value in parsed.items():
            tmp_counter = 0
            s = sum(value)
            for i in range(len(value)):
                if value[i] == 1 or tmp_counter + s >= 6:
                    res[k][i] += value[i]
                    tmp_counter += value[i]
                else:
                    break
        return res

    def calculate_min_result(self, pos_hand: list['Card']) -> int:
        res = 0
        w_n = 0
        melds = []
        points_in_round = POINTS_IN_ROUND
        parsed_hand = self.parse_pos_hand(pos_hand)
        for k, value in parsed_hand.items():
            if value[2] == 1 and value[3] == 1:
                melds.append(k)

        guarantedd_winners = self.guaranteed_winners(pos_hand)
        for k, value in guarantedd_winners.items():
            if value[2] == 1 and value[3] == 1:
                res += MELD_POINTS_DICT[k]
                melds.pop(melds.index(k))

            for i in range(len(value)):
                if value[i] == 1:
                    w_n += 1

        res += max([0] + [MELD_POINTS_DICT[meld] for meld in melds])
        res += sum(points_in_round[:w_n])
        return res

    def calculate_all_pos_results(self, hand: list['Card']) -> list[int]:
        all_pos_hands = self.get_all_poss_hands(hand)
        return sorted([self.calculate_min_result(pos_hand) for pos_hand in all_pos_hands])

    def parse_all_pos_results(self, all_pos_results: list[int]) -> list[tuple[int, int, float]]:
        res = []
        counter = 1
        iterator = 1
        while iterator < len(all_pos_results):
            while iterator < len(all_pos_results) and all_pos_results[iterator] == all_pos_results[iterator - 1]:
                counter += 1
                iterator += 1
            res.append((all_pos_results[iterator - 1], counter, round(counter / len(all_pos_results) * 100, 2)))
            counter = 1
            iterator += 1
        if len(all_pos_results) > 1 and all_pos_results[-1] != all_pos_results[-2]:
            res.append((all_pos_results[-1], 1, round(1 / len(all_pos_results) * 100, 2)))

        return res

    def dict_of_probabilities(self, data: list[tuple[int, int, float]]) -> dict[str, float]:
        res = {"<100": 0, ">=100": 0, ">=110": 0, ">=120": 0
            , ">=130": 0, ">=140": 0, ">=150": 0, ">=160": 0
            , ">=170": 0, ">=180": 0, ">=190": 0, ">=200": 0
            , ">=210": 0, ">=220": 0}
        for value, count, percentage in data:
            if value < 100:
                res["<100"] += percentage
            if value >= 100:
                res[">=100"] += percentage
            if value >= 110:
                res[">=110"] += percentage
            if value >= 120:
                res[">=120"] += percentage
            if value >= 130:
                res[">=130"] += percentage
            if value >= 140:
                res[">=140"] += percentage
            if value >= 150:
                res[">=150"] += percentage
            if value >= 160:
                res[">=160"] += percentage
            if value >= 170:
                res[">=170"] += percentage
            if value >= 180:
                res[">=180"] += percentage
            if value >= 190:
                res[">=190"] += percentage
            if value >= 200:
                res[">=200"] += percentage
            if value >= 210:
                res[">=210"] += percentage
            if value >= 220:
                res[">=220"] += percentage
        return res

    def get_dict_of_probabilities(self, hand: list['Card']) -> dict[str, float]:
        p = self.calculate_all_pos_results(hand)
        return self.dict_of_probabilities(self.parse_all_pos_results(p))
