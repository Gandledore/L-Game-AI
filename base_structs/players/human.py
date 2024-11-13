from base_structs.player import Player
from base_structs.action import action
from game import Game

class Human(Player):
    def getMove(self, game: Game) -> action:
        return game.getInput()

