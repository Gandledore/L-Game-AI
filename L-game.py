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
    
    #vertical initial state
    # def __init__(self, 
    #                 player:int=0,
    #                 L_pieces:List[L_piece]=[L_piece(x=2,y=4,d='E'),L_piece(x=3,y=1,d='W')],
    #                 token_pieces:Set[token_piece]={token_piece(x=1,y=1),token_piece(x=4,y=4)},
    #                 transform:np.ndarray[bool]=np.array([False,False,False])):
    
    #horizontal initial state
    def __init__(self,
                    player:int=0,
                    L_pieces:List[L_piece]=None,
                    token_pieces:Set[token_piece]=None,
                    transform:np.ndarray[bool]=None):
        
        self.player:int = player
        self.L_pieces: List[L_piece] = L_pieces if L_pieces is not None else [L_piece(x=1,y=3,d='N'),L_piece(x=4,y=2,d='S')]
        self.token_pieces: Set[token_piece] = token_pieces if token_pieces is not None else {token_piece(x=1,y=1),token_piece(x=4,y=4)}
        self.transform = transform if transform is not None else np.array([False,False,False])
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
                print('Saving Legal Moves...',end='')
                pickle.dump(cls._legalMoves,f)
                print('\rSaved Legal Moves')
        
    def __repr__(self):
        return f"Player: {self.player}\nL pieces: {self.L_pieces}\nT pieces: {self.token_pieces}\nTransform:{self.transform}"
    
    def display(self,internal_display=False):
        board = np.full((4, 4), "  ", dtype=object) # 4 by 4 of empty string
        
        #denormalize to display what human expects to see
        if not internal_display: self.denormalize()
        
        for i, l in enumerate(self.L_pieces):
            color = "\033[1;31m1□\033[0m" if i == 0 else "\033[32m2▲\033[0m"  # Red for L1, Blue for L2
            for px, py in l.get_coords():
                board[py - 1, px - 1] = color #+ "L" + str(i + 1) + "\033[0m"
        
        for i, t in enumerate(self.token_pieces):
            tx, ty = t.get_position()
            board[ty - 1, tx - 1] = "\033[33m○○\033[0m"


        rows = ["|" + "|".join(f"{cell:>2}" for cell in row) + "|" for row in board]
        #left wall then the row then the ending right wall
        # f"{cell:>2}" align cell to the right > with a width of 2 spaces. 

        horizontal_separator = "-------------\n"
        
        board_str = horizontal_separator + f"\n{horizontal_separator}".join(rows) + "\n" + horizontal_separator
        print(board_str)
        
        #renormalize for internal use
        if not internal_display: self.normalize(self.transform)
    
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

    def update_denormalization(self,transform:np.ndarray[bool])->None:
        #if new state is transposed, swap original reflect x and reflect y to compensate cause that's what transpose does
        if transform[2] and self.transform[0]!=self.transform[1]:
            self.transform[:2] = np.logical_not(self.transform[:2])
        
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
    

    #interface to display game board and pieces, added for Human transform display
    #self.state._____ becomes self.______
    def display(self,internal_display:bool=False)->None:
        board = np.full((4, 4), "  ", dtype=object) # 4 by 4 of empty string
        
        #denormalize to display what human expects to see
        if not internal_display: self.denormalize()
        
        for i, l in enumerate(self.L_pieces):
            color = "\033[1;31m1□\033[0m" if i == 0 else "\033[32m2▲\033[0m"  # Red for L1, Blue for L2
            for px, py in l.get_coords():
                board[py - 1, px - 1] = color #+ "L" + str(i + 1) + "\033[0m"
        
        for i, t in enumerate(self.token_pieces):
            tx, ty = t.get_position()
            board[ty - 1, tx - 1] = "\033[33m○○\033[0m"


        rows = ["|" + "|".join(f"{cell:>2}" for cell in row) + "|" for row in board]
        #left wall then the row then the ending right wall
        # f"{cell:>2}" align cell to the right > with a width of 2 spaces. 

        horizontal_separator = "-------------\n"
        
        board_str = horizontal_separator + f"\n{horizontal_separator}".join(rows) + "\n" + horizontal_separator
        print(board_str)
        
        #renormalize for internal use
        if not internal_display: self.normalize(self.transform)




