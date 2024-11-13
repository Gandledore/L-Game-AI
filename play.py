import Players
from classes.game import Game

def setGameMode(self)->None:

    # gamemode input, exception handling
    while True:
        try:
            modeInput = int(input("0 = human vs human\n1 = human vs agent\n2 = agent vs agent\nEnter your mode: "))
            self.gamemode = modeInput
            break
        except modeInput not in [0,1,2]:
            print(f"Invalid input.")
            continue

    # instantiating players

    if self.gamemode == 0:
        players = [Players.Human(),Players.Human()]
    elif self.gamemode == 1:
        players = [Players.Human(),Players.RandomAgent()]
    elif self.gamemode == 2:
        players = [Players.RandomAgent(),Players.RandomAgent()]

    return players

def play():
    game = Game()

    # Enter gamemode 0, 1, or 2
    players = setGameMode(game)
    
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
    print('Player',game.whoWins(game.state),'wins!')

if __name__ == "__main__":
    play()