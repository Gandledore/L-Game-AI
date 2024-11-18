import Players
from classes.game import Game

from typing import Tuple,List
import copy
import numpy as np

def getGameMode()->int:
    # gamemode input, exception handling
    while True:
        try:
            modeInput = int(input("0 = human vs human\n1 = human vs agent\n2 = agent vs agent\nEnter your mode: "))
            
            if modeInput not in [0, 1, 2, 3, 4, 5]:
                raise ValueError("Invalid input")
            break

        except ValueError:
            print(f"Invalid input")
    return modeInput

def setGameMode(mode)->Tuple[int,List[Players.Player]]:
    # instantiating players
    if mode == 0:
        players = [Players.Human(0),Players.Human(1)]
    elif mode == 1:
        players = [Players.Human(0),Players.Agent(1)]
    elif mode == 2:
        players = [Players.Agent(0),Players.Agent(1)]
    
    elif mode == 3:
        players = [Players.Agent(0),Players.RandomAgent(1)]
    elif mode == 4:
        players = [Players.RandomAgent(0),Players.RandomAgent(1)]
    return mode,players

def play():
    game = Game()
    
    # Enter gamemode 0, 1, or 2
    gamemode,players = setGameMode(getGameMode())

    K = 3
    winner = None
    turns = 0
    while winner==None:
        # print('Gamestates Generated:',gamestate._count)
        game.display()
        turn = game.getTurn()
        turns+=1
        print(f"Player {turn+1}'s turn ({turns})")
        
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
    print('Total Turns',turns)
    gs = type(game.state)
    print(f'{gs._count} gamestates generated')
    num_legal_moves_per_state = [len(moves) for state,moves in gs._legalMoves.items()]
    print(f'Branching factor | Max:{np.max(num_legal_moves_per_state)} | Mean: {np.mean(num_legal_moves_per_state):.2f}')
    print(f'CH: {gs._cache_hits} | CM:{gs._cache_misses} | Cache Hit Rate: {100*gs._cache_hits/(gs._cache_misses+gs._cache_hits):.1f}%')
if __name__ == "__main__":
    play()