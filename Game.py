from typeguard import *
from Card import Card
from CardsManipulator import CardsManipulator
import random
from GlobalVariables import *
from Player import Player
from Auction import Auction
import pygame
import time
from Bot import Bot

def winning_card(cards_in_order: list['Card'], trump) -> 'Card':
    if cards_in_order[1].can_beat(cards_in_order[0], trump):
        if cards_in_order[2].can_beat(cards_in_order[1], trump):
            return cards_in_order[2]
        else:
            return cards_in_order[1]
    else:
        if cards_in_order[2].can_beat(cards_in_order[0], trump):
            return cards_in_order[2]
        else:
            return cards_in_order[0]


@typechecked
class Game:
    def __init__(self, auction: 'Auction'):
        self.players_in_order: list['Player'] = auction.players_in_order
        self.cards_manipulator = CardsManipulator()
        self.playing_player_index = auction.active_player_index
        self.trick_pile: list['Card'] = []
        self.trump = None
        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1600, 1000))
        pygame.display.set_caption('Thousand Card Game')
        self.card_images = self.load_card_images()
        self.background = pygame.image.load('graphics/board.png')
        self.font = pygame.font.Font(None, 36)
        self.player_positions = [(250, 200), (750, 750), (750, 200)]  # Pozycje kart graczy

    def load_card_images(self):
        card_images = {}
        for suit in ["H", "D", "C", "S"]:
            for rank in ["N", "T", "J", "Q", "K", "A"]:
                card_images[f'{rank}{suit}'] = pygame.image.load(f'graphics/{rank}{suit}.png')
        return card_images

    def draw_cards(self, cards_in_order):
        self.screen.blit(self.background, (0, 0))

        # Rysuj karty graczy
        for i, player in enumerate(self.players_in_order):
            player_hand = player.hand
            for j, card in enumerate(player_hand):
                card_image = self.card_images[f'{card.rank}{card.suit}']
                self.screen.blit(card_image, (self.player_positions[i][0] + 60 * j, self.player_positions[i][1]))

        # Rysuj karty na stole
        positions = [(550, 400), (650, 500), (750, 400)]
        for i, card in enumerate(cards_in_order):
            if card:
                card_image = self.card_images[f'{card.rank}{card.suit}']
                self.screen.blit(card_image, positions[i])
                pygame.display.flip()
                time.sleep(1.5)
    def play2(self, draw: bool = False):
        two_cards = self.players_in_order[self.playing_player_index].discard_two_cards()
        self.players_in_order[(self.playing_player_index - 1) % 3].hand += [two_cards[0]]
        self.players_in_order[(self.playing_player_index + 1) % 3].hand += [two_cards[1]]

        for i in range(8):
            print(f"\nTrick {i + 1}:")
            cards_in_order = [None, None, None]

            current_player_index = self.playing_player_index
            if current_player_index == 2:
                cards_in_order[0] = self.players_in_order[current_player_index].play_first_card_in_trick()
            else:
                cards_in_order[0] = self.players_in_order[current_player_index].play_random_card(None, None, self.trump)
            if self.players_in_order[current_player_index].is_melding(cards_in_order[0]):
                print(f"Player {current_player_index + 1} melds!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {cards_in_order[0]}")
                self.trump = cards_in_order[0].suit
            print(f"Player {current_player_index + 1} played {cards_in_order[0]}")

            for j in range(1,3):
                current_player_index = (self.playing_player_index + j) % 3
                cards_in_order[j] = self.players_in_order[current_player_index].play_random_card(cards_in_order[0],
                                                                                                 cards_in_order[1],
                                                                                                 self.trump)
                print(f"Player {current_player_index + 1} played {cards_in_order[j]}")

            w_card = winning_card(cards_in_order, self.trump)
            card_ind = cards_in_order.index(w_card)
            winner_index = (self.playing_player_index + card_ind) % 3
            print(f"Winning card: {w_card} by Player {winner_index + 1}")

            self.players_in_order[winner_index].trick_pile += cards_in_order
            self.players_in_order[winner_index].sum_of_points += sum([card.value for card in cards_in_order])
            self.playing_player_index = winner_index

            # Print remaining hands
            for k in range(3):
                player_index = (self.playing_player_index + k) % 3
                print(
                    f"Player {player_index + 1} remaining hand: {[str(card) for card in self.players_in_order[player_index].hand]}")

            # Print the trick pile and sum of points for each player
            for k in range(3):
                print(f"Player {k + 1} trick pile: {[str(card) for card in self.players_in_order[k].trick_pile]}")
                print(f"Player {k + 1} sum of points: {self.players_in_order[k].sum_of_points}")

            if self.trump:
                print(f"Current trump: {self.trump}")
            else:
                print("No trump declared yet")
            if draw:
                self.draw_cards(cards_in_order)
auction = Auction([Player(), Player(), Bot()])
auction.play()
print("----------------------------------------------------------------------------------------------------------")
game = Game(auction)
game.play2()
