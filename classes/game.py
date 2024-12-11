import numpy as np
import time

from classes.base_structs.gamestate import gamestate # imports as class 
from classes.base_structs.action import packed_action

from typing import Optional
class Game:
    def __init__(self, L_pieces=None, token_pieces=None):
        if L_pieces and token_pieces:
            self.state = gamestate(L_pieces=L_pieces, token_pieces=token_pieces)
        else: 
            self.state = gamestate()
        
        self.turns = 0

        # List of moves for undoing and redoing
        self.history = []

        self.saveMove()
    
    def saveMove(self)->None:
        try:
            self.history[self.turns] = self.state
        except IndexError:
            self.history.append(self.state)
        self.turns+=1
    
    def undo(self) -> bool:

        if self.turns < 3:
            return False

        # undo -- this should go back to this players previous move
        self.turns -= 2
        self.state = self.history[self.turns-1]
        return True

    def redo(self) -> bool:
        if self.turns==len(self.history):
            return False
        self.turns += 2
        self.state = self.history[self.turns-1]
        return True
        
    def replay(self) -> None:
        for i in range(self.turns):
            self.history[i].display()
            time.sleep(1)
    def getTurn(self)->int:
        return self.state.player
    
    def getState(self)->gamestate:
        return gamestate(self.state.player,
                        self.state.L_pieces[:],
                        self.state.token_pieces.copy(),
                        self.state.transform[:])
    
    #updates game state with action if it is valid, returns true iff successfuly
    #feedback passed through to valid moves
    def apply_action(self,move:packed_action)->None:
        self.state = self.state.getSuccessor(move)
        self.saveMove()
        
    #interface to display game board and pieces
    def display(self,internal_display:bool=False)->None:
        self.state.display(internal_display=internal_display)
    
    #determines who wins, returns None, 0 or 1
    # made a copy of this in gamestate
    def whoWins(self)->Optional[int]:
        return self.state.whoWins()
    
    def totalTurns(self)->int:
        return self.turns
    
    def reset(self)->None:
        self.history.clear()

        self.turns = 0
        self.state = gamestate()
        self.saveMove()