from abc import ABC,abstractmethod

from typing import Tuple,Union,List
class Player(ABC):

    def __init__(self,id:int):
        self.id = id
    
    @abstractmethod
    def instructionHandler(self, state: gamestate, display:bool=False) -> Tuple[str,Union[packed_action,str,List[bool]]]:
        pass
    
    @abstractmethod
    def getMove(self, state: gamestate, display:bool=False) -> packed_action:
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
        if display: 
            move.denormalize(state.transform)
            print(f"Random Agent played {move}")
            move.normalize(state.transform)
        return move

    def instructionHandler(self, state: gamestate, display:bool=False):
        return ('move', self.getMove(state,display))
    
    def set_seed(self,s):
        random.seed(s)
        
    def game_reset(self):
        pass

import numpy as np

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
    def getMove(self, state: gamestate, move_parts) -> packed_action:
        if len(move_parts)==7 or len(move_parts)==3:
            try:    #raises value error if can't cast to int
                new_l_pos = (int(move_parts[0]), int(move_parts[1]),move_parts[2])
            except ValueError as e:
                raise ValueError('Use integers for x and y.')
            
            if len(move_parts)==7:
                try:
                    current_token_pos = (int(move_parts[3]), int(move_parts[4]))
                    new_token_pos = (int(move_parts[5]), int(move_parts[6]))
                except ValueError as e:
                    raise ValueError('Use integers for token locations.')
            elif len(move_parts)==3:
                current_token_pos=(0,0)
                new_token_pos = (0,0)
        
            move = packed_action(l_piece_id=state.player,new_l_pos=new_l_pos,current_token_pos=current_token_pos,new_token_pos=new_token_pos)
            move.normalize(state.transform)
        else:
            raise ValueError(f"Enter commands in specified format.")
        return move

    def instructionHandler(self, state:gamestate, display:bool=False):
        if display: print('Valid Moves:',len(state.getLegalMoves()))
        
        moves = state.getLegalMoves()
        vals = np.array([self.heuristic(state.getSuccessor(move)) for move in state.getLegalMoves()])
        bestMove = moves[np.argmax(vals)]

        bestMove.denormalize(state.transform)
        print("Suggested Move: ", bestMove.suggest_format())
        bestMove.normalize(state.transform)
        
        instruction = input("Enter instruction: ")
        pieces = instruction.split()
        if len(pieces)==0:
            return ('move',bestMove)
        instruction = pieces[0]
        if instruction not in ('undo','redo','replay','save','swap','x','y','t','cw','ccw','help'):
            return ('move',self.getMove(state,pieces))
        elif instruction == "x":
            return ('view',[True,False,False])
        elif instruction == "y":
            return ('view',[False,True,False])
        elif instruction == "t":
            return ('view',[False,False,True])
        elif instruction == "cw":
            return ('view',[True,False,True])
        elif instruction == "ccw":
            return ('view',[False,True,True])
        elif instruction == 'replay':
            return ('view','replay')
        elif instruction in ('undo','redo','save','help'):
            return ('control',instruction)
        elif instruction=='swap':
            return ('swap','ai')
        else:
            raise ValueError(f"Invalid instruction {instruction}.")
        
    def game_reset(self):
        pass

from typing import Tuple
import time
import numpy as np
import pickle
from tqdm import tqdm

import sys
sys.setrecursionlimit(5000)#maybe this can be improved

