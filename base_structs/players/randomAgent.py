
import random

from base_structs.player import Player
from base_structs.action import action
from game import Game

class Agent(Player):
    def getMove(self, game: Game) -> action:
        legal_moves = game.getLegalMoves(game.state)
        return random.choice(legal_moves) if legal_moves else None

