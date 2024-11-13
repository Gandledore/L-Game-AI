from classes.players.player import Player
from classes.base_structs.action import action
from classes.game import Game

class Agent(Player):
    def getMove(self, game: Game) -> action:
        legal_moves = game.getLegalMoves(game.state)
        return legal_moves[0] if legal_moves else None

