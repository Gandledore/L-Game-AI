from abc import ABC, abstractmethod
from base_structs.action import action
from game import Game
from players.agent import Agent
from players.human import Human
from players.randomAgent import RandomAgent

class Player:

    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def getMove(self, game: Game) -> action:
        pass


