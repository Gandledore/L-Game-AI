import numpy as np
import copy

from classes.base_structs.gamestate import gamestate # imports as class 
from classes.base_structs.action import packed_action

from typing import Optional
class Game:
    def __init__(self, L_pieces=None, token_pieces=None):
        if L_pieces and token_pieces:
            self.state = gamestate(L_pieces=L_pieces, token_pieces=token_pieces)
        else: self.state = gamestate()
        self.turns = 0
        
    def getTurn(self)->int:
        return self.state.player
    
    def getState(self)->gamestate:
        return gamestate(self.state.player,self.state.L_pieces[:],self.state.token_pieces.copy(),self.state.transform[:])
    
    #updates game state with action if it is valid, returns true iff successfuly
    #feedback passed through to valid moves
    def apply_action(self,move:packed_action)->None:
        self.state = self.state.getSuccessor(move)
        self.turns+=1
        
    #interface to display game board and pieces
    def display(self,internal_display:bool=False)->None:
        board = np.full((4, 4), "  ", dtype=object) # 4 by 4 of empty string
        
        #denormalize to display what human expects to see
        if not internal_display: self.state.denormalize()
        
        for i, l in enumerate(self.state.L_pieces):
            color = "\033[1;31m1□\033[0m" if i == 0 else "\033[32m2▲\033[0m"  # Red for L1, Blue for L2
            for px, py in l.get_coords():
                board[py - 1, px - 1] = color #+ "L" + str(i + 1) + "\033[0m"
        
        for i, t in enumerate(self.state.token_pieces):
            tx, ty = t.get_position()
            board[ty - 1, tx - 1] = "\033[33m○○\033[0m"


        rows = ["|" + "|".join(f"{cell:>2}" for cell in row) + "|" for row in board]
        #left wall then the row then the ending right wall
        # f"{cell:>2}" align cell to the right > with a width of 2 spaces. 

        horizontal_separator = "-------------\n"
        
        board_str = horizontal_separator + f"\n{horizontal_separator}".join(rows) + "\n" + horizontal_separator
        print(board_str)
        
        #renormalize for internal use
        if not internal_display: self.state.normalize(self.state.transform)
    
    #determines who wins, returns None, 0 or 1
    # made a copy of this in gamestate
    def whoWins(self)->Optional[int]:
        return self.state.whoWins()
    
    def totalTurns(self)->int:
        return self.turns
    
    def reset(self)->None:
        self.state = gamestate()
        self.turns = 0
    
if __name__ == "__main__":
    print("run python3 play.py instead")
    test = Game()
    test.display()
    test.getInput()

    test.display()
    test.getInput()

        

