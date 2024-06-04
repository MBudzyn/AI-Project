from Bot import Bot
from Auction import Auction
from Player import Player
from Game import Game
from GlobalVariables import MAX_POINTS

def print_data(list_of_players):
    print("------------------------------------------------")
    for i in range(len(list_of_players)):
        print()
        print("Player: ", i + 1)
        print("Hand: ", [str(card) for card in list_of_players[i].hand])
        print("Trick pile: ", [str(card) for card in list_of_players[i].trick_pile])

        print("is_declarer: ", list_of_players[i].is_declarer)
        print("sum_of_points: ", list_of_players[i].sum_of_points)
        print("sum_of_points_in_actual_round: ", list_of_players[i].sum_of_points_in_actual_round)
        print("actual_value_in_auction: ", list_of_players[i].actual_value_in_auction)
        print("points_to_play: ", list_of_players[i].points_to_play)
    print("------------------------------------------------")



class FullGame:
    def __init__(self):
        self.p1 = Player()
        self.p2 = Player()
        self.b1 = Bot([self.p1, self.p2])

    def is_game_over(self, points_to_play):
        return (self.p1.sum_of_points >= points_to_play or
                self.p2.sum_of_points >= points_to_play or
                self.b1.sum_of_points >= points_to_play)

    def play(self):
        ptable = [self.p1, self.p2, self.b1]
        while not self.is_game_over(MAX_POINTS):
            ptable = [ptable[-1]] + ptable[:-1]
            auction = Auction(ptable)
            auction.play()
            game = Game(auction)
            game.play()
            print_data(ptable)
        self.print_final_results()
            
    def print_final_results(self):
        print("Player1 all_points", self.p1.sum_of_points)
        print("Player2 all_points", self.p2.sum_of_points)
        print("Bot all_points", self.b1.sum_of_points)



full_game = FullGame()
full_game.play()