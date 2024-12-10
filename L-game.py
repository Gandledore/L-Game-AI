import sys
import subprocess
import time

# profiling (built in?)
# import cProfile
# import pstats

# Package install routine

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def install_all():

    install('numpy')
    install('tqdm')

try:
    import numpy as np
    from tqdm import tqdm
except ImportError:
    install_all()

# End package install routine


import struct

from typing import Tuple
import numpy as np

class packed_action:
    __slots__ = ('data',)
    _format = '3B c 4B'

    def __init__(self, l_piece_id:int=0, new_l_pos:Tuple[int,int,str]=(1, 3, 'S'), current_token_pos:Tuple[int,int]=(1,1), new_token_pos:Tuple[int,int]=(3, 1)):
        assert l_piece_id in {0,1},f"action L_id={l_piece_id} not in {0,1}"
        assert current_token_pos in token_piece._POSSIBLE_POS,f"action current_t_pos={current_token_pos} not in {token_piece._POSSIBLE_POS}"
        assert new_token_pos in token_piece._POSSIBLE_POS,f"action current_t_pos={new_token_pos} not in {token_piece._POSSIBLE_POS}"
        assert new_l_pos[0] in L_piece._POSSIBLE_SETS['x'], f"action Lx={new_l_pos[0]} not in {L_piece._POSSIBLE_SETS['x']}"
        assert new_l_pos[1] in L_piece._POSSIBLE_SETS['y'], f"action Lx={new_l_pos[0]} not in {L_piece._POSSIBLE_SETS['y']}"
        assert new_l_pos[2] in L_piece._POSSIBLE_SETS['d'], f"action Lx={new_l_pos[0]} not in {L_piece._POSSIBLE_SETS['d']}"
        
        self.data = struct.pack(packed_action._format, 
                                 l_piece_id, new_l_pos[0], new_l_pos[1], new_l_pos[2].encode('utf-8'), 
                                 current_token_pos[0], current_token_pos[1],
                                 new_token_pos[0], new_token_pos[1])

    def get_rep(self):
        return struct.unpack(packed_action._format, self.data)
    def __hash__(self):
        return hash(self.data)
    def __eq__(self, other):
        return self.data == other.data
    def __repr__(self):
        unpacked = struct.unpack(packed_action._format,self.data)
        return f'({unpacked[0]},({unpacked[1]},{unpacked[2]},{unpacked[3].decode('utf-8')}),({unpacked[4]},{unpacked[5]}),({unpacked[6]},{unpacked[7]}))'
    
    def suggest_format(self):
        unpacked = struct.unpack(packed_action._format,self.data)
        return f"{unpacked[1]} {unpacked[2]} {unpacked[3].decode('utf-8')} " + (f"{unpacked[4]} {unpacked[5]} {unpacked[6]} {unpacked[7]}" if unpacked[4] != 0 else f"")
    
    def normalize(self,transform:np.ndarray[bool])->None:
        l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, curr_token_pos_x, curr_token_pos_y, new_token_pos_x,new_token_pos_y = struct.unpack(packed_action._format,self.data)
        new_l_pos_d = new_l_pos_d.decode('utf-8')
        
        #reflect x
        if transform[0]:
            new_l_pos_x = 5 - new_l_pos_x
            if curr_token_pos_x != 0:
                curr_token_pos_x = 5 - curr_token_pos_x
                new_token_pos_x = 5 - new_token_pos_x
            new_l_pos_d = L_piece._reflection_map[new_l_pos_d] if new_l_pos_d in ['E','W'] else new_l_pos_d
        
        #reflect y
        if transform[1]:
            new_l_pos_y = 5 - new_l_pos_y
            if curr_token_pos_y != 0:
                # print("if ther is  token move")
                curr_token_pos_y = 5 - curr_token_pos_y
                new_token_pos_y = 5 - new_token_pos_y
            new_l_pos_d = L_piece._reflection_map[new_l_pos_d] if new_l_pos_d in ['N','S'] else new_l_pos_d
        
        #transpose
        if transform[2]:
            new_l_pos_d = (L_piece._transpose_map[new_l_pos_d])
            
            temp = new_l_pos_x
            new_l_pos_x = new_l_pos_y
            new_l_pos_y = temp
            
            temp = curr_token_pos_x
            curr_token_pos_x = curr_token_pos_y
            curr_token_pos_y = temp
            
            temp = new_token_pos_x
            new_token_pos_x = new_token_pos_y
            new_token_pos_y = temp
        
        #save transformed data
        self.data = struct.pack(packed_action._format,
                                l_piece_id,new_l_pos_x,new_l_pos_y,new_l_pos_d.encode('utf-8'),
                                curr_token_pos_x,curr_token_pos_y,
                                new_token_pos_x,new_token_pos_y)
        
    def denormalize(self,transform:np.ndarray[bool])->None:
        l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, curr_token_pos_x, curr_token_pos_y, new_token_pos_x,new_token_pos_y = struct.unpack(packed_action._format,self.data)
        new_l_pos_d = new_l_pos_d.decode('utf-8')
        
        #transpose
        if transform[2]:
            new_l_pos_d = (L_piece._transpose_map[new_l_pos_d])
            
            temp = new_l_pos_x
            new_l_pos_x = new_l_pos_y
            new_l_pos_y = temp
            
            temp = curr_token_pos_x
            curr_token_pos_x = curr_token_pos_y
            curr_token_pos_y = temp
            
            temp = new_token_pos_x
            new_token_pos_x = new_token_pos_y
            new_token_pos_y = temp
        
        #reflect y
        if transform[1]:
            new_l_pos_y = 5 - new_l_pos_y
            curr_token_pos_y = 5 - curr_token_pos_y
            new_token_pos_y = 5 - new_token_pos_y
            new_l_pos_d = L_piece._reflection_map[new_l_pos_d] if new_l_pos_d in ['N','S'] else new_l_pos_d
        
        #reflect x
        if transform[0]:
            new_l_pos_x = 5 - new_l_pos_x
            curr_token_pos_x = 5 - curr_token_pos_x
            new_token_pos_x = 5 - new_token_pos_x
            new_l_pos_d = L_piece._reflection_map[new_l_pos_d] if new_l_pos_d in ['E','W'] else new_l_pos_d

        #save transformed data
        self.data = struct.pack(packed_action._format,
                                l_piece_id,new_l_pos_x,new_l_pos_y,new_l_pos_d.encode('utf-8'),
                                curr_token_pos_x,curr_token_pos_y,
                                new_token_pos_x,new_token_pos_y)
                                
                                
                                
                                
                                
                                
                                
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
            
            
            
            
            
            
import numpy as np
from typing import Tuple,Set,List

