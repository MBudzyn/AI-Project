from Bot import Bot
from Auction import Auction
from Player import Player
from Game import Game


player1 = Player()
player2 = Player()
bot1 = Bot([player1, player2])

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



def test_game_parameters_actualization():
    ptable = [player1, player2, bot1]
    for i in range(1):
        ptable = [ptable[-1]] + ptable[:-1]
        auction = Auction(ptable)
        auction.play()
        print_data(ptable)
        game = Game(auction)
        game.play(True)
        print("Player1 s",player1.sum_of_points_in_actual_round,"all_points", player1.sum_of_points)
        print("Player2 s", player2.sum_of_points_in_actual_round, "all_points", player2.sum_of_points)
        print("Bot s", bot1.sum_of_points_in_actual_round, "all_points", bot1.sum_of_points)
        print(auction.active_player_index)





