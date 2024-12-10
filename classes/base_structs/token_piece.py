from typing import Tuple,Set,List,Union
import numpy as np

class token_piece():
    __slots__ = ('x','y')
    #dictionary with keys being initialization params, values being their respective possible assignments
    _POSSIBLE_LISTS = {'x':[1,2,3,4],'y':[1,2,3,4]}
    _POSSIBLE_SETS = {'x':{1,2,3,4},'y':{1,2,3,4}}
    _NULL_SPOTS = {(0,0),(0,5),(5,0),(5,5)}
    _POSSIBLE_POS = {(x,y) for x in range(1,5) for y in range(1,5)} | _NULL_SPOTS
    #possible spots for tokens representing no movement, because of transformations
    
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
    
    def __repr__(self):
        return f'({self.x}, {self.y})'
        
    def __hash__(self):
        return hash((self.x,self.y))

    def copy(self):
        return token_piece(self.x,self.y)
    
    def reflect_x(self)->None:
        self.x = 5 - self.x
    
    def reflect_y(self)->None:
        self.y = 5 - self.y
    
    def transpose(self)->None:
        temp = self.x
        self.x = self.y
        self.y = temp
        
    def normalize(self,transform:np.ndarray[bool]=None)->None:
        if transform[0]:
            self.reflect_x()
        if transform[1]:
            self.reflect_y()
        if transform[2]:
            self.transpose()
    
    def denormalize(self,transform:np.ndarray[bool])->None:
        if transform[2]:
            self.transpose()
        if transform[1]:
            self.reflect_y()
        if transform[0]:
            self.reflect_x()