import numpy as np
from typing import Tuple

class L_piece():
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
    
    def __init__(self,x:int,y:int,d:str):
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
        
        self.p0,self.p1,self.p2,self.p3 = self.compute_L_coords()
    
    def newPos(self,x:int,y:int,d:str):
        self.x = x
        self.y = y
        self.short_leg_direction = d
        
        if self.short_leg_direction in ['N','S']:
            self.long_leg_direction = self.orientation_map[self.short_leg_direction][x>2]
        elif self.short_leg_direction in ['E','W']:
            self.long_leg_direction = self.orientation_map[self.short_leg_direction][y>2]
        
        self.p0,self.p1,self.p2,self.p3 = self.compute_L_coords()
