from typing import Tuple,Set

class token_piece():
    #dictionary with keys being initialization params, values being their respective possible assignments
    _POSSIBLE_LISTS = {'x':[1,2,3,4],'y':[1,2,3,4]}
    _POSSIBLE_SETS = {'x':{1,2,3,4},'y':{1,2,3,4}}
    
    def __init__(self,x:int,y:int)->None:
        assert x in token_piece._POSSIBLE_SETS['x'], f"Token x={x} not in {token_piece._POSSIBLE_SETS['x']}"
        assert y in token_piece._POSSIBLE_SETS['y'], f"Token y={y} not in {token_piece._POSSIBLE_SETS['y']}"
        
        self.x=x
        self.y=y
        
    def get_coords(self)->Set[Tuple[int,int]]:
        return set([(self.x,self.y)])
    
    def get_position(self)->Tuple[int,int]:
        return self.x,self.y
    
    def get_tuple(self)->Tuple[int,int]:
        return self.x,self.y
    
    def __eq__(self, other:'token_piece')->bool:
        return self.x==other.x and self.y==other.y
    def __lt__(self,value:int)->bool:
        return self.x<value and self.y<value
    def __gt__(self,value:int)->bool:
        return self.x>value and self.y>value
    def __repr__(self):
        return f'({self.x}, {self.y})'
    def __hash__(self):
        return hash((self.x,self.y))