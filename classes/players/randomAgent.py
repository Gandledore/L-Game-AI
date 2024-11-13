
import random

from classes.players.player import Player
from classes.base_structs.action import action
from classes.game import Game

class RandomAgent(Player):
    def getMove(self, game: Game) -> action:
        legal_moves = game.getLegalMoves(game.state)
        return random.choice(legal_moves) if legal_moves else None