class Agent(Player):

    # Constants for heuristic
    _CORE = {(2,2), (2,3), (3,2), (3,3)}                                        #the coordinates of the core
    _CORNERS = {(1,1), (1,4), (4,1), (4,4)}                                     #the coordinates of the corner
    _KILLER_TOKENS = {(2,1), (3,1), (1,2), (1,3), (4,2), (4,3), (2,4), (3,4)}   #the coordinates of the attacking token positions
    
    #states where an optimal oponent can force us to loss, according to wikipedia (and confirmed via previous testing)
    _death_states = {  gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(1,3),token_piece(4,1)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(1,4),token_piece(4,2)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(1,4),token_piece(4,1)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(4,3),token_piece(4,1)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(3,4),token_piece(4,3)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(4,3),token_piece(4,2)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(3,4),token_piece(4,2)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(3,4),token_piece(4,1)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(4,2),token_piece(4,1)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(3,3,'N')],token_pieces={token_piece(4,2),token_piece(4,1)}),
                            gamestate(0,L_pieces=[L_piece(2,1,'S'),L_piece(1,3,'N')],token_pieces={token_piece(3,2),token_piece(3,4)}),
                            gamestate(0,L_pieces=[L_piece(2,1,'S'),L_piece(3,3,'N')],token_pieces={token_piece(1,2),token_piece(4,2)}),
                            gamestate(0,L_pieces=[L_piece(2,1,'S'),L_piece(1,3,'N')],token_pieces={token_piece(3,2),token_piece(4,4)}),
                            gamestate(0,L_pieces=[L_piece(1,2,'N'),L_piece(1,3,'S')],token_pieces={token_piece(3,1),token_piece(4,2)}),
                            
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(1,3),token_piece(4,1)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(1,4),token_piece(4,2)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(1,4),token_piece(4,1)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(4,3),token_piece(4,1)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(3,4),token_piece(4,3)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(4,3),token_piece(4,2)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(3,4),token_piece(4,2)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(3,4),token_piece(4,1)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(4,2),token_piece(4,1)}),
                            gamestate(1,L_pieces=[L_piece(3,3,'N'),L_piece(1,1,'S')],token_pieces={token_piece(4,2),token_piece(4,1)}),
                            gamestate(1,L_pieces=[L_piece(1,3,'N'),L_piece(2,1,'S')],token_pieces={token_piece(3,2),token_piece(3,4)}),
                            gamestate(1,L_pieces=[L_piece(3,3,'N'),L_piece(2,1,'S')],token_pieces={token_piece(1,2),token_piece(4,2)}),
                            gamestate(1,L_pieces=[L_piece(1,3,'N'),L_piece(2,1,'S')],token_pieces={token_piece(3,2),token_piece(4,4)}),
                            gamestate(1,L_pieces=[L_piece(1,3,'S'),L_piece(1,2,'N')],token_pieces={token_piece(3,1),token_piece(4,2)})}
    
    
    def __init__(self, id:int, depth=-1, prune:bool=False,):
        super().__init__(id)
        
        self.prune = bool(prune)
        
        #default depth to search a state, -1 does infinite depth and solves whole game
        self.depth = depth
        
        # TRANSPOSITION TABLE (state: (depth,alpha,beta,optimal_moves_list))
        # depth=d means the state was searched up to depth d (equivalent to directly calling search from the state with depth d)
        # alpha,beta are pruning bounds.  alpha==beta implies all children were evaluated, or its a terminal node, or state is a death state
        # optimal moves stores all moves of equivalent value (best value found for the node so far)
        self.finished = {}
        
        #save heuristics for actions cause they're called a lot for sorting moves
        self.action_heuristics = {}
        
        # depth necessary to be confident a repeated state is a tie
        # 2 because we have stored all possible death states
        self.check_tie_depth = 2
        
        #keep track of states seen in current game, so that we can switch moves to hopefully confuse opponent
        self.played_states = {}
        
        #location for saved optimal moves, or location to save it
        self.optimal_moves_path = 'optimal_moves_id'+str(self.id)+'.pkl'
        self.display=False
        
        #only pre-process optimal moves for states when running infinite depth
        if self.depth<0:self.preprocess_optimal_moves()
    
    #load or precompute and save optimal moves
    def preprocess_optimal_moves(self):
        """
            loads or precomputes and save optimal moves
            looks for file stored in self.optimal_moves_path
            if it doesn't exist, runs through states solving optimal moves and saves in file specified by self.optimal_moves_path
        """
        #try to load saved file
        try:
            with open(self.optimal_moves_path,'rb') as f:
                print('Loading Solved Game...',end='')
                self.finished = pickle.load(f)
                print('\rLoaded Solved Game    ')
        
        #if file not found, process optimal moves and save
        except FileNotFoundError:
            print(f'Game not Solved. Player {self.id+1} solving game now...')
            #run through each state and optimize move for it
            for s in gamestate._legalMoves.keys():
                if s.player==self.id:#only have to optimize for states I will see
                    _,_ = self.AlphaBetaSearch(s)
            
            #save optimal moves in pickle file
            with open(self.optimal_moves_path,'wb') as f:
                print('Saving Optimal Moves...',end='')
                pickle.dump(self.finished,f)
                print('\rSaved Optimal Moves    ')
           
    #takes a state and wether do display information, and returns an action
    #called by play when this players turn 
    def getMove(self, state: gamestate,display:bool=False) -> packed_action:
        self.display=display
        if self.display: print('Thinking...')
        
        #call alpha beta search and measure time to compute next move
        start = time.time()
        value, bestActions = self.AlphaBetaSearch(state)
        end = time.time()

        #keep track of number of times seen this state in a game
        attempt = self.played_states.get(state)
        if attempt is None:
            attempt=0
            self.played_states[state]=0
        self.played_states[state]+=1
        
        #choose the kth move of bestActions after seeing it k times.
        #this switches up move to throw off opponent
        bestAction = bestActions[attempt%len(bestActions)]

        if self.display:
            if self.depth>0: print(f'Finished MinMaxing {len(self.finished)} states')
            bestAction.denormalize(state.transform) #to print as human expects
            print(f'Choosing Move:{bestAction} for value: {value}')
            bestAction.normalize(state.transform)   #to return as game expects
            print(f'Time: {1000*(end-start):.3f}ms | Pruned: {100*self.num_prune/self.max_prune:.2f}% ({self.num_prune}/{self.max_prune})')
        return bestAction

    def instructionHandler(self, state:gamestate, display:bool=False):
        return ('move',self.getMove(state,display))
    
    #heuristic to estimate how good an action is (current version not very good)
    def action_heuristic(self,move:packed_action)->int:
        #if already known, return it
        h = self.action_heuristics.get(move)
        if h is not None:
            return h
        
        #otherwise compute it
        core_weight = 25                #weight for being in the core
        corner_weight = 40              #weight for being in the corner
        killer_token_weight = 10        #weight for placing a token in a killer position
        
        l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, curr_token_pos_x, curr_token_pos_y, new_token_pos_x,new_token_pos_y = move.get_rep()
        new_l_pos = (new_l_pos_x,new_l_pos_y,new_l_pos_d.decode('utf-8'))
        curr_t_pos = (curr_token_pos_x,curr_token_pos_y)
        new_t_pos = (new_token_pos_x,new_token_pos_y)
        
        l_set = L_piece._compute_L_coords(*new_l_pos)

        control_core = core_weight * len(l_set & Agent._CORE)                   #reward controlling core
        avoid_corner = -1*corner_weight * int(bool(l_set & Agent._CORNERS))     #penalize touching corner
        killer_token = killer_token_weight * int(new_t_pos in Agent._KILLER_TOKENS if curr_t_pos!=(0,0) else 0) #reward placing tokens in killer positions
        
        score = control_core + avoid_corner + killer_token
        self.action_heuristics[move]=score      #save score for later
        return score
    
    #estimate how good a state is (current version not very good)
    def heuristic(self, state:gamestate) -> float:
        player = self.id
        opponent = int(not self.id)
        flip_factor = 2*int(player == state.player) - 1 #1 if my turn, -1 if opponent's turn

        options_weight = 1          #weight for how many moves this state has
        core_weight = 25            #weight for being in the core
        corner_weight = 40          #weight for being in the corner
        win_weight = float('inf')   #weight for winning or losing

        #penalize number of moves other person has
        control_options = flip_factor * options_weight * len(state.getLegalMoves()) #reward me having moves, penalize moves for opponent
        
        player_l_set = state.L_pieces[player].get_coords()
        opponent_l_set = state.L_pieces[opponent].get_coords()
        
        # reward for controlling core
        control_core = core_weight * len(player_l_set & Agent._CORE)
        # penalize opponent in core
        expel_core = -1*core_weight * len(opponent_l_set & Agent._CORE)
        # penalize touching corner
        avoid_corner = -1*corner_weight * len(player_l_set & Agent._CORNERS)
        # reward opponent being in corner (we want to trap them in a corner / basically all win states involve opponent in corner)
        force_corner = corner_weight * len(opponent_l_set & Agent._CORNERS)

        # negative flip because if state is goal, current player lost.
        # flip_factor is +1 when its agent's turn, but want to penalize losing
        endgame = state in Agent._death_states
        winning = -1*flip_factor*win_weight if state.isGoal() or endgame else 0 #colinear with legalmovesofother

        score = control_options + control_core + expel_core + avoid_corner + force_corner + winning
        return score
    
    # wrapper for max value with some setup
    def AlphaBetaSearch(self, state: gamestate) -> Tuple[int,packed_action]:
        #for pruning quanitfication
        self.max_prune = 1
        self.num_prune = 0
        
        #keeps track of dfs path to detect tie
        self.seen = {state:1}
        return self.MaxValueAB(state, self.depth)

    # max and min are basically the same
    def MaxValueAB(self, state: gamestate, depth:int, alpha:float = float('-inf'), beta:float=float('inf')) -> Tuple[int, packed_action]:
        
        # if we have already finished evaluating this state with at least this much depth, return saved value
        cached_data = self.finished.get(state)
        if cached_data is not None:
            # finished state stores
            # - initiating a search from that depth on that state, as in knows the depth # of next moves
            # - alpha and beta as bounds for pruning
            # - optimal moves for state being accessed (any moves with equivalent value to best so far)

            stored_depth,saved_alpha,saved_beta,optimal_moves = cached_data

            # if using finite depth and stored depth is deeper than what's necessary, use it
            saved_deeper_search = depth>=0 and stored_depth>=depth

            # negative depth saved => state fully searched
            # the only way to have negative depth is if you start with negative depth (so this is only true when solving whole game)
            state_fully_searched = stored_depth<0

            # if the depth searched is greater than tie state, we can assume it is a tie
            tied_state = stored_depth>=self.check_tie_depth

            #if the state being accessed was pruned, then check if it can be pruned again without any searching
            prunable = saved_alpha>beta
            exact = saved_beta==saved_alpha #state fully searched for saved depth, or endgame state (terminal or death)
            if (saved_deeper_search or state_fully_searched or tied_state):
                if exact or prunable:
                    return saved_alpha,optimal_moves
        
        moves = state.getLegalMoves()
        numMoves = len(moves)
        self.max_prune+= numMoves       #keep track for pruning data
        
        # calculate heuristic score for each move
        # sort by score (descending) and then apply that order to moves
        # if action heuristic is good, should prune a lot
        heuristics = np.array([self.action_heuristic(move) for move in moves])
        sort_indexes = np.argsort(heuristics,stable=True)[::-1]     #sort reverse cause standard sorts in increasing order, but higher heuristic is better
        moves = moves[sort_indexes]
        
        if state in Agent._death_states:
            h = self.heuristic(state)
            self.finished[state] = (-1,h,h,moves)
            return h,moves
        
        if depth == 0 or state.isGoal():
            h = self.heuristic(state)
            self.finished[state] = (depth,h,h,None)
            return h, None
        
        # v is the value of the best move
        v = float('-inf')
        optimal_moves = []
        for i,m in enumerate(moves):
            next_state = state.getSuccessor(m)
            # if we've seen this state before, then start a check from check_tie_depth instead of continuing infinite search
            num_seen = self.seen.get(next_state)
            
            if num_seen is None:
                self.seen[next_state]=0
                d=depth-1
            elif num_seen>0:
                d = self.check_tie_depth if depth<0 else min(depth-1,self.check_tie_depth)
            else:
                d = depth-1
                
            # v2 is the value of the best move for the opponent (could be a pruned value, in which case its ignored)
            self.seen[next_state]+=1
            v2,_ = self.MinValueAB(next_state, d, v, beta)      #pass v to ensure not pruning on parent's data (because saving to transposition table)
            self.seen[next_state]-=1
            
            #if new best, update optimal moves and v
            if v2 > v:
                v, optimal_moves = v2, [m]
                alpha = max(alpha, v)
            elif v2==v:
                optimal_moves.append(m)         #save other moves with value equal to current equivalent
            if self.prune and v > beta:         #don't prune on equality because saving equal values. parent node would add it to its optimal moves list
                self.num_prune+= numMoves-i-1
                self.finished[state] = (depth,v, float('inf'),optimal_moves)        #max can do at least as well as alpha, could be any amount higher
                return v,optimal_moves
        
        self.finished[state] = (depth,v,v,optimal_moves)
        return v, optimal_moves
    
    def MinValueAB(self, state: gamestate, depth:int, alpha:float = float('-inf'), beta:float=float('inf')) -> Tuple[int, packed_action]:
        #if we have already finished evaluating this state with at least this much depth, return saved value
        cached_data = self.finished.get(state)
        
        if cached_data is not None:
            stored_depth,saved_alpha,saved_beta,optimal_moves = cached_data
            saved_deeper_search = depth>=0 and stored_depth>=depth
            state_fully_searched = stored_depth<0
            tied_state = stored_depth>=self.check_tie_depth
            prunable = saved_beta<alpha
            exact = saved_beta==saved_alpha
            if (saved_deeper_search or state_fully_searched or tied_state):
                if exact or prunable:
                    return saved_beta,optimal_moves
            
        #not prune on equality when saving equal states
        moves = state.getLegalMoves()
        numMoves = len(moves)
        self.max_prune+= numMoves
        
        heuristics = np.array([self.action_heuristic(move) for move in moves])
        sort_indexes = np.argsort(heuristics,stable=True)[::-1]
        moves = moves[sort_indexes]
        
        if state in Agent._death_states:
            h = self.heuristic(state)
            self.finished[state] = (-1,h,h,moves)
            return h,moves
      
        if depth == 0 or state.isGoal():
            h = self.heuristic(state)
            self.finished[state] = (depth,h,h,None)
            return h, None
        
        v = float('inf')
        optimal_moves = []
        for i,m in enumerate(moves):
            next_state = state.getSuccessor(m)
            
            num_seen = self.seen.get(next_state)
            
            if num_seen is None:
                self.seen[next_state]=0
                d=depth-1
            elif num_seen>0:
                d = self.check_tie_depth if depth<0 else min(depth-1,self.check_tie_depth)
            else:
                d = depth-1
            
            self.seen[next_state]+=1
            v2,_ = self.MaxValueAB(next_state, d, alpha, v)
            self.seen[next_state]-=1
            
            if v2 < v:
                v, optimal_moves = v2, [m]
                beta = min(beta, v)
            elif v2==v:
                optimal_moves.append(m)
            if self.prune and v < alpha:
                self.num_prune+=numMoves-i-1
                self.finished[state] = (depth,float('-inf'),v,optimal_moves)
                return v,optimal_moves

        self.finished[state] = (depth,v,v,optimal_moves)
        return v, optimal_moves

    def game_reset(self):
        # pass
        self.played_states = {}#reset this so that it starts from best of bestActions


