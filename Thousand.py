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
        print("is_declarer: ", list_of_players[i].is_declarer)
        print("sum_of_points: ", list_of_players[i].sum_of_points)
        print("sum_of_points_in_actual_round: ", list_of_players[i].sum_of_points_in_actual_round)
        print("actual_value_in_auction: ", list_of_players[i].actual_value_in_auction)
        print("points_to_play: ", list_of_players[i].points_to_play)
    print("------------------------------------------------")




for i in range(10):
    auction = Auction([player1, player2, bot1])
    auction.play()
    print_data([player1, player2, bot1])
    game = Game(auction)
    game.play()
    print(player1.sum_of_points_in_actual_round)
    print(player2.sum_of_points_in_actual_round)
    print(auction.active_player_index)