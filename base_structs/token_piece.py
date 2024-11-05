from typing import Tuple

class token_piece():
    def __init__(self,x:int,y:int)->None:
        self.x=x
        self.y=y
    def get_position(self)->Tuple[int,int]:
        return self.x,self.y
    def __eq__(self, other:'token_piece')->bool:
        return self.x==other.x and self.y==other.y
    def __lt__(self,value:int)->bool:
        return self.x<value and self.y<value
    def __gt__(self,value:int)->bool:
        return self.x>value and self.y>value