from abc import ABC, abstractmethod
from classes.base_structs.action import action
from classes.game import Game

class Player:

    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def getMove(self, game: Game) -> action:
        pass


