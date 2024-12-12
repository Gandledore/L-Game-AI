# our imports
import Players
from classes.game import Game
from classes.base_structs.L_piece import L_piece
from classes.base_structs.token_piece import token_piece

# use Python 3.5 and up (typing library built in)
from typing import Tuple,List,Optional

import sys
import subprocess
import time

# profiling (built in?)
import cProfile
import pstats

# Package install routine

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def install_all():

    install('numpy')
    install('tqdm')

try:
    import numpy as np
    from tqdm import tqdm
except ImportError:
    install_all()

# End package install routine

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

    # handling loading game

    # Set initial state
    
    while True:

        load = input('Load Game? (y/n): ')
        if load.lower() == 'y':
            try:
                filename = input('Enter filename: ')
                print(filename)
                game = Game.load(filename)
                break
            except FileNotFoundError as e:
                print('File not found')


        InitialStateCoordinates = input(f"Enter Initial State Coords [L1, L2, T1, T2] or Default: ")
        InitialStateCoordinatesList = InitialStateCoordinates.split()

        try:
            InitialStateCoordinatesList = InitialStateCoordinates.split()
            if len(InitialStateCoordinatesList) == 0:
                print('Using Default Initial Gamestate')
                game = Game()
                break

            else:
                L1_x, L1_y, L1_d = int(InitialStateCoordinatesList[0]), int(InitialStateCoordinatesList[1]), InitialStateCoordinatesList[2]
                L2_x, L2_y, L2_d = int(InitialStateCoordinatesList[3]), int(InitialStateCoordinatesList[4]), InitialStateCoordinatesList[5]
                T1_x, T1_y = int(InitialStateCoordinatesList[6]), int(InitialStateCoordinatesList[7])
                T2_x, T2_y = int(InitialStateCoordinatesList[8]), int(InitialStateCoordinatesList[9])

                L_pieces = [L_piece(x=L1_x, y=L1_y, d=L1_d), L_piece(x=L2_x, y=L2_y, d=L2_d)]
                token_pieces = {token_piece(x=T1_x, y=T1_y), token_piece(x=T2_x, y=T2_y)}

                # print board to get confirmation from user that they want to use this board

                game = Game(L_pieces=L_pieces, token_pieces=token_pieces)
                game.display()

                confirm = input('Confirm this board? (y/n): ')
                if confirm.lower() == 'y':
                    break
                else:
                    continue

            # break
        except (ValueError,AssertionError) as e:
            print('Invalid Intial State')
        except IndexError as e:
            print('Enter Moves in correct Format')
        
    #     # End set initial state

    if gm==None:
        randoms,players = setGameMode(*getPlayers())
    else:
        randoms,players = setGameMode(*gm)
    winners  = np.empty(shape=(N),dtype=int)
    turns = np.empty(shape=(N),dtype=int)
    turn_times = [[],[]]
    # for n in range(N):
    for n in tqdm(range(N)):
        for i,r in enumerate(randoms):
            if r:
                players[i].set_seed(n+i+123456)
        while game.whoWins()==None and game.totalTurns()<64:
            turn = game.getTurn()
            
            if display:
                print()
                # print(game.state)
                # game.display(internal_display=True)
                game.display()
            turn = game.getTurn()
            if display: print(f"Player {turn+1}'s turn (Turn {game.totalTurns()})")
            
            current_player = players[turn]
            success=False
            K = 5
            for k in range(K):#while True
                try:
                    start = time.time()
                    move = current_player.getMove(game.getState(),display) #value error if invalid input format
                    
                    if isinstance(move, str) and move in {'u','r','replay','save'}:

                        # ensures repeated u/r/re does not trigger the auto game termination (parsed as valid move)
                        success=True

                        if move == 'u':
                            if game.undo():
                                print('\nUndo Successful')
                                game.display()
                                print(f"Player {turn+1}'s turn (Turn {game.totalTurns()})")
                                continue
                            else:
                                print('\nUndo Unsuccessful')
                                continue
                        elif move == 'r':
                            if game.redo():
                                print('\nRedo Successful')
                                game.display()
                                print(f"Player {turn+1}'s turn (Turn {game.totalTurns()})")
                                continue
                            else:
                                print('\nRedo Unsuccessful')
                                continue
                        elif move == 'replay':
                            print('Replaying Game until current turn')
                            game.replay()
                            continue
                        elif move == 'save':
                            filename = input('Enter filename: ')
                            game.save(filename)
                            continue

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
        winner = int(not game.getTurn())+1 if winner==None else winner+1
        winner = winner if game.totalTurns()<64 else 0
        winners[n] = winner
        turns[n] = game.totalTurns()

        if display: 
            game.display()

            if game.totalTurns()==64:
                print('Draw!')
            else:                
                print('Player',winner,'wins!')
                print('Total Turns',game.totalTurns())
        
        print()
        while True:
            menu = input("Menu:\n Replay Game (r)\n Save Game (s)\n Continue (any key)\n")
            print()

            if menu == 'r':
                print('Replaying Game')
                game.replay()
                continue
            elif menu == 's':
                filename = input('Enter filename: ')
                game.save(filename)
                continue
            else:
                break

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

    # # Play again?
    # while True:
    #     _,_,_ = play()
    #     cont = input('Play again? (y/n): ')
    #     if cont.lower() != 'y'.strip():
    #         break
    
    profiler.disable()
    
    stats = pstats.Stats(profiler)
    
    # Sort by 'time' (total time in each function) and print the top 10 functions
    stats.strip_dirs()  # Optional: remove long file paths for readability
    stats.sort_stats("time").print_stats(16)
    