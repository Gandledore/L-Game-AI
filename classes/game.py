import numpy as np
import copy

from classes.base_structs.gamestate import gamestate # imports as class 
from classes.base_structs.action import action

from typing import Union,List,Optional,Tuple
class Game:
    def __init__(self):
        self.state = gamestate()
        
    def getTurn(self)->int:
        return self.state.player
    
    def getState(self)->gamestate:
        return copy.deepcopy(self.state)
    
    #updates game state with action if it is valid, returns true iff successfuly
    #feedback passed through to valid moves
    def apply_action(self,move:action)->None:
        self.state = self.state.getSuccessor(move)
    
    #interface to display game board and pieces
    def display(self)->None:
        board = np.full((4, 4), "  ") # 4 by 4 of empty string
        
        for i,l in enumerate(self.state.L_pieces):
            for px, py in l.get_coords():
                board[py-1, px-1] = "L"+str(i+1)

        for i,t in enumerate(self.state.token_pieces):
            tx, ty = t.get_position()
            board[ty - 1, tx - 1] = "T"+str(i+1)


        rows = ["|" + "|".join(f"{cell:>2}" for cell in row) + "|" for row in board]
        #left wall then the row then the ending right wall
        # f"{cell:>2}" align cell to the right > with a width of 2 spaces. 

        horizontal_separator = "-------------\n"
        
        board_str = horizontal_separator + f"\n{horizontal_separator}".join(rows) + "\n" + horizontal_separator
        print(board_str)
        #checks who wins. Either None, 0 or 1
    
    #determines who wins, returns None, 0 or 1
    # made a copy of this in gamestate
    def whoWins(self)->Optional[int]:
        if self.state.isGoal():
            #winner is previous player
            #current player is stuck
            return int(not self.state.player)
        #game is not over
        return None
    
if __name__ == "__main__":
    print("run python3 play.py instead")
    test = Game()
    test.display()
    test.getInput()

    test.display()
    test.getInput()

        