import numpy as np
import time
import pickle

from typing import Optional

class Game:
    def __init__(self, L_pieces=None, token_pieces=None):
        if L_pieces and token_pieces:
            self.state = gamestate(L_pieces=L_pieces, token_pieces=token_pieces)
        else: 
            self.state = gamestate()
        
        self.turns = 0

        # List of moves for undoing and redoing
        self.history = []

        # Save initial state
        self.saveMove()
    
    def saveMove(self)->None:
        try:
            self.history[self.turns] = self.state
        except IndexError:
            self.history.append(self.state)
        self.turns+=1
    
    def undo(self) -> bool:

        if self.turns < 3:
            return False

        # undo -- this should go back to this players previous move
        self.turns -= 2
        self.state = self.history[self.turns-1]
        return True

    def redo(self) -> bool:
        if self.turns==len(self.history):
            return False
        self.turns += 2
        self.state = self.history[self.turns-1]
        return True
        
    def replay(self) -> None:
        for i in range(self.turns-1):
            self.history[i].display()
            time.sleep(.5)

    def getTurn(self)->int:
        return self.state.player
    
    def getState(self)->gamestate:
        return gamestate(self.state.player,
                        self.state.L_pieces[:],
                        self.state.token_pieces.copy(),
                        self.state.transform[:])
    
    #updates game state with action if it is valid, returns true iff successfuly
    #feedback passed through to valid moves
    def apply_action(self,move:packed_action)->None:
        self.state = self.state.getSuccessor(move)
        self.saveMove()
        
    #interface to display game board and pieces
    def display(self,internal_display:bool=False)->None:
        self.state.display(internal_display=internal_display)
    
    #determines who wins, returns None, 0 or 1
    # made a copy of this in gamestate
    def whoWins(self)->Optional[int]:
        return self.state.whoWins()
    
    def totalTurns(self)->int:
        return self.turns
    
    def reset(self)->None:
        self.history.clear()

        self.turns = 0
        self.state = gamestate()
        self.saveMove()

    def save(self, filename: str = None) -> None:
        save_dict = {'history': self.history[:self.turns], 'turns': self.turns}
        if filename is None:
            filename = str(round(time.time())) + '.pkl'
        else:
            if filename[-4:] != '.pkl':
                filename = filename + '.pkl'
        with open(filename, 'wb') as f:
            pickle.dump(save_dict, f)
        print('Game saved to',filename)

    @staticmethod
    def load(filename: str) -> 'Game':
        # if filename doesnt end with pkl, add it
        if filename[-4:] != '.pkl':
            filename = filename + '.pkl'
        # filename = filename + '.pkl'
        with open(filename, 'rb') as f:
            save_dict = pickle.load(f)
        
        game = Game()
        game.history = save_dict['history']
        game.turns = save_dict['turns']
        game.state = game.history[game.turns-1]
        
        print('Game',filename,"loaded.\n")
        return game


