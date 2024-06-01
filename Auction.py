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
        self.playing_player_index = 0
        self.active_player_index = 0

    def deal_start_cards(self):
        hand1, hand2, hand3, hand4 = self.deck.split_three_seven_seven_seven()
        self.talon = hand1
        self.players_in_order[0].set_hand(hand2)
        self.players_in_order[1].set_hand(hand3)
        self.players_in_order[2].set_hand(hand4)

    def play(self):
        to_play = 110
        redraw_needed = True
        while redraw_needed:
            self.deal_start_cards()
            redraw_needed = any([player.redraw() for player in self.players_in_order])

        turn_index = 0
        self.players_in_order[2].actual_value_in_auction = 100
        in_play = [True, True, True]
        print("player1: ", [str(card) for card in self.players_in_order[0].hand])
        print("player2: ", [str(card) for card in self.players_in_order[1].hand])
        print("player3: ", [str(card) for card in self.players_in_order[2].hand])

        while sum(in_play) > 1:
            current_player_index = turn_index % 3
            if not in_play[current_player_index]:
                turn_index += 1
                continue

            player = self.players_in_order[current_player_index]
            player_choice = player.decide_to_play_or_pass(to_play)
            if player_choice:
                print(f"Player {current_player_index + 1} plays {to_play}")
                player.actual_value_in_auction = to_play
                to_play += 10
            else:
                print(f"Player {current_player_index + 1} passes")
                in_play[current_player_index] = False

            turn_index += 1

        active_player_index = in_play.index(True)
        self.active_player_index = active_player_index
        active_player = self.players_in_order[active_player_index]
        active_player.hand += self.talon
        print(self.active_player_index)





auction = Auction([Player(), Player(), Bot()])
auction.play()







