from base_structs import *
from game import Game

def play():
    game = Game()
    firstPlayer = True

    # for now: all human
    # later: assigning players 1 and 2 based on gamemode?
    # handle swapping in the middle?
    player_1 = game.state.L1
    player_2 = game.state.L2

    game.setGamemode()

    while True:
        game.display()
        if game.gamemode == 0:
            if firstPlayer:
                print("Player 1's turn")
                game.player = 0
            else:
                print("Player 2's turn")
                game.player = 1
        else:
            print(f"Player {game.player}'s turn")

        game.getInput()
        
        # if move is None:
        #     break

        # game.display()
        firstPlayer = not firstPlayer

        if game.isGoal():
            print(f"Player {game.player} wins!")
            break


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


        # if game.player == 0:
        #     player_1.newPos(move)
        # else:
        #     player_2.newPos(move)