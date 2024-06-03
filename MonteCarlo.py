

import copy
import concurrent.futures
import time
from Auction import Auction
from Player import Player
from Bot import Bot
from typeguard import *
from GlobalVariables import MELD_POINTS_DICT

import random
import math


@typechecked
class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0  # To będzie przechowywać sumę punktów zdobytych w symulacjach

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_actions())

    def best_child(self, c_param=math.sqrt(2)):
        choices_weights = [
            (child.wins / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self):
        actions = self.state.get_legal_actions()
        for action in actions:
            new_state = self.state.take_action(action)
            child_node = MCTSNode(new_state, parent=self)
            self.children.append(child_node)
            return child_node
        raise Exception("Should never reach here if node is not fully expanded")

    def best_action(self):
        visits = [child.visits for child in self.children]
        return self.children[visits.index(max(visits))]

    def simulate_single(self):
        current_state = self.state.clone()
        while current_state.get_legal_actions():
            current_state = current_state.take_action(random.choice(current_state.get_legal_actions()))
        return current_state.calculate_if_its_win(self.state.our_player_ind)

    def simulate(self, ite=6):
        points = 0
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.simulate_single) for _ in range(ite)]
            for future in concurrent.futures.as_completed(futures):
                points += future.result()
        return points


class MCTS:
    def __init__(self, itermax):
        self.itermax = itermax

    def search(self, initial_state):
        root = MCTSNode(state=initial_state)

        for _ in range(self.itermax):
            node = root

            # Selection
            while node.is_fully_expanded() and node.children:
                node = node.best_child()

            # Expansion
            if not node.is_fully_expanded():
                node = node.expand()

            # Simulation
            points = node.simulate()

            # Backpropagation
            while node is not None:
                node.visits += 1
                node.wins += points
                node = node.parent

        return root.best_action().state.last_action


# Example usage with hypothetical game state:
class GameState:

    def __init__(self, players_in_order, playing_player_ind, trump,
                 our_player_ind: int, main_player_ind: int,
                 points_to_play: int, cards_on_table = [None, None, None]):
        self.players_in_order = players_in_order
        self.playing_player_index: int = playing_player_ind
        self.our_player_ind = our_player_ind
        self.main_player_ind = main_player_ind
        self.cards_on_table = cards_on_table
        self.points_to_play = points_to_play
        self.trump = trump
        self.last_action = None


    def get_player_by_ind(self, ind):
        return self.players_in_order[ind]
    def get_legal_actions(self) -> list['Card']:
        return self.get_player_by_ind(self.playing_player_index).possible_moves(self.cards_on_table[0], self.cards_on_table[1], self.trump)

    def take_action(self, card: 'Card'):
        from Game import winning_card
        new_state = self.clone()
        new_state.last_action = card
        if new_state.cards_on_table[0] is None and new_state.cards_on_table[1] is None and new_state.cards_on_table[2] is None:
            if self.get_player_by_ind(self.playing_player_index).is_melding(card):
                new_state.get_player_by_ind(self.playing_player_index).sum_of_points += MELD_POINTS_DICT[card.suit]
                new_state.trump = card.suit
        new_state.cards_on_table[new_state.playing_player_index] = card
        new_state.get_player_by_ind(new_state.playing_player_index).hand.remove(card)
        new_state.playing_player_index = (new_state.playing_player_index + 1) % 3
        if new_state.cards_on_table[0] is not None and new_state.cards_on_table[1] is not None and new_state.cards_on_table[2] is not None:
            w_c = winning_card(new_state.cards_on_table, new_state.trump)
            card_ind = new_state.cards_on_table.index(w_c)
            winner_index = (new_state.playing_player_index + card_ind) % 3
            new_state.get_player_by_ind(winner_index).trick_pile += new_state.cards_on_table
            new_state.get_player_by_ind(winner_index).sum_of_points += sum([card.value for card in new_state.cards_on_table])
            new_state.playing_player_index = winner_index
            new_state.cards_on_table = [None, None, None]
        return new_state



    def calculate_if_its_win(self, our_player_ind):
        if our_player_ind == self.main_player_ind:
            return 1 if self.get_player_by_ind(self.main_player_ind).sum_of_points >= self.points_to_play else 0
        else:
            return 1 if self.get_player_by_ind(self.main_player_ind).sum_of_points < self.points_to_play else 0


    def clone(self):
        return copy.deepcopy(self)




# Initialize game state
# auction = Auction([Player(), Player(), Bot()])
# auction.play()
# from Game import Game
# game = Game(auction)
# initial_state = GameState(auction.players_in_order, auction.playing_player_index,None,
#                           2,auction.playing_player_index, game.get_player_by_index(auction.playing_player_index).actual_value_in_auction)

# s = time.time()
# mcts = MCTS(itermax=20)
# best_action = mcts.search(initial_state)
# print(best_action)
# e = time.time()
# print("time: " ,e-s)
