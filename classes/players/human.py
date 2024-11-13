from classes.players.player import Player
from classes.base_structs.action import action
from classes.game import Game

class Human(Player):
    def getMove(self, game: Game) -> action:
        return game.getInput()

