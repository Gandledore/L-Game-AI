import Players
from classes.game import Game

def play():
    game = Game()

    # for now: all human
    # later: assigning players 1 and 2 based on gamemode?
    # handle swapping in the middle?
    # players = [Players.Human(),Players.RandomAgent()]
    players = [Players.RandomAgent(),Players.RandomAgent()]

    game.setGamemode()
    
    while game.whoWins(game.state)==None:
        game.display()
        print(f"Player {game.player+1}'s turn")

        # move = game.getInput() if isinstance(players[game.player],Players.Human) else players[game.player].getMove(game)
        move = players[game.player].getMove(game)
        while(not game.apply_action(game.state,move)):
            print('Invalid Move')
            # move = game.getInput()
            move = players[game.player].getMove(game)
        # if move is None:
        #     break

        game.next_turn()

        # if game.isGoal():
        #     print(f"Player {game.player} wins!")
        #     break
    game.display()
    print('Player',game.whoWins(game.state),'wins')

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