# our imports
import Players

# use Python 3.5 and up (typing library built in)
from typing import Tuple,List,Optional

import sys
import subprocess
import time

# profiling (built in?)
import cProfile
import pstats

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
    return players

# change player from human to agent and take input
def changePlayer(player:Player)->Player:
    if isinstance(player,Human):
        depth = int(input(f"Enter Depth (int or -1): "))
        prune = bool(int(input(f"Enter Prune (0 or 1): ")))
        return Agent(player.id,depth,prune)
    return player

def loadGame() -> Optional[Game]:
    while True:
        load = input('Load Game? (y/n): ')
        if load.lower() == 'y':
            try:
                filename = input('Enter filename: ')
                return Game.load(filename)            
            except FileNotFoundError as e:
                print('File not found')
        else:
            return None
        
def create_game():
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

        except (ValueError,AssertionError) as e:
            print('Invalid Intial State')
            continue
        except IndexError as e:
            print('Enter Moves in correct Format')
            continue
        
        # print board to get confirmation from user that they want to use this board
        game.display()
        while True:
            confirm = input('Confirm this board? (y/n): ')
            if confirm.lower() == 'n':
                del game
                game = None
                break
            elif confirm.lower()=='y' or confirm.lower()=='':
                return game
            else:
                print("Please enter 'y' or 'n'")
