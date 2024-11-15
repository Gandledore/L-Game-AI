
import random

from classes.players.player import Player
from classes.base_structs.action import action
from classes.base_structs.gamestate import gamestate

class RandomAgent(Player):
    def __init__(self, id):
        super().__init__(id)
    
    def getMove(self, state: gamestate) -> action:
        legal_moves = state.getLegalMoves(state.state)
        return random.choice(legal_moves) if legal_moves else None

