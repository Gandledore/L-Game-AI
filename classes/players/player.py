from abc import ABC,abstractmethod
from classes.base_structs.action import packed_action
from classes.base_structs.gamestate import gamestate

from typing import Tuple,Union,List
class Player(ABC):

    def __init__(self,id:int):
        self.id = id
    
    @abstractmethod
    def instructionHandler(self, state: gamestate, display:bool=False) -> Tuple[str,Union[packed_action,str,List[bool]]]:
        pass
    
    @abstractmethod
    def getMove(self, state: gamestate, display:bool=False) -> packed_action:
        pass  