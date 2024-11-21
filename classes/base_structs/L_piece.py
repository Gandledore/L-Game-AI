import numpy as np
from typing import Tuple,Set
import sys

class L_piece():
    #dictionary with keys being initialization params, values being their respective possible assignments
    _POSSIBLE_SETS = {'x':{1,2,3,4},'y':{1,2,3,4},'d':{'N','E','S','W'}}
    _POSSIBLE_LISTS = {'x':[1,2,3,4],'y':[1,2,3,4],'d':['N','E','S','W']}
    _direction_mapping = {
        'N':np.array([0,-1]),
        'E':np.array([1,0]),
        'S':np.array([0,1]),
        'W':np.array([-1,0])
    }
    _orientation_map = {
        'N': ('E', 'W'),
        'E': ('S', 'N'),
        'S': ('E', 'W'),
        'W': ('S', 'N')
    }
    _l_coords = {}
    @classmethod
    def _compute_L_coords(cls,x,y,d)->Set[Tuple[int,int]]:
        """computes matrix coords of L piece
            matrix coords:
                upper left  : [1,1]
                top right   : [4,1]
                bottom left : [1,4]
                bottom right: [4,4]
            L coords example:
                
                | p1 | p2 | p3 |
                | p0 |
                
        Returns:
            Tuple of 4 ndarrays each containing 2 integers
        """
        if (x,y,d) not in cls._l_coords:
        
            p1 = np.array([x,y])
            p0 = p1 + cls._direction_mapping[d]
            
            if d in ['N','S']:
                ld = cls._orientation_map[d][x>2]
            elif d in ['E','W']:
                ld = cls._orientation_map[d][y>2]

            p2 = p1 + cls._direction_mapping[ld]
            p3 = p1 + cls._direction_mapping[ld]*2
            cls._l_coords[(x,y,d)] = set((tuple(p0),tuple(p1),tuple(p2),tuple(p3)))
        
        return cls._l_coords[(x,y,d)]
    
    def __init__(self,x:int=1,y:int=1,d:str='E'):
        assert x in L_piece._POSSIBLE_SETS['x'], f"L piece x={x} is not in {L_piece._POSSIBLE_SETS['x']}"
        assert y in L_piece._POSSIBLE_SETS['y'], f"L piece y={y} is not in {L_piece._POSSIBLE_SETS['y']}"
        assert d in L_piece._POSSIBLE_SETS['d'], f"L piece d={d} is not in {L_piece._POSSIBLE_SETS['d']}"
        
        self.x = x
        self.y = y
        self.d = d
        
        self.coords = L_piece._compute_L_coords(x,y,d)
    
    def get_coords(self)->Set[Tuple[int,int]]:
        return self.coords
    
    def get_tuple(self)->Tuple[int,int,str]:
        return self.x,self.y,self.d
    
    def get_position(self)->Tuple[int,int]:
        return self.x,self.y
    
    def __eq__(self, other:'L_piece')->bool:
        return self.x==other.x and self.y==other.y and self.d==other.d
    
    def __lt__(self,value:int)->bool: #true if any are less than value
        return any(x < value for tpl in self.coords for x in tpl)

    def __gt__(self,value:int)->bool: #true if any are greater than value
        return any(x > value for tpl in self.coords for x in tpl)
    
    def __repr__(self):
        return f'({self.x}, {self.y}, {self.d})'
    
    def __hash__(self):
        return hash((self.x,self.y,self.d))