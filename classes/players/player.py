from abc import ABC,abstractmethod
from classes.base_structs.action import packed_action
from classes.base_structs.gamestate import gamestate

class Player(ABC):

    def __init__(self,id:int):
        self.id = id
    
    @abstractmethod
    def getMove(self, game: gamestate,display:bool=False) -> packed_action:
        pass

    # example: for a human, the instructionKey could be s and the instruction would be the function to save the game
    # @abstractmethod
    # def instructionHandler(self, state:gamestate, display:bool=False):
    #     pass