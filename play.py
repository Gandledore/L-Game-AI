import Players
from classes.game import Game

from typing import Tuple,List
import numpy as np
import time
import cProfile
import pstats

def getGameMode()->int:
    # gamemode input, exception handling
    while True:
        try:
            modeInput = int(input( "\
                                    0 = human vs human\n\
                                    1 = human vs agent\n\
                                    2 = agent vs agent\n\
                                    Enter your mode: "))
            
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
        players = [Players.Agent(0),Players.Human(1)]
    elif mode == 2:
        players = [Players.Agent(0),Players.Agent(1)]
    
    elif mode == 3:
        players = [Players.Agent(0),Players.RandomAgent(1)]
    elif mode == 4:
        players = [Players.RandomAgent(0),Players.RandomAgent(1)]
    else:
        print(f'Gamemode {mode} not defined')
    return mode,players

def play(gm:int=-1,N:int=1,display=True)->Tuple[np.ndarray,np.ndarray,List[List[float]]]:
    game = Game()
    
    # Enter gamemode 0, 1, or 2
    if gm==-1:
        gamemode,players = setGameMode(getGameMode())
    else:
        gamemode,players = setGameMode(gm)    
    winners  = np.empty(shape=(N),dtype=int)
    turns = np.empty(shape=(N),dtype=int)
    turn_times = [[],[]]
    for n in range(N):
        while game.whoWins()==None:
            # print('Gamestates Generated:',gamestate._count)
            if display: game.display()
            turn = game.getTurn()
            if display: print(f"Player {turn+1}'s turn ({game.totalTurns()})")
            
            current_player = players[turn]
            success=False
            K = 3
            for k in range(K):#while True
                try:
                    start = time.time()
                    move = current_player.getMove(game.getState()) #value error if invalid input format
                    end=time.time()
                    # if display: print("Move:",move)
                    game.apply_action(move)  #assertion error if invalid move
                    success=True
                    turn_times[turn].append(end-start)
                    break
                except ValueError as e:
                    print(f'Invalid Input. {e}\n')
                except AssertionError as e:
                    print(f'Invalid Move. {e}\n')
            if not success: #if no valid move provided after K attempts, kill game
                print(f'\n\nNo valid play after {K} moves. Game over.')
                break

        winner = game.whoWins()
        winner = int(not turn)+1 if winner==None else winner+1
        winners[n] = winner
        turns[n] = game.totalTurns()

        if display: 
            game.display()
            print('Player',winner,'wins!')
            print('Total Turns',game.totalTurns())
            
        game.reset()
        if not display: print(f'{100*(n+1)/(N):.1f}%',end='\r')
    print()
    length = max(len(turn_times[0]),len(turn_times[1]))
    turn_times = [row + [0] * (length - len(row)) for row in turn_times]
    return winners, turns, turn_times

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    
    _,_,_ = play()
    
    profiler.disable()
    
    stats = pstats.Stats(profiler)
    
    # Sort by 'time' (total time in each function) and print the top 10 functions
    stats.strip_dirs()  # Optional: remove long file paths for readability
    stats.sort_stats("time").print_stats(10)
    