import numpy as np

class L_piece():
    def compute_L_coords(self):
        p1 = np.array([self.x,self.y])
        p2 = p1 + self.direction_mapping[self.d]
        p3 = p1 + self.direction_mapping[self.d]*2
        p0 = p1 + self.direction_mapping[self.orientation_map[self.d][self.mirror]]
        return p0,p1,p2,p3
    
    def __init__(self,x:int,y:int,d:str,mirror:bool):
        self.x = x
        self.y = y
        self.d = d
        self.mirror = mirror
        
        self.direction_mapping = {
            'N':np.array([0,-1]),
            'E':np.array([1,0]),
            'S':np.array([0,1]),
            'W':np.array([-1,0])
        }
        self.orientation_map = {
            'N': ('E', 'W'),
            'E': ('S', 'N'),
            'S': ('W', 'E'),
            'W': ('N', 'S')
        }
        
        self.p0,self.p1,self.p2,self.p3 = self.compute_L_coords()