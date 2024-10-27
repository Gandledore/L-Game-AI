from typing import Tuple

class token_piece():
    def __init__(self,x:int,y:int)->None:
        self.x=x
        self.y=y
    def get_position(self)->Tuple[int,int]:
        return self.x,self.y