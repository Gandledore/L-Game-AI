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
    return players

# change player from human to agent and take input
def changePlayer(player:Players.Player)->Players.Player:
    if isinstance(player,Players.Human):
        depth = int(input(f"Enter Depth (int or -1): "))
        prune = bool(int(input(f"Enter Prune (0 or 1): ")))
        return Players.Agent(player.id,depth,prune)
    return player

def loadGame() -> Optional[Game]:
    while True:
        load = input('Load Game? (y/n): ')
        if load.lower() == 'y':
            try:
                filename = input('Enter filename: ')
                return Game.load(filename)            
            except FileNotFoundError as e:
                print('File not found')
        else:
            return None
        
def create_game():
    while True:
        InitialStateCoordinates = input(f"Enter Initial State Coords [L1, L2, T1, T2] or Default: ")
        InitialStateCoordinatesList = InitialStateCoordinates.split()

        try:
            InitialStateCoordinatesList = InitialStateCoordinates.split()
            if len(InitialStateCoordinatesList) == 0:
                print('Using Default Initial Gamestate')
                game = Game()
            else:
                L1_x, L1_y, L1_d = int(InitialStateCoordinatesList[0]), int(InitialStateCoordinatesList[1]), InitialStateCoordinatesList[2]
                L2_x, L2_y, L2_d = int(InitialStateCoordinatesList[3]), int(InitialStateCoordinatesList[4]), InitialStateCoordinatesList[5]
                T1_x, T1_y = int(InitialStateCoordinatesList[6]), int(InitialStateCoordinatesList[7])
                T2_x, T2_y = int(InitialStateCoordinatesList[8]), int(InitialStateCoordinatesList[9])

                L_pieces = [L_piece(x=L1_x, y=L1_y, d=L1_d), L_piece(x=L2_x, y=L2_y, d=L2_d)]
                token_pieces = {token_piece(x=T1_x, y=T1_y), token_piece(x=T2_x, y=T2_y)}

                game = Game(L_pieces=L_pieces, token_pieces=token_pieces)

        except (ValueError,AssertionError) as e:
            print('Invalid Intial State')
            continue
        except IndexError as e:
            print('Enter Moves in correct Format')
            continue
        
        # print board to get confirmation from user that they want to use this board
        game.display()
        while True:
            confirm = input('Confirm this board? (y/n): ')
            if confirm.lower() == 'n':
                del game
                game = None
                break
            elif confirm.lower()=='y' or confirm.lower()=='':
                return game
            else:
                print("Please enter 'y' or 'n'")
def print_instructions():
    print("\n\n\
            Instructions:\n\
            Move: x y d t1x t1y t2x  t2y\n\
            Undo: undo\n\
            Redo: redo\n\
            Replay: replay\n\
            Save Game: save\n\
            Transform Board: 'x' or 'y' or 't' or 'cw' or 'ccw'\n\
            Have AI take over: swap\n\
            Display Instructions: help\n\
    \n\n")
def play(gm:Tuple[Tuple[int,Optional[int],Optional[int]],Tuple[int,Optional[int],Optional[int]]]=None,N:int=1,display=True)->Tuple[np.ndarray,np.ndarray,List[List[float]]]:

    game = loadGame()

    if game is None:
        game = create_game()

    if gm==None:
        players = setGameMode(*getPlayers())
    else:
        players = setGameMode(*gm)

    print_instructions()

    tie_end = 64
    while game.whoWins()==None and game.totalTurns()<tie_end:
        if display: game.display()
        
        turn = game.getTurn()
        if display: print(f"Player {turn+1}'s turn (Turn {game.totalTurns()})")
        
        current_player = players[turn]
        success=False
        K = 5
        for k in range(K):#while True
            try:
                instruction_type,instruction = current_player.instructionHandler(game.getState(),display) #value error if invalid input format

                if instruction_type == 'move':
                    game.apply_action(instruction)  #assertion error if invalid move
                elif instruction_type == 'view':
                    if instruction == 'replay':
                        print('\nReplaying Game until current turn')
                        game.replay()
                    elif isinstance(instruction,List) and len(instruction)==3:#not checking that elements are bool
                        game.state.update_denormalization(instruction)#bad practice
                elif instruction_type=='control':
                    if instruction == 'undo':
                        if game.undo():
                            print('\nUndo Successful\n')
                        else:
                            print('\nUndo Unsuccessful\n')
                    elif instruction == 'redo':
                        if game.redo():
                            print('\nRedo Successful\n')
                            game.display()
                        else:
                            print('\nRedo Unsuccessful\n')
                    elif instruction == 'save':
                        filename = input('Enter filename: ')
                        game.save(filename)
                    elif instruction == 'help':
                        print_instructions()
                elif instruction_type=='swap':
                    if instruction=='ai':
                        current_player = changePlayer(current_player)
                        players[turn] = current_player
                        print(f'Player {turn+1} changed to AI')
                else:
                    raise ValueError(f"Invalid instruction {instruction}.")
                success=True
                break
            
            # except ValueError as e:
            #     print(f'Invalid Input. {e}\n')
            except AssertionError as e:
                print(f'Invalid Move. {e}\n')

        if not success: #if no valid move provided after K attempts, kill game
            print(f'\n\nNo valid play after {K} moves. Game over.')
            break

    winner = game.whoWins()
    winner = int(not game.getTurn())+1 if winner==None else winner+1
    winner = winner if game.totalTurns()<tie_end else 0

    if display: 
        game.display()

        if game.totalTurns()==tie_end:
            print('Draw!')
        else:
            print('Player',winner,'wins!')
            print('Total Turns',game.totalTurns())
    
    while True:
        menu = input("\nMenu:\n Replay Game (r)\n Save Game (s)\n Continue (any key)\n\n")
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

    return winner
if __name__ == "__main__":
    
    # Keep Playing?
    while True:
        _ = play()
        cont = input('Play again? (y/n): ')
        if cont.lower() != 'y'.strip():
            break