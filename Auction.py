from typeguard import *
from Card import Card
from CardsManipulator import CardsManipulator
from Deck import Deck
from Player import Player
from Bot import Bot

@typechecked
class Auction:
    def __init__(self, players_in_order: list['Player']):
        self.deck: 'Deck' = Deck()
        self.players_in_order = players_in_order
        self.talon: list['Card'] = []
        self.cards_manipulator: CardsManipulator = CardsManipulator()

    def deal_start_cards(self):
        hand1, hand2, hand3, hand4 = self.deck.split_three_seven_seven_seven()
        self.talon = hand1
        self.players_in_order[0].set_hand(hand2)
        self.players_in_order[1].set_hand(hand3)
        self.players_in_order[2].set_hand(hand4)

    def play(self):
        to_play = 100
        turn_index = 0
        self.deal_start_cards()
        in_play = [True, True, True]

        while sum(in_play) > 1:
            current_player_index = turn_index % 3
            if not in_play[current_player_index]:
                turn_index += 1
                continue

            player = self.players_in_order[current_player_index]
            player_choice = player.decide_to_play_or_pass(to_play)
            if player_choice:
                player.actual_value_in_auction = to_play
                to_play += 10
            else:
                in_play[current_player_index] = False

            turn_index += 1

        active_player_index = in_play.index(True)
        active_player = self.players_in_order[active_player_index]

        print([str(card) for card in active_player.hand], active_player.actual_value_in_auction)
        active_player.hand += self.talon
        print([str(card) for card in self.talon])
        print([str(card) for card in active_player.hand], active_player.actual_value_in_auction)
        print([str(card) for card in self.players_in_order[0].hand], self.players_in_order[0].actual_value_in_auction)
        print([str(card) for card in self.players_in_order[1].hand], self.players_in_order[1].actual_value_in_auction)
        print([str(card) for card in self.players_in_order[2].hand], self.players_in_order[2].actual_value_in_auction)




auction = Auction([Player(), Player(), Bot()])
auction.play()







