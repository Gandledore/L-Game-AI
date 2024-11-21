
import random

from classes.players.player import Player
from classes.base_structs.action import packed_action
from classes.base_structs.gamestate import gamestate

random.seed(0)

class RandomAgent(Player):
    def __init__(self, id):
        super().__init__(id)
        
    def getMove(self, state: gamestate) -> packed_action:
        legal_moves = state.getLegalMoves()
        return random.choice(legal_moves)
