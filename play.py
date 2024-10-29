from base_structs import *
from game import Game

def play():
    game = Game()
    firstPlayer = True

    # assigning players 1 and 2 based on gamemode?
    # handle swapping in the middle?
    player_1 = game.state.L1
    player_2 = game.state.L2

    while True:
        if game.gamemode == 0:
            if firstPlayer:
                print("Player 1's turn")
                game.player = 0
            else:
                print("Player 2's turn")
                game.player = 1
        else:
            print(f"Player {game.player}'s turn")

        move = game.getInput()
        if move is None:
            break

        if game.player == 0:
            player_1.newPos(*move)
        else:
            player_2.newPos(*move)

        game.display()
        firstPlayer = not firstPlayer

if __name__ == "__main__":
    play()

# Agent()
#     player_2 = Agent()

#     while not game.isGoal():
#         if firstPlayer:
#             action = player_1.getInput()
#             game = game.applyAction(action)

#         else:
#             action = player_2.getInput()
#             game = game.applyAction(action)

#         firstPlayer = not firstPlayer
#         game.display()