# from classes import *
from classes.game import Game

def play():
    game = Game()

    # for now: all human
    # later: assigning players 1 and 2 based on gamemode?
    # handle swapping in the middle?
    # player_1 = game.state.L1
    # player_2 = game.state.L2

    game.setGamemode()

    while game.whoWins()==None:
        game.display()
        print(f"Player {game.player+1}'s turn")

        move = game.getInput()
        while(not game.apply_action(move)):
            print('Invalid Move')
            move = game.getInput()
        # if move is None:
        #     break

        game.next_turn()

        # if game.isGoal():
        #     print(f"Player {game.player} wins!")
        #     break
    game.display()
    print('Player',game.whoWins(),'wins')

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