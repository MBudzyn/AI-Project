from typeguard import *
from Card import Card
from CardsManipulator import CardsManipulator
import random
from GlobalVariables import *
from Player import Player


@typechecked
class Game:
    def __init__(self, players_in_order: list['Player']):
        self.players_in_order: list['Player'] = players_in_order
        self.cards_manipulator = CardsManipulator()
        self.playing_player_index = 0
        self.trick_pile: list['Card'] = []
        self.trump = None