def print_instructions():
    print("\n\n\
            Instructions:\n\
            Move: x y d t1x t1y t2x  t2y\n\
            Undo: undo\n\
            Redo: redo\n\
            Replay: replay\n\
            Save Game: save\n\
            Transform Board: 'x' or 'y' or 't' or 'cw' or 'ccw'\n\
            Have AI take over: swap\n\
            Display Instructions: help\n\
    \n\n")
def play(gm:Tuple[Tuple[int,Optional[int],Optional[int]],Tuple[int,Optional[int],Optional[int]]]=None,N:int=1,display=True)->Tuple[np.ndarray,np.ndarray,List[List[float]]]:

    game = loadGame()

    if game is None:
        game = create_game()

    if gm==None:
        players = setGameMode(*getPlayers())
    else:
        players = setGameMode(*gm)

    print_instructions()

    tie_end = 64
    while game.whoWins()==None and game.totalTurns()<tie_end:
        if display: game.display()
        
        turn = game.getTurn()
        if display: print(f"Player {turn+1}'s turn (Turn {game.totalTurns()})")
        
        current_player = players[turn]
        success=False
        K = 5
        for k in range(K):#while True
            try:
                instruction_type,instruction = current_player.instructionHandler(game.getState(),display) #value error if invalid input format

                if instruction_type == 'move':
                    game.apply_action(instruction)  #assertion error if invalid move
                elif instruction_type == 'view':
                    if instruction == 'replay':
                        print('\nReplaying Game until current turn')
                        game.replay()
                    elif isinstance(instruction,List) and len(instruction)==3:#not checking that elements are bool
                        game.state.update_denormalization(instruction)#bad practice
                elif instruction_type=='control':
                    if instruction == 'undo':
                        if game.undo():
                            print('\nUndo Successful\n')
                        else:
                            print('\nUndo Unsuccessful\n')
                    elif instruction == 'redo':
                        if game.redo():
                            print('\nRedo Successful\n')
                            game.display()
                        else:
                            print('\nRedo Unsuccessful\n')
                    elif instruction == 'save':
                        filename = input('Enter filename: ')
                        game.save(filename)
                    elif instruction == 'help':
                        print_instructions()
                elif instruction_type=='swap':
                    if instruction=='ai':
                        current_player = changePlayer(current_player)
                        players[turn] = current_player
                        print(f'Player {turn+1} changed to AI')
                else:
                    raise ValueError(f"Invalid instruction {instruction}.")
                success=True
                break
            
            except ValueError as e:
                print(f'Invalid Input. {e}\n')
            except AssertionError as e:
                print(f'Invalid Move. {e}\n')

        if not success: #if no valid move provided after K attempts, kill game
            print(f'\n\nNo valid play after {K} moves. Game over.')
            break

    winner = game.whoWins()
    winner = int(not game.getTurn())+1 if winner==None else winner+1
    winner = winner if game.totalTurns()<tie_end else 0

    if display: 
        game.display()

        if game.totalTurns()==tie_end:
            print('Draw!')
        else:
            print('Player',winner,'wins!')
            print('Total Turns',game.totalTurns())
    
    while True:
        menu = input("\nMenu:\n Replay Game (r)\n Save Game (s)\n Continue (any key)\n\n")
        print()

        if menu == 'r':
            print('Replaying Game')
            game.replay()
            continue
        elif menu == 's':
            filename = input('Enter filename: ')
            game.save(filename)
            continue
        else:
            break

    return winner
if __name__ == "__main__":
    
    # Keep Playing?
    while True:
        _ = play()
        cont = input('Play again? (y/n): ')
        if cont.lower() != 'y'.strip():
            break