class L_piece():
    __slots__ = ('x','y','d')
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
    _transpose_map = {
        'N': 'W',
        'W': 'N',
        'S': 'E',
        'E': 'S'
    }
    _reflection_map = {
        'N': 'S',
        'S': 'N',
        'W': 'E',
        'E': 'W'
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
    
    def get_coords(self)->Set[Tuple[int,int]]:
        return L_piece._compute_L_coords(self.x,self.y,self.d)
    
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
    
    def copy(self):
        return L_piece(self.x,self.y,self.d)
    
    def __repr__(self):
        return f'({self.x}, {self.y}, {self.d})'
    
    def __hash__(self):
        return hash((self.x,self.y,self.d))
    
    def reflect_x(self)->None:
        self.x = 5 - self.x
        self.d = L_piece._reflection_map[self.d] if self.d in ['E','W'] else self.d
    
    def reflect_y(self)->None:
        self.y = 5 - self.y
        self.d = L_piece._reflection_map[self.d] if self.d in ['N','S'] else self.d
    
    def transpose(self)->None:
        temp = self.x
        self.x = self.y
        self.y = temp
        
        self.d = L_piece._transpose_map[self.d]

    def compute_normalization(self)->np.ndarray[bool]:
        return np.array([self.x>2, self.y>2, self.d in ['E', 'W']])
    
    def normalize(self,transform:np.ndarray[bool])->None:
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
            
            
            
            
            
            
import pickle
import numpy as np

from typing import Union,List,Optional,Tuple,Set
from tqdm import tqdm

class gamestate():
    __slots__ = ('player','L_pieces','token_pieces','transform','token_pair_id')
    #precompute with static stuff
    _general_L_pos = []     #list of L positions that are generally possible (assuming no other pieces present)
    _general_T_pos = []     #list of T positions that are generally possible (assuming no other pieces present)
    _legalMoves = {}        #dictionary mapping states to numpy list of legal actions
    _legalMoves_path = 'legal_moves.pkl' #relative to play file
    
    #0=nothing, 1=processing legal moves, 2=done preprocessing
    _preprocessing_done = 0
    
    _board = {(x,y) for x in range(1,5) for y in range(1,5)}        #set of tuples of valid board coords

    #normalized state defined as L1 piece in upper left quadrant (x,y)<=2, long leg east (6 total possible tuples)
    _normalized_L_tuples = [(x,y,d) for x in range(1,3) for y in range(1,3) for d in ['N','S'] if not (y==1 and d=='N')]
    
    #horizontal initial state
    # def __init__(self,
    #                 player:int=0,
    #                 L_pieces:List[L_piece]=[L_piece(x=1,y=3,d='N'),L_piece(x=4,y=2,d='S')],
    #                 token_pieces:Set[token_piece]={token_piece(x=1,y=1),token_piece(x=4,y=4)},
    #                 transform:np.ndarray[bool]=np.array([False,False,False])):
    
    #vertical initial state
    def __init__(self, 
                    player:int=0,
                    L_pieces:List[L_piece]=[L_piece(x=2,y=4,d='E'),L_piece(x=3,y=1,d='W')],
                    token_pieces:Set[token_piece]={token_piece(x=1,y=1),token_piece(x=4,y=4)},
                    transform:np.ndarray[bool]=np.array([False,False,False])):
        
        
        self.player:int = player
        self.L_pieces: List[L_piece] = L_pieces
        self.token_pieces: Set[token_piece] = token_pieces
        self.transform = transform
        self.renormalize()


        #compute a unique token id for hashing the set of tokens. gives a unique binary number for each cell, such that summing any pair is also unique
        self.token_pair_id = sum(1 << (token.x+4*token.y) for token in self.token_pieces)
        
        #preprocessing
        if gamestate._preprocessing_done==0: #(do not run if preprocessing legal moves is currently running, or if it is completely done)
            gamestate._precompute_gen_L_pos()
            gamestate._precompute_gen_T_pos()

            gamestate._preprocessing_done = 1    
            #preprocessing legal moves started
            #this is necessary because otherwise preprocess_all_legalMoves recursively creates gamestates

            gamestate._preprocess_all_legalMoves()
            gamestate._preprocessing_done = 2


        #trust that preprocess_all_legal moves only generates valid gamestates.
        # this is for checking that provided initial state is correct.
        if gamestate._preprocessing_done==2:
            assert self in gamestate._legalMoves, "Invalid Gamestate"

    #precompute L positions that are generally possible, 
    # assuming no other pieces on the board (ie within board)
    @classmethod
    def _precompute_gen_L_pos(cls):
        for x in L_piece._POSSIBLE_LISTS['x']:
            for y in L_piece._POSSIBLE_LISTS['y']:
                for d in L_piece._POSSIBLE_LISTS['d']:
                    l = L_piece(x=x,y=y,d=d)
                    if cls._withinBoard(l):
                        cls._general_L_pos.append((x,y,d))

    #precompute T positions that are generally possible, 
    # assuming no other pieces on board (ie within board)
    @classmethod
    def _precompute_gen_T_pos(cls):
        for x in token_piece._POSSIBLE_LISTS['x']:
            for y in token_piece._POSSIBLE_LISTS['y']:
                cls._general_T_pos.append((x,y))#don't need to check within board, cause they are size 1x1
                
    #returns true if piece is entirely within board
    @classmethod
    def _withinBoard(cls,piece:Union[L_piece, token_piece])->bool:
        return piece.get_coords() <= cls._board
    
    #computes all legal moves for a given state, saves it to gamestate._legalMoves
    @classmethod 
    def _compute_legalMoves(cls,state:"gamestate"):
        #create list of possible actions
        validActions = []
        for Lpos in cls._general_L_pos:                                                 #possible positions L can move in general
            #consider not moving tokens only once per possible l move  
            #consider not moving first because this checks if L move is even possible                  
            move = packed_action(state.player, Lpos, (0,0), (0,0))
            if state.valid_move(move)[0]:
                validActions.append(move)
                
                #if L piece fails, no point trying tokens
                #sorting tokens so that it is consistent order (only necessary for repeatability)
                # tokens = sorted(list(state.token_pieces))
                for token in state.token_pieces:
                    token_pos = token.get_position()
                    for Tpos in cls._general_T_pos:
                        if (Tpos != token.get_position()):                                   #only consider actually moving the token.
                            move = packed_action(state.player, Lpos, token_pos, Tpos)
                            if (state.valid_move(move)[0]):                                  #only add it if its valid
                                validActions.append(move)
        
        cls._legalMoves[state] = np.array(validActions)
    
    #calls _compute_legalMoves for all normalized states (4592)
    @classmethod 
    def _preprocess_all_legalMoves(cls)->None:
        """saves a dictionary mapping any state to a list of the legal moves from that state

            generates all possible states by iterating throough all valid L1 placements
                all valid L2 placements given the L1 position, all valid T1 positions
                given L1 and L2, all valid T2 positions given L1,L2 and T1, 
                and both player turns given the rest

        Returns:
            None
        """
        try:
            with open(cls._legalMoves_path,'rb') as f:
                print('Loading Preprocessed States...',end='',flush=True)
                cls._legalMoves = pickle.load(f)
                print('\rLoaded Preprocessed States    ')
        except FileNotFoundError as e:
            print('Legal Moves not Preprocessed. Processing them now...')
            for l0_pos in tqdm(cls._normalized_L_tuples):
                l0_set = L_piece._compute_L_coords(*l0_pos)
                l0 = L_piece(*l0_pos)
                for l1_pos in cls._general_L_pos:
                    l1_set = L_piece._compute_L_coords(*l1_pos)
                    if not l0_set & l1_set:
                        l1 = L_piece(*l1_pos)
                        for i,t0_pos in enumerate(cls._general_T_pos):
                            if not (t0_pos in l0_set or t0_pos in l1_set):
                                t0 = token_piece(*t0_pos)
                                for j,t1_pos in enumerate(cls._general_T_pos):
                                    if j>i:     #consider only unique pairs of token positions
                                        if not (t1_pos in l0_set or t1_pos in l1_set):
                                            t1 = token_piece(*t1_pos)
                                            for p in [0,1]:
                                                #consider each player as a different state
                                                state = gamestate(p,[l0,l1],{t0,t1})
                                                cls._compute_legalMoves(state)
            
            #save legal moves since not already saved
            with open(cls._legalMoves_path,'wb') as f:
                print('Saving Legal Moves...',end='',flush=True)
                pickle.dump(cls._legalMoves,f)
                print('\rSaved Legal Moves')
        
    def __repr__(self):
        return f"Player: {self.player}\nL pieces: {self.L_pieces}\nT pieces: {self.token_pieces}\nTransform:{self.transform}"
    def __hash__(self):
        return hash((self.player,*self.L_pieces[0].get_tuple(),*self.L_pieces[1].get_tuple(),self.token_pair_id))
    
    #ignore transform equality so that different unormalized states evaluate as equal when equal normalized
    def __eq__(self,other:"gamestate"):
        return self.token_pair_id==other.token_pair_id and self.player==other.player and self.L_pieces==other.L_pieces
    
    def compute_normalization(self)->np.ndarray[bool]:
        return self.L_pieces[0].compute_normalization()
    
    def update_normalization(self,transform:np.ndarray[bool])->None:
        #if previous state was transposed, swap partial transform reflect x and reflect y to compensate cause that's what transpose does
        if self.transform[2] and transform[0]!=transform[1]:
            transform[:2] = np.logical_not(transform[:2])
            
        #take xor between states because doing something twice cancels it
        self.transform = np.logical_xor(self.transform,transform)
        
    def normalize(self,transform):        
        #normalize the L pieces
        for piece in self.L_pieces:
            piece.normalize(transform)
        
        #'or' comprehension necessary because 
        #   1) normalize returns none, then 'or piece' uses new version
        #   2) modifying elements in a set in place changes hash and results in unexpected behavior
        self.token_pieces = {piece.normalize(transform) or piece for piece in self.token_pieces}
        self.token_pair_id = sum(1 << (token.x+4*token.y) for token in self.token_pieces)

    #reverses normalization with same transpose
    def denormalize(self)->None:
        #normalize the L pieces
        for piece in self.L_pieces:
            piece.denormalize(self.transform)
        
        #'or' comprehension necessary because 
        #   1) normalize returns none
        #   2) modifying elements in a set in place changes hash and results in unexpected behavior
        self.token_pieces = {piece.denormalize(self.transform) or piece for piece in self.token_pieces}
        self.token_pair_id = sum(1 << (token.x+4*token.y) for token in self.token_pieces)

    #computes transformation necessary to get state that was just moved out of normalized space back to normalized space
    #normalizes state accordingly
    #updates transform with partial transform, to display correctly
    def renormalize(self)->None:
        partial_transform = self.compute_normalization()
        self.normalize(partial_transform)
        self.update_normalization(partial_transform)
            
    #returns list of legal actions for current player
    def getLegalMoves(self)->List[packed_action]:
        try:
            return gamestate._legalMoves[self]
        except KeyError:
            gamestate._compute_legalMoves(self)
            return gamestate._legalMoves[self]

    #return True if valid move, False if invalid
    #feedback to for assertions statements describing first error that's invalid
    def valid_move(self,move:packed_action)->Tuple[bool,str]:

        #unpack the move
        l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, curr_token_pos_x, curr_token_pos_y, new_token_pos_x,new_token_pos_y = move.get_rep()
        new_l_pos = (new_l_pos_x,new_l_pos_y,new_l_pos_d.decode('utf-8'))
        curr_t_pos = (curr_token_pos_x,curr_token_pos_y)
        new_t_pos = (new_token_pos_x,new_token_pos_y)

        #check moved l piece was actually moved
        if new_l_pos==self.L_pieces[l_piece_id].get_tuple():
            return False, 'L piece not moved.'
        
        # turn coords of l pieces into sets to check overlap quickly
        new_l_set = L_piece._compute_L_coords(*new_l_pos)
        current_L_other_set = self.L_pieces[not l_piece_id].get_coords()
        
        #check l pieces don't collide
        if new_l_set & current_L_other_set:
            return False, "L pieces overlap."
        
        #check that moved l piece intersects with neither current token (because L piece moves first)
        #already know other token doesn't collide with other l
        current_token_pos = {token.get_position() for token in self.token_pieces}
        if current_token_pos & new_l_set:
            return False, f'Moved L piece collides with token(s)'
        
        #check moved l piece is inside game board
        if not new_l_set <= gamestate._board:
            return False, "L piece not in game board."
        
        #null spots are corners outside board ({0,5},{0,5}) (not just (0,0) because of transforms)
        if curr_t_pos not in token_piece._NULL_SPOTS:
            if curr_t_pos not in current_token_pos:
                return False, f'No Token at {curr_t_pos}.'
            
            #check if moved token collides with new l pos or other l piece
            if new_t_pos in new_l_set:
                return False, f"Moved token collides with L{l_piece_id+1} piece."
            if new_t_pos in current_L_other_set:
                return False, f"Moved token collides with L{int(not l_piece_id)+1} piece."
            
            #check token isn't moved onto other token
            if new_t_pos in current_token_pos:
                return False, "Token moved onto other token."
            
        return True, "valid move"
    
    #take state and move, return new gamestate where move is applied
    def getSuccessor(self, move: packed_action) -> "gamestate":
        valid, feedback = self.valid_move(move)
        assert valid, feedback
        
        #unpack move
        l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, curr_token_pos_x, curr_token_pos_y, new_token_pos_x,new_token_pos_y = move.get_rep()
        new_l_pos = (new_l_pos_x,new_l_pos_y,new_l_pos_d.decode('utf-8'))
        curr_t_pos = (curr_token_pos_x,curr_token_pos_y)
        new_t_pos = (new_token_pos_x,new_token_pos_y)
        
        #generate a new state, copy old position if not modified by move
        state = gamestate(player=int(not self.player),
                        L_pieces=[L_piece(*new_l_pos) if self.player==i else l_piece.copy() for i,l_piece in enumerate(self.L_pieces)],
                        token_pieces={token_piece(*new_t_pos) if curr_t_pos==token.get_position() else token.copy() for token in self.token_pieces},
                        transform=self.transform.copy())
        
        #only renormalize when L1 moved
        # because moving L2 doesn't change normalization 
        #  because (normalization defined by L1)
        if self.player==0:
            state.renormalize()
        return state
    
    #checks state is goal
    def isGoal(self)->bool:
        #game over when no legal moves available
        return len(self.getLegalMoves())==0
    
    def whoWins(self)->Optional[int]:
        if self.isGoal():
            #winner is previous player
            #current player is stuck
            return int(not self.player)
        #game is not over
        return None
    

    


from abc import ABC,abstractmethod

class Player(ABC):

    def __init__(self,id:int):
        self.id = id
    
    @abstractmethod
    def getMove(self, game: gamestate,display:bool=False) -> packed_action:
        pass
    


import random

class RandomAgent(Player):
    def __init__(self, id, seed=-1):
        super().__init__(id)
        if seed!=-1:
            random.seed(seed)
        
    def getMove(self, state: gamestate,display:bool=False) -> packed_action:
        legal_moves = state.getLegalMoves()
        move = random.choice(legal_moves)
        move.denormalize(state.transform)
        print(f"Random Agent played {move}")
        move.normalize(state.transform)
        return random.choice(legal_moves)
    
    def set_seed(self,s):
        random.seed(s)
    def game_reset(self):
        pass
    
    
    
    
class Human(Player):
    _CORE = {(2,2), (2,3), (3,2), (3,3)}
    _CORNERS = {(1,1), (1,4), (4,1), (4,4)}
    _KILLER_TOKENS = {(2,1), (3,1), (1,2), (1,3), (4,2), (4,3), (2,4), (3,4)}
    _heuristics = {}

    def __init__(self,id:int):
        super().__init__(id)
    
    def heuristic(self, state:gamestate) -> int:
        player = self.id
        opponent = int(not self.id)
        flip_factor = 2*int(player == state.player) - 1 #1 if my turn, -1 if opponent's turn

        options_weight = 1
        core_weight = 25
        corner_weight = 40
        win_weight = 1000

        #penalize number of moves other person has
        control_options = flip_factor * options_weight * len(state.getLegalMoves()) #state is already the other player, just call getLegalMoves
        
        player_l_set = state.L_pieces[player].get_coords()
        opponent_l_set = state.L_pieces[opponent].get_coords()
        
        control_core = core_weight * len(player_l_set & Human._CORE)           #reward controlling core
        expel_core = -1*core_weight * len(opponent_l_set & Human._CORE)        #penalize oponent in core
        avoid_corner = -1*corner_weight * len(player_l_set & Human._CORNERS)   #penalize touching corner
        force_corner = corner_weight * len(opponent_l_set & Human._CORNERS)    #reward oponent being in corner

        #negative flip because if state is goal, current player lost. 
        # flip is +1 when its agent's turn, but want to penalize losing
        winning = -1*flip_factor*win_weight * state.isGoal() #colinear with legalmovesofother

        score = control_options + control_core + expel_core + avoid_corner + force_corner + winning
        return score
    

    #interface for a play code to get human input
    def getMove(self, state: gamestate, display:bool=True) -> packed_action:

        if display: print('Valid Moves:',len(state.getLegalMoves()))
        
        bestVal = float('-inf')
        bestMove = None
        for suggestmove in state.getLegalMoves(): # i htink the iseu is the moves are normalized moves...
            successor = state.getSuccessor(suggestmove)
            v = self.heuristic(successor)
            if v>bestVal:
                bestVal = v
                bestMove = suggestmove
        bestMove.denormalize(state.transform)
        print("Suggested Move: ", bestMove.suggest_format())
        bestMove.normalize(state.transform)
        
        # print('\nRecieved State:',state)
        wholeMoves = input(f"Player {state.player+1}: Enter xl1 yl1 dl1 tx ty tx ty: ")
        move_parts = wholeMoves.split()
        
        if len(move_parts)==0:
            move = bestMove
        
        elif ( (len(move_parts) != 7) and (len(move_parts) != 3) ):
            raise ValueError("Enter commands in specified format")
        else:
            #raises value error if can't cast to int
            try:
                new_l_pos = (int(move_parts[0]), int(move_parts[1]),move_parts[2])
            except ValueError as e:
                raise ValueError('Use integers for xl1 yl1')
            
            if len(move_parts)==7:
                try:
                    current_token_pos = (int(move_parts[3]), int(move_parts[4]))
                    new_token_pos = (int(move_parts[5]), int(move_parts[6]))
                except ValueError as e:
                    raise ValueError('Use integers for token locations')
                
            elif len(move_parts)==3:
                current_token_pos=(0,0)
                new_token_pos = (0,0)
        
            move = packed_action(l_piece_id=state.player,new_l_pos=new_l_pos,current_token_pos=current_token_pos,new_token_pos=new_token_pos)
            move.normalize(state.transform)
        return move
    def game_reset(self):
        pass
    
    
    
    
    

from typing import Tuple
import time
import numpy as np
import pickle

class Agent(Player):

    # Constants for heuristic

    _CORE = {(2,2), (2,3), (3,2), (3,3)}
    _CORNERS = {(1,1), (1,4), (4,1), (4,4)}
    _KILLER_TOKENS = {(2,1), (3,1), (1,2), (1,3), (4,2), (4,3), (2,4), (3,4)}
    _optimal_moves_path = 'optimal_moves'
    
    def __init__(self, id:int, depth=-1, prune:bool=False):
        super().__init__(id)
        
        self.display=False
        self.depth = depth
        if depth<0: self.prune = False
        else: self.prune = bool(prune)
        # TRANSPOSITION TABLE
        # check bugs here (saving depth it solved to)
        # <1 = assuming fully solved, may not be correct assumption
        # stores all moves of equivalent value
        self.finished = {} #stores state:(d,v) tuple of depth and best backpropagated value of highest depth search (-1 = infinite depth)
        self.check_tie_depth = 11#min(depth,11)%12 #look >5 ply ahead, cause according to wikipedia, you can avoid losing if you look 5 steps ahead
        # how to check ties: if encounter a looped state or a state we've already seen, say hey we've already seen this state, potentially a tie, then depth limited search starting from depth 11 because wikipedia says a player can win in 4 turns (check assumption)
        # in the next 11 turns, can a win or loss be forced? backtrack
        self.last = 0
        # not actually the max score, a lazy approximation of it (did not want to compute max score)
        # if the |score| is >900 consider a forced terminal state
        # forced = one player can win no matter what the opponent plays -> can force a terminal state
        self.max_score = 900
        self.played_states = {}
        if self.depth<0:self.preprocess_optimal_moves(gamestate(player=self.id))
    
    def preprocess_optimal_moves(self,state):
        solved_path = Agent._optimal_moves_path+'_id'+str(self.id)+'.pkl'
        try:
            with open(solved_path,'rb') as f:
                print('Loading Solved Game...',end='')
                self.finished = pickle.load(f)
                print('\rLoaded Solved Game    ')
        except FileNotFoundError:
            print('Game not Solved. Solving game now...')
            _,_ = self.AlphaBetaSearch(state)
            
            with open(solved_path,'wb') as f:
                print('Saving Optimal Moves...',end='')
                pickle.dump(self.finished,f)
                print('\rSaved Optimal Moves    ')
            
    def getMove(self, state: gamestate,display:bool=False) -> packed_action:
        self.display=display
        if self.display: 
            print('Thinking...')
            # print(len(state.getLegalMoves()))
        start = time.time()
        value, bestActions = self.AlphaBetaSearch(state)
        end = time.time()
        try:
            attempt = self.played_states[state]
        except KeyError:
            attempt = 0
            self.played_states[state]=0
        self.played_states[state]+=1
        
        bestAction = bestActions[attempt%len(bestActions)]
        
        if self.display:
            print(f'Finished MinMaxing {len(self.finished)} states')
            bestAction.denormalize(state.transform)
            # print(f'Choosing Move:{bestAction} for value: {value} from depth {self.finished[state][0]} out of {len(bestActions)} options')
            print(f'Choosing Move:{bestAction} for value: {value}')
            bestAction.normalize(state.transform)
            print(f'Time: {end-start:.1f}s | Pruned: {100*self.num_prune/self.max_prune:.1f}% ({self.num_prune}/{self.max_prune})')
        return bestAction
    
    def action_heuristic(self,move:packed_action)->int:
        core_weight = 20
        corner_weight = 40
        killer_token_weight = 10
        
        l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, curr_token_pos_x, curr_token_pos_y, new_token_pos_x,new_token_pos_y = move.get_rep()
        new_l_pos = (new_l_pos_x,new_l_pos_y,new_l_pos_d.decode('utf-8'))
        curr_t_pos = (curr_token_pos_x,curr_token_pos_y)
        new_t_pos = (new_token_pos_x,new_token_pos_y)
        
        l_set = L_piece._compute_L_coords(*new_l_pos)

        control_core = core_weight * len(l_set & Agent._CORE)           #reward controlling core
        avoid_corner = -1*corner_weight * int(bool(l_set & Agent._CORNERS))   #penalize touching corner
        killer_token = killer_token_weight * int(new_t_pos in Agent._KILLER_TOKENS if curr_t_pos!=(0,0) else 0) #reward placing tokens in killer positions
        
        return control_core + avoid_corner + killer_token
    
    def heuristic(self, state:gamestate) -> int:
        player = self.id
        opponent = int(not self.id)
        flip_factor = 2*int(player == state.player) - 1 #1 if my turn, -1 if opponent's turn

        options_weight = 1
        core_weight = 25
        corner_weight = 40
        win_weight = 1000

        #penalize number of moves other person has
        control_options = flip_factor * options_weight * len(state.getLegalMoves()) #state is already the other player, just call getLegalMoves
        
        player_l_set = state.L_pieces[player].get_coords()
        opponent_l_set = state.L_pieces[opponent].get_coords()
        
        control_core = core_weight * len(player_l_set & Agent._CORE)           #reward controlling core
        expel_core = -1*core_weight * len(opponent_l_set & Agent._CORE)        #penalize oponent in core
        avoid_corner = -1*corner_weight * len(player_l_set & Agent._CORNERS)   #penalize touching corner
        force_corner = corner_weight * len(opponent_l_set & Agent._CORNERS)    #reward oponent being in corner

        #negative flip because if state is goal, current player lost. 
        # flip is +1 when its agent's turn, but want to penalize losing
        winning = -1*flip_factor*win_weight * state.isGoal() #colinear with legalmovesofother

        score = control_options + control_core + expel_core + avoid_corner + force_corner + winning
        return score
    
    # wrapper for max value with some setup
    def AlphaBetaSearch(self, state: gamestate) -> Tuple[int,packed_action]:
        self.max_prune = 1
        self.num_prune = 0
        self.seen = {state:[self.depth]}
        return self.MaxValueAB(state, self.depth)

    # max and min are basically the same, difference = sign flips
    def MaxValueAB(self, state: gamestate, depth:int, alpha:float = float('-inf'), beta:float=float('inf')) -> Tuple[int, packed_action]:
        if self.display and self.last < len(self.finished) and len(self.finished)%100==0:
            self.last = len(self.finished)
            # print(f'Cached: {self.last} states')

        #if we have already finished evaluating this state with at least this much depth, return saved value
        # try except = reduces hash lookups
        try:
            # finished state stores
            # - initiating a search from that depth on that state, as in knows the depth # of next moves
            # - value it backpropagated
            # - optimal move for state being accessed (var "state")

            stored_depth,val,optimal_moves = self.finished[state]

            # if using finite depth and stored depth is deeper than what's necessary, use it
            saved_deeper_search = depth>=0 and stored_depth>=depth

            # if the value we backpropagated is greater than the max score (or our estimate of the max score), then no matter what depth you searched from, someone can force a win or loss (force a terminal state)
            # CHECK THIS
            guaranteed_terminal = abs(val)>=self.max_score

            # we want for negative depth saved = this has been fully searched
            # CHECK THIS (check maintaining)
            # the only way to have negative depth is if you start with negative depth (so this is only a check for negative depth)
            state_fully_searched = stored_depth<0

            # if we've seen this state before, and we've seen it at a depth greater than the check_tie_depth, then we can assume it's a tie
            tied_state = stored_depth>=self.check_tie_depth

            #
            if (saved_deeper_search or guaranteed_terminal or state_fully_searched or tied_state):
                # if self.display and depth==-1: print(f'MAX USING Saved evaluation {stored_depth,val,move} for depth {depth}')
                return val,optimal_moves
        except KeyError:
            pass
        
        if depth == 0 or state.isGoal():
            h =self.heuristic(state)
            self.finished[state] = (depth,h,[])
            # print(f'SAVING evaluation {state}\n(D,V):{self.finished[state]}')
            return h, []
        
        moves = state.getLegalMoves()
        numMoves = len(moves)
        self.max_prune+= numMoves
        
        # calculate heuristic score for each move
        # sort by score (descending) and then apply that order to moves
        heuristics = np.array([self.action_heuristic(move) for move in moves])
        sort_indexes = np.argsort(heuristics)[::-1]
        moves = moves[sort_indexes]
        
        # v is the value of the best move
        v = float('-inf')
        optimal_moves = None
        for i,m in enumerate(moves):
            next_state = state.getSuccessor(m)
            # if we've seen this state before, then we've seen it at a depth of at least check_tie_depth or negative depth
            if next_state in self.seen and len(self.seen[next_state])>0:
                d = self.check_tie_depth-1 if depth<0 else min(depth-1,self.check_tie_depth-1)
                self.seen[next_state].append(d)
            else:
                d = depth-1
                self.seen[next_state] = [depth]
            
            # v2 is the value of the best move for the opponent
            v2,_ = self.MinValueAB(next_state, d, alpha, beta)
            self.seen[next_state].pop()
            
            if v2 > v:
                v, optimal_moves = v2, [m]
                alpha = max(alpha, v)
            elif v2==v:
                optimal_moves.append(m)
            if self.prune and v > beta:
                self.num_prune+= numMoves-i-1
                return v,optimal_moves

        self.finished[state] = (depth,v,optimal_moves)
        return v, optimal_moves
    
    def MinValueAB(self, state: gamestate, depth:int, alpha:float = float('-inf'), beta:float=float('inf')) -> Tuple[int, packed_action]:
        if self.display and self.last < len(self.finished) and len(self.finished)%100==0:
            self.last = len(self.finished)
            # print(f'Cached: {self.last} states')
        
        #if we have already finished evaluating this state with at least this much depth, return saved value
        try:
            stored_depth,val,optimal_moves = self.finished[state]
            saved_deeper_search = depth>=0 and stored_depth>=depth
            guaranteed_terminal = abs(val)>=self.max_score
            state_fully_searched = stored_depth<0
            tied_state = stored_depth>=self.check_tie_depth-1
            if (saved_deeper_search or guaranteed_terminal or state_fully_searched or tied_state):
                # print(f'USING Saved evaluation | {self.finished[state]}')
                return val,optimal_moves
            # else: print(f'NOT using saved {stored_depth,val,move} for current depth {depth}')
        except KeyError:
            pass
        
        if depth == 0 or state.isGoal():
            h = self.heuristic(state)
            self.finished[state] = (depth,h,[])
            # print(f'SAVING evaluation {state}\n(D,V):{self.finished[state]}')
            return h, []
      
        moves = state.getLegalMoves()
        numMoves = len(moves)
        self.max_prune+= numMoves
        
        heuristics = np.array([self.action_heuristic(move) for move in moves])
        sort_indexes = np.argsort(heuristics)[::-1]
        moves = moves[sort_indexes]
        
        v = float('inf')
        optimal_moves = None
        for i,m in enumerate(moves):
            next_state = state.getSuccessor(m)
            
            if next_state in self.seen and len(self.seen[next_state])>0:
                d = self.check_tie_depth if depth<0 else min(depth-1,self.check_tie_depth)
                self.seen[next_state].append(d)
            else:
                d = depth-1
                self.seen[next_state] = [depth]
                
            v2,_ = self.MaxValueAB(next_state, d, alpha, beta)
            self.seen[next_state].pop()
            
            if v2 < v:
                v, optimal_moves = v2, [m]
                beta = min(beta, v)
            elif v2==v:
                optimal_moves.append(m)
            if self.prune and v < alpha:
                self.num_prune+=numMoves-i-1
                return v,optimal_moves
            
        self.finished[state] = (depth,v,optimal_moves)
        return v, optimal_moves

    def game_reset(self):
        # pass
        self.played_states = {}
        
        
        
        
        
        
import numpy as np

from typing import Optional
class Game:
    def __init__(self, L_pieces=None, token_pieces=None):
        if L_pieces and token_pieces:
            self.state = gamestate(L_pieces=L_pieces, token_pieces=token_pieces)
        else: 
            self.state = gamestate()
        self.turns = 0
        
    def getTurn(self)->int:
        return self.state.player
    
    def getState(self)->gamestate:
        return gamestate(self.state.player,self.state.L_pieces[:],self.state.token_pieces.copy(),self.state.transform[:])
    
    #updates game state with action if it is valid, returns true iff successfuly
    #feedback passed through to valid moves
    def apply_action(self,move:packed_action)->None:
        self.state = self.state.getSuccessor(move)
        self.turns+=1
        
    #interface to display game board and pieces
    def display(self,internal_display:bool=False)->None:
        board = np.full((4, 4), "  ", dtype=object) # 4 by 4 of empty string
        
        #denormalize to display what human expects to see
        if not internal_display: self.state.denormalize()
        
        for i, l in enumerate(self.state.L_pieces):
            color = "\033[1;31m1□\033[0m" if i == 0 else "\033[32m2▲\033[0m"  # Red for L1, Blue for L2
            for px, py in l.get_coords():
                board[py - 1, px - 1] = color #+ "L" + str(i + 1) + "\033[0m"
        
        for i, t in enumerate(self.state.token_pieces):
            tx, ty = t.get_position()
            board[ty - 1, tx - 1] = "\033[33m○○\033[0m"


        rows = ["|" + "|".join(f"{cell:>2}" for cell in row) + "|" for row in board]
        #left wall then the row then the ending right wall
        # f"{cell:>2}" align cell to the right > with a width of 2 spaces. 

        horizontal_separator = "-------------\n"
        
        board_str = horizontal_separator + f"\n{horizontal_separator}".join(rows) + "\n" + horizontal_separator
        print(board_str)
        
        #renormalize for internal use
        if not internal_display: self.state.normalize(self.state.transform)
    
    #determines who wins, returns None, 0 or 1
    # made a copy of this in gamestate
    def whoWins(self)->Optional[int]:
        return self.state.whoWins()
    
    def totalTurns(self)->int:
        return self.turns
    
    def reset(self)->None:
        self.state = gamestate()
        self.turns = 0
    


# use Python 3.5 and up (typing library built in)
from typing import Tuple,List,Optional

# gamemode input, exception handling
def getPlayers()->Tuple[
                    Tuple[int,Optional[int],Optional[bool]],
                    Tuple[int,Optional[int],Optional[bool]]]:
    print(f"\
                                0 = human\n\
                                1 = agent\n\
                                2 = random\n")
    
    players = []
    for i in range(2):
        while True:
            try:
                p = int(input(f"\
                                Enter Player {i+1}: "))
                if p not in {0, 1, 2}:
                    raise ValueError()
                if p==1:
                    depth = int(input(f"\
                                Player {i+1} Depth (int or -1): "))
                    prune = bool(int(input(f"\
                                Player {i+1} Prune (0 or 1): ")))
                    player = [p,depth,prune]
                else: player = [p,None,None]
                players.append(tuple(player))
                print()
                break
            except ValueError:
                print('Invalid Input')
        
    return tuple(players)

def setGameMode(p1,p2)->Tuple[np.ndarray[bool],np.ndarray[Player]]:
    # instantiating players
    player_dict = {
        0: Human,
        1: Agent,
        2: RandomAgent,
    }
    player1 = player_dict[p1[0]](0) if p1[1]==None else player_dict[p1[0]](0,p1[1],p1[2])
    player2 = player_dict[p2[0]](1) if p2[1]==None else player_dict[p2[0]](1,p2[1],p2[2])
    players = np.array([player1,player2])
    return np.array([p1[0]==2,p2[0]==2]),players

def play(gm:Tuple[Tuple[int,Optional[int],Optional[int]],Tuple[int,Optional[int],Optional[int]]]=None,N:int=1,display=True)->Tuple[np.ndarray,np.ndarray,List[List[float]]]:

    # Set initial state
    
    while True:
        InitialStateCoordinates = input(f"Enter Initial State Coords [L1, L2, T1, T2] or Default: ")
        InitialStateCoordinatesList = InitialStateCoordinates.split()

        try:
            InitialStateCoordinatesList = InitialStateCoordinates.split()
            if len(InitialStateCoordinatesList) == 0:
                print('Using Default Initial Gamestate')
                game = Game()
            else:
                L1_x, L1_y, L1_d = int(InitialStateCoordinatesList[0]), int(InitialStateCoordinatesList[1]), InitialStateCoordinatesList[2]
                L2_x, L2_y, L2_d = int(InitialStateCoordinatesList[3]), int(InitialStateCoordinatesList[4]), InitialStateCoordinatesList[5]
                T1_x, T1_y = int(InitialStateCoordinatesList[6]), int(InitialStateCoordinatesList[7])
                T2_x, T2_y = int(InitialStateCoordinatesList[8]), int(InitialStateCoordinatesList[9])

                L_pieces = [L_piece(x=L1_x, y=L1_y, d=L1_d), L_piece(x=L2_x, y=L2_y, d=L2_d)]
                token_pieces = {token_piece(x=T1_x, y=T1_y), token_piece(x=T2_x, y=T2_y)}

                game = Game(L_pieces=L_pieces, token_pieces=token_pieces)
            break
        except (ValueError,AssertionError) as e:
            print('Invalid Intial State')
        except IndexError as e:
            print('Enter Moves in correct Format')
        
        # End set initial state

    if gm==None:
        randoms,players = setGameMode(*getPlayers())
    else:
        randoms,players = setGameMode(*gm)
    winners  = np.empty(shape=(N),dtype=int)
    turns = np.empty(shape=(N),dtype=int)
    turn_times = [[],[]]
    # for n in tqdm(range(N)):
    for n in range(N):
        for i,r in enumerate(randoms):
            if r:
                players[i].set_seed(n+i)
        while game.whoWins()==None and game.totalTurns()<64:
            if display:
                print()
                # print(game.state)
                # game.display(internal_display=True)
                game.display()
            turn = game.getTurn()
            if display: print(f"Player {turn+1}'s turn (Turn {game.totalTurns()+1})")
            
            current_player = players[turn]
            success=False
            K = 3
            for k in range(K):#while True
                try:
                    start = time.time()
                    move = current_player.getMove(game.getState(),display) #value error if invalid input format
                    end=time.time()
                    # if display: print("Move:",move)
                    game.apply_action(move)  #assertion error if invalid move
                    success=True
                    turn_times[turn].append(end-start)
                    break
                except ValueError as e:
                    print(f'Invalid Input. {e}\n')
                except AssertionError as e:
                    print(f'Invalid Move. {e}\n')
            if not success: #if no valid move provided after K attempts, kill game
                print(f'\n\nNo valid play after {K} moves. Game over.')
                break

        winner = game.whoWins()
        winner = int(not turn)+1 if winner==None else winner+1
        winner = winner if game.totalTurns()<64 else 0
        winners[n] = winner
        turns[n] = game.totalTurns()

        if display: 
            game.display()

            if game.totalTurns()==64:
                print('Draw!')
            else:                
                print('Player',winner,'wins!')
                print('Total Turns',game.totalTurns())
            
        game.reset()
        for player in players:
            player.game_reset()
    print()
    length = max(len(turn_times[0]),len(turn_times[1]))
    turn_times = [row + [0] * (length - len(row)) for row in turn_times]
    return winners, turns, turn_times

if __name__ == "__main__":
    # profiler = cProfile.Profile()
    # profiler.enable()
    
    # _,_,_ = play()

    # Play again?
    while True:
        _,_,_ = play()
        cont = input('Play again? (y/n): ')
        if cont.lower() != 'y'.strip():
            break
    
    # profiler.disable()
    
    # stats = pstats.Stats(profiler)
    
    # Sort by 'time' (total time in each function) and print the top 10 functions
    # stats.strip_dirs()  # Optional: remove long file paths for readability
    # stats.sort_stats("time").print_stats(16)
    