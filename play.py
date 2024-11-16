import Players
from classes.game import Game

from typing import Tuple,List
import copy

def setGameMode()->Tuple[int,List[Players.Player]]:

    # gamemode input, exception handling
    while True:
        try:
            modeInput = int(input("0 = human vs human\n1 = human vs agent\n2 = agent vs agent\nEnter your mode: "))
            
            if modeInput not in [0, 1, 2, 3, 4]:
                raise ValueError("Invalid input")
            break

        except ValueError:
            print(f"Invalid input")
        
    # instantiating players
    if modeInput == 0:
        players = [Players.Human(0),Players.Human(1)]
    elif modeInput == 1:
        players = [Players.Human(0),Players.RandomAgent(1)]
    elif modeInput == 2:
        players = [Players.RandomAgent(0),Players.RandomAgent(1)]
    
    elif modeInput == 3:
        players = [Players.Agent(0),Players.RandomAgent(1)]
    elif modeInput == 4:
        players = [Players.Agent(0),Players.Agent(1)]

    return modeInput,players

def play():
    game = Game()
    
    # Enter gamemode 0, 1, or 2
    gamemode,players = setGameMode()

    K = 3
    winner = None
    while winner==None:
        game.display()
        turn = game.getTurn()
        print(f"Player {turn+1}'s turn")
        
        current_player = players[turn]
        success=False
        for i in range(K):#while True
            try:
                move = current_player.getMove(copy.deepcopy(game.state)) #value error if invalid input format
                game.apply_action(move)  #assertion error if invalid move
                success=True
                break
            except ValueError as e:
                print(f'Invalid Input. {e}\n')
            except AssertionError as e:
                print(f'Invalid Move. {e}\n')
        if not success: #if no valid move provided after K attempts, kill game
            print(f'\n\nNo valid play after {K} moves. Game over.')
            break
        winner = game.whoWins()

    game.display()
    print('Player',bool(winner)+1,'wins!')

if __name__ == "__main__":
    play()