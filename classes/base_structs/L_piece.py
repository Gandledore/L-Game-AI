import numpy as np
from typing import Tuple
import sys

class L_piece():
    #dictionary with keys being initialization params, values being their respective possible assignments
    POSSIBLE_SETS = {'x':{1,2,3,4},'y':{1,2,3,4},'short_leg_direction':{'N','E','S','W'}}
    POSSIBLE_LISTS = {'x':[1,2,3,4],'y':[1,2,3,4],'short_leg_direction':['N','E','S','W']}
    
    def compute_L_coords(self)->Tuple[np.ndarray[int,int],
                                      np.ndarray[int,int],
                                      np.ndarray[int,int],
                                      np.ndarray[int,int]]:
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
        
        p1 = np.array([self.x,self.y])
        p0 = p1 + self.direction_mapping[self.short_leg_direction]
        
        p2 = p1 + self.direction_mapping[self.long_leg_direction]
        p3 = p1 + self.direction_mapping[self.long_leg_direction]*2
        return p0,p1,p2,p3
    
    def update_coords(self):
        self.coords = np.array(self.compute_L_coords())
    
    def __init__(self,x:int,y:int,d:str):
        assert x in L_piece.POSSIBLE_SETS['x'], f"L piece x={x} is not in {L_piece.POSSIBLE_SETS['x']}"
        assert y in L_piece.POSSIBLE_SETS['y'], f"L piece y={y} is not in {L_piece.POSSIBLE_SETS['y']}"
        assert d in L_piece.POSSIBLE_SETS['short_leg_direction'], f"L piece short_leg_direciton={d} is not in {L_piece.POSSIBLE_SETS['short_leg_direction']}"
        
        self.x = x
        self.y = y
        self.short_leg_direction = d
        
        self.direction_mapping = {
            'N':np.array([0,-1]),
            'E':np.array([1,0]),
            'S':np.array([0,1]),
            'W':np.array([-1,0])
        }
        self.orientation_map = {
            'N': ('E', 'W'),
            'E': ('S', 'N'),
            'S': ('E', 'W'),
            'W': ('S', 'N')
        }
        
        if self.short_leg_direction in ['N','S']:
            self.long_leg_direction = self.orientation_map[self.short_leg_direction][x>2]
        elif self.short_leg_direction in ['E','W']:
            self.long_leg_direction = self.orientation_map[self.short_leg_direction][y>2]
        
        self.update_coords()
    
    def get_coords(self)->np.ndarray:
        return self.coords
    
    def get_tuple(self)->Tuple[int,int,str]:
        return self.x,self.y,self.short_leg_direction
    
    def get_position(self)->Tuple[int,int]:
        return self.x,self.y
    
    def __eq__(self, other:'L_piece')->bool:
        return self.x==other.x and self.y==other.y and self.short_leg_direction==other.short_leg_direction
    
    def __lt__(self,value:int)->bool: #true if any are less than value
        return bool(np.sum(self.coords.flatten()<value))

    def __gt__(self,value:int)->bool: #true if any are greater than value
        return bool(np.sum(self.coords.flatten()>value))
    
    def __repr__(self):
        return f'({self.x}, {self.y}, {self.short_leg_direction})'
    
    def __hash__(self):
        return hash((self.x,self.y,self.short_leg_direction))