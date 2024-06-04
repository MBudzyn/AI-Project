

import copy
import concurrent.futures
import time
from Auction import Auction
from Player import Player
from Bot import Bot
from typeguard import *
from GlobalVariables import MELD_POINTS_DICT, MONTE_CARLO_ITERATIONS, MONTE_CARLO_SYMULATIONS
import random
import math
import logging

logging.basicConfig(level=logging.DEBUG)

@typechecked
class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

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
            if not any(child.state.last_action == action for child in self.children):
                new_state = self.state.take_action(action)
                child_node = MCTSNode(new_state, parent=self)
                self.children.append(child_node)
                logging.debug(f"Expanded with action: {action}, total children: {len(self.children)}")
                return child_node
        raise Exception("Should never reach here if node is not fully expanded")

    def best_action(self):
        visits = [child.visits for child in self.children]
        return self.children[visits.index(max(visits))]

    def simulate_single(self):
        current_state = self.state.clone()
        while current_state.get_legal_actions():
            current_state = current_state.take_action(random.choice(current_state.get_legal_actions()))
        return current_state.calculate_if_its_win(self.state.actual_moving_player)

    def simulate(self, ite=MONTE_CARLO_SYMULATIONS):
        points = 0
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.simulate_single) for _ in range(ite)]
            for future in concurrent.futures.as_completed(futures):
                points += future.result()
        return points


class MCTS:
    def __init__(self, itermax=MONTE_CARLO_ITERATIONS):
        self.itermax = itermax

    def search(self, initial_state):
        root = MCTSNode(state=initial_state)

        for i in range(self.itermax):
            node = root

            # Selection
            while node.is_fully_expanded() and node.children:
                node = node.best_child()
                logging.debug(f"Selection - Iteration {i}: Best child selected")

            # Expansion
            if not node.is_fully_expanded():
                node = node.expand()
                logging.debug(f"Expansion - Iteration {i}: Node expanded")

            # Simulation
            points = node.simulate()
            logging.debug(f"Simulation - Iteration {i}: Points scored {points}")

            # Backpropagation
            while node is not None:
                node.visits += 1
                node.wins += points
                logging.debug(f"Backpropagation - Iteration {i}: Node visits {node.visits}, wins {node.wins}")
                node = node.parent

        return root.best_action().state.last_action


class GameState:
    def __init__(self, players_in_order, trump,
                 actual_moving_player, main_player_ind: int,
                 points_to_play: int, cards_on_table=[None, None, None]):
        self.players_in_order = players_in_order
        self.actual_moving_player = actual_moving_player
        self.main_player_ind = main_player_ind
        self.cards_on_table = cards_on_table
        self.points_to_play = points_to_play
        self.trump = trump
        self.last_action = None

    def get_player_by_ind(self, ind):
        return self.players_in_order[ind]

    def get_legal_actions(self) -> list['Card']:
        return self.get_player_by_ind(self.actual_moving_player).possible_moves(self.cards_on_table[0], self.cards_on_table[1], self.trump)

    def take_action(self, card: 'Card'):
        from Game import winning_card
        new_state = self.clone()
        new_state.last_action = card
        if all(c is None for c in new_state.cards_on_table):
            if self.get_player_by_ind(self.actual_moving_player).is_melding(card):
                new_state.get_player_by_ind(self.actual_moving_player).sum_of_points_in_actual_round += MELD_POINTS_DICT[card.suit]
                new_state.trump = card.suit
        new_state.cards_on_table[new_state.actual_moving_player] = card
        new_state.get_player_by_ind(new_state.actual_moving_player).hand.remove(card)
        new_state.actual_moving_player = (new_state.actual_moving_player + 1) % 3


        if all(c is not None for c in new_state.cards_on_table):
            w_c = winning_card(new_state.cards_on_table, new_state.trump)
            card_ind = new_state.cards_on_table.index(w_c)
            winner_index = card_ind
            new_state.get_player_by_ind(winner_index).trick_pile += new_state.cards_on_table
            new_state.get_player_by_ind(winner_index).sum_of_points_in_actual_round += sum(card.value for card in new_state.cards_on_table)
            new_state.actual_moving_player = winner_index
            new_state.cards_on_table = [None, None, None]
        return new_state

    def calculate_if_its_win(self, moving_player_ind: int):
        if moving_player_ind == self.main_player_ind:
            return 1 if self.get_player_by_ind(self.main_player_ind).sum_of_points_in_actual_round >= self.points_to_play else 0
        else:
            return 1 if self.get_player_by_ind(self.main_player_ind).sum_of_points_in_actual_round < self.points_to_play else 0

    def clone(self):
        return copy.deepcopy(self)

# Test function to execute Monte Carlo Tree Search
