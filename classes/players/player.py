from abc import ABC,abstractmethod
from classes.base_structs.action import action
from classes.base_structs.gamestate import gamestate

class Player(ABC):

    def __init__(self,id:int):
        self.id = id
    
    @abstractmethod
    def getMove(self, game: gamestate) -> action:
        pass
    

