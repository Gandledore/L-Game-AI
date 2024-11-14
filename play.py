import Players
from classes.game import Game

from typing import Tuple,List

def setGameMode()->Tuple[int,List[Players.Player]]:

    # gamemode input, exception handling
    while True:
        try:
            modeInput = int(input("0 = human vs human\n1 = human vs agent\n2 = agent vs agent\nEnter your mode: "))
            
            if modeInput not in [0,1,2, 3]:
                raise ValueError("Invalid input")
            break

        except ValueError:
            print(f"Invalid input")
        
    # instantiating players
    if modeInput == 0:
        players = [Players.Human(),Players.Human()]
    elif modeInput == 1:
        players = [Players.Human(),Players.RandomAgent()]
    elif modeInput == 2:
        players = [Players.RandomAgent(),Players.RandomAgent()]
    
    elif modeInput == 3:
        players = [Players.Agent(),Players.RandomAgent()]

    return modeInput,players

def play():
    game = Game()
    
    # Enter gamemode 0, 1, or 2
    gamemode,players = setGameMode()

    K = 3
    winner = None
    while winner==None:
        game.display()
        print(f"Player {game.player+1}'s turn")
        
        current_player = players[game.player]
        success=False
        for i in range(K):#while True
            try:
                move = current_player.getMove(game) #value error if invalid input format
                game.apply_action(game.state,move)  #assertion error if invalid move
                success=True
                break
            except ValueError as e:
                print(f'Invalid Input. {e}\n')
            except AssertionError as e:
                print(f'Invalid Move. {e}\n')
        if not success: #if no valid move provided after K attempts, kill game
            print(f'\n\nNo valid play after {K} moves. Game over.')
            break
        game.next_turn()
        winner = game.whoWins(game.state)

    game.display()
    print('Player',winner+1 if winner!=None else int(not game.player)+1,'wins!')

if __name__ == "__main__":
    play()