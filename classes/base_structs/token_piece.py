from typing import Tuple

class token_piece():
    #dictionary with keys being initialization params, values being their respective possible assignments
    POSSIBLE_SETS = {'x':{1,2,3,4},'y':{1,2,3,4}}
    def __init__(self,x:int,y:int)->None:
        assert x in self.POSSIBLE_SETS['x'], f"Token initialization failed. {x} not in {self.POSSIBLE_SETS}"
        assert y in self.POSSIBLE_SETS['y'], f"Token initialization failed. {y} not in {self.POSSIBLE_SETS}"
        
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
    def __repr__(self):
        return f'({self.x} | {self.y})'
