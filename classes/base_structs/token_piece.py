from typing import Tuple,Set,List,Union

class token_piece():
    #dictionary with keys being initialization params, values being their respective possible assignments
    _POSSIBLE_LISTS = {'x':[1,2,3,4],'y':[1,2,3,4]}
    _POSSIBLE_SETS = {'x':{1,2,3,4},'y':{1,2,3,4}}
    _POSSIBLE_POS = {(x,y) for x in range(1,5) for y in range(1,5)} | {(0,0)}
    #possible spots for tokens representing no movement, because of transformations
    _NULL_SPOTS = {(0,0),(0,5),(5,0),(5,5)}
    
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
    
    #compare less than for either ints or another token (sorting)
    def __lt__(self,other:Union[int,"token_piece"])->bool:
        if isinstance(other, token_piece):
            #1.2 slightly prioritizes x by making y larger, so that all board spots are unique. 
            return self.x + 1.2*self.y < other.x + 1.2*other.y
        elif isinstance(other, int):
            return self.x < other and self.y<other
        else:
            raise NotImplementedError(f'Comparison of token and {type(other)} not supported')
        
    def __gt__(self,value:int)->bool:
        return self.x>value and self.y>value
    
    def __hash__(self):
        return hash((self.x,self.y))

    def reflect_x(self)->None:
        self.x = 5 - self.x
    
    def reflect_y(self)->None:
        self.y = 5 - self.y
    
    def transpose(self)->None:
        temp = self.x
        self.x = self.y
        self.y = temp
        
    def normalize(self,transform:List[bool]=None)->None:
        if transform[0]:
            self.reflect_x()
        if transform[1]:
            self.reflect_y()
        if transform[2]:
            self.transpose()
        