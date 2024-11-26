
import random

from classes.players.player import Player
from classes.base_structs.action import packed_action
from classes.base_structs.gamestate import gamestate


class RandomAgent(Player):
    def __init__(self, id, seed=-1):
        super().__init__(id)
        if seed!=-1:
            random.seed(seed)
        
    def getMove(self, state: gamestate,display:bool=False) -> packed_action:
        legal_moves = state.getLegalMoves()
        return random.choice(legal_moves)
    
    def set_seed(self,s):
        random.seed(s)