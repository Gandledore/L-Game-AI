import Players
from classes.game import Game

from typing import Tuple,List,Optional
import numpy as np
import time
import cProfile
import pstats
from tqdm import tqdm

# gamemode input, exception handling
def getPlayers()->Tuple[
                    Tuple[int,Optional[int],Optional[bool]],
                    Tuple[int,Optional[int],Optional[bool]]]:
    print(f"\
                                0 = human\n\
                                1 = agent\n\
                                2 = random\n")
    
    players = []
    for i in range(2):
        while True:
            try:
                p = int(input(f"\
                                Enter Player {i+1}: "))
                if p not in {0, 1, 2}:
                    raise ValueError()
                if p==1:
                    depth = int(input(f"\
                                Player {i+1} Depth (int or -1): "))
                    prune = bool(int(input(f"\
                                Player {i+1} Prune (0 or 1): ")))
                    player = [p,depth,prune]
                else: player = [p,None,None]
                players.append(tuple(player))
                print()
                break
            except ValueError:
                print('Invalid Input')
        
    return tuple(players)

def setGameMode(p1,p2)->Tuple[np.ndarray[bool],np.ndarray[Players.Player]]:
    # instantiating players
    player_dict = {
        0: Players.Human,
        1: Players.Agent,
        2: Players.RandomAgent,
    }
    player1 = player_dict[p1[0]](0) if p1[1]==None else player_dict[p1[0]](0,p1[1],p1[2])
    player2 = player_dict[p2[0]](1) if p2[1]==None else player_dict[p2[0]](1,p2[1],p2[2])
    players = np.array([player1,player2])
    return np.array([p1[0]==2,p2[0]==2]),players

def play(gm:Tuple[Tuple[int,Optional[int],Optional[int]],Tuple[int,Optional[int],Optional[int]]]=None,N:int=1,display=True)->Tuple[np.ndarray,np.ndarray,List[List[float]]]:
    game = Game()
    
    if gm==None:
        randoms,players = setGameMode(*getPlayers())
    else:
        randoms,players = setGameMode(*gm)
    winners  = np.empty(shape=(N),dtype=int)
    turns = np.empty(shape=(N),dtype=int)
    turn_times = [[],[]]
    for n in tqdm(range(N)):
        for i,r in enumerate(randoms):
            if r:
                players[i].set_seed(n+i)
        while game.whoWins()==None and game.totalTurns()<64:
            if display:
                # print(game.state)
                # game.display(internal_display=True)
                game.display()
            turn = game.getTurn()
            if display: print(f"Player {turn+1}'s turn ({game.totalTurns()})")
            
            current_player = players[turn]
            success=False
            K = 3
            for k in range(K):#while True
                try:
                    start = time.time()
                    move = current_player.getMove(game.getState(),display) #value error if invalid input format
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
        winner = winner if game.totalTurns()<64 else 0
        winners[n] = winner
        turns[n] = game.totalTurns()

        if display: 
            game.display()
            print('Player',winner,'wins!')
            print('Total Turns',game.totalTurns())
            
        game.reset()
        for player in players:
            player.game_reset()
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
    stats.sort_stats("time").print_stats(16)
    