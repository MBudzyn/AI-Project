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

    def get_player_by_index(self, index: int) -> 'Player':
        return self.players_in_order[index]

    def deal_valid_cards(self):
        redraw_needed = True
        while redraw_needed:
            self.deal_start_cards()
            redraw_needed = any([player.redraw() for player in self.players_in_order])

    def deal_start_cards(self):
        talon, hand1, hand2, hand3 = self.deck.split_three_seven_seven_seven()
        self.talon = talon
        self.players_in_order[0].set_hand(hand1)
        self.players_in_order[1].set_hand(hand2)
        self.players_in_order[2].set_hand(hand3)

    def print_players_hands(self):
        print("player1: ", [str(card) for card in self.players_in_order[0].hand])
        print("player2: ", [str(card) for card in self.players_in_order[1].hand])
        print("player3: ", [str(card) for card in self.players_in_order[2].hand])

    def actualize_after_auction(self, active_player_ind: int):
        self.active_player_index = active_player_ind
        active_player = self.get_player_by_index(active_player_ind)
        active_player.hand += self.talon
        print(self.active_player_index)

    def play(self):
        self.get_player_by_index(2).set_actual_value_in_auction(100)
        self.deal_valid_cards()
        self.print_players_hands()
        to_play = 110
        turn_index = 0
        in_play = [True, True, True]

        while sum(in_play) > 1:
            current_player_index = turn_index % 3
            if not in_play[current_player_index]:
                turn_index += 1
                continue
            player = self.get_player_by_index(current_player_index)
            player_choice = player.decide_to_play_or_pass(to_play)
            if player_choice:
                print(f"Player {current_player_index + 1} plays {to_play}")
                player.set_actual_value_in_auction(to_play)
                to_play += 10
            else:
                print(f"Player {current_player_index + 1} passes")
                in_play[current_player_index] = False
            turn_index += 1

        active_player_index = in_play.index(True)
        self.actualize_after_auction(active_player_index)


auction = Auction([Player(), Player(), Bot()])
auction.play()







