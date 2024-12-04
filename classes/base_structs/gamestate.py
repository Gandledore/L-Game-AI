import pickle
import numpy as np

from classes.base_structs.L_piece import L_piece
from classes.base_structs.token_piece import token_piece
from classes.base_structs.action import packed_action

from typing import Union,List,Optional,Tuple,Set
from tqdm import tqdm

class gamestate():
    __slots__ = ('player','L_pieces','token_pieces','transform','token_pair_id')
    #precompute with static stuff
    _general_L_pos = []
    _general_T_pos = []
    _legalMoves = {}
    _legalMoves_path = 'legal_moves.pkl' #relative to play file
    
    _preprocessing_done = False
    
    _board = {(x,y) for x in range(1,5) for y in range(1,5)}
    _count_successors = 0
    _successors = {}
    #normalized state defined as L1 piece in upper left quadrant (x,y)<=2, long leg east (6)
    _normalized_L_tuples = [(x,y,d) for x in range(1,3) for y in range(1,3) for d in ['N','S'] if not (y==1 and d=='N')]
    
    def __init__(self, 
                 player: int = 0, 
                 L_pieces: List[L_piece] = None, 
                 token_pieces: Set[token_piece] = None, 
                 transform: np.ndarray = np.array([False, False, False])):
        
        self.player:int = player
        self.L_pieces: List[L_piece] = L_pieces if L_pieces is not None else [L_piece(x=1, y=3, d='N'), L_piece(x=4, y=2, d='S')]
        self.token_pieces: Set[token_piece] = token_pieces if token_pieces is not None else {token_piece(x=1, y=1), token_piece(x=4, y=4)}

        self.transform = transform
        self.renormalize()
        
        self.token_pair_id = sum(2**(token.x+4*token.y-5) for token in self.token_pieces)
        #preprocess everything
        if not gamestate._preprocessing_done:
            gamestate._precompute_gen_L_pos()
            gamestate._precompute_gen_T_pos()
            gamestate._preprocessing_done = True    
            #preprocessing below setting done=True so it doesn't recursively call itself
            # upon initialization of states in preprocessing
            gamestate._preprocess_all_legalMoves()
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
                print('\rLoaded Preprocessed States')
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
    def __eq__(self,other:"gamestate"):
        return self.token_pair_id==other.token_pair_id and self.player==other.player and self.L_pieces==other.L_pieces
    
    def compute_normalization(self)->np.ndarray[bool]:
        return self.L_pieces[0].compute_normalization()
    
    def update_normalization(self,transform:np.ndarray[bool])->None:
        if self.transform[2] and transform[0]!=transform[1]:
            transform[:2] = np.logical_not(transform[:2])
        self.transform = np.logical_xor(self.transform,transform)
        
    def normalize(self,transform):        
        #normalize the L pieces
        for piece in self.L_pieces:
            piece.normalize(transform)
        
        #'or' comprehension necessary because 
        #   1) normalize returns none
        #   2) modifying elements in a set in place changes hash and results in unexpected behavior
        self.token_pieces = {piece.normalize(transform) or piece for piece in self.token_pieces}
        self.token_pair_id = sum(2**(token.x+4*token.y-5) for token in self.token_pieces)

    #just a wrapper, cause each part of transformation is binary and independent, 
    # so doing it twice reverses it (basically an xor operation)
    def denormalize(self)->None:
        #normalize the L pieces
        for piece in self.L_pieces:
            piece.denormalize(self.transform)
        
        #'or' comprehension necessary because 
        #   1) normalize returns none
        #   2) modifying elements in a set in place changes hash and results in unexpected behavior
        self.token_pieces = {piece.denormalize(self.transform) or piece for piece in self.token_pieces}
        self.token_pair_id = sum(2**(token.x+4*token.y-5) for token in self.token_pieces)

    def renormalize(self)->None:
        partial_transform = self.compute_normalization()
        # if not all(partial_transform==self.transform):
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
            return False, f'Moved l piece collides with token(s)'
        
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
        try:
            return gamestate._successors[(self,move)]
        except KeyError:
            valid, feedback = self.valid_move(move)
            assert valid, feedback#+f'\n\nMove: {move}\nState: {self}'
            
            l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, curr_token_pos_x, curr_token_pos_y, new_token_pos_x,new_token_pos_y = move.get_rep()
            new_l_pos = (new_l_pos_x,new_l_pos_y,new_l_pos_d.decode('utf-8'))
            curr_t_pos = (curr_token_pos_x,curr_token_pos_y)
            new_t_pos = (new_token_pos_x,new_token_pos_y)
            
            state = gamestate(player=int(not self.player),
                            L_pieces=[L_piece(*new_l_pos) if self.player==i else l_piece.copy() for i,l_piece in enumerate(self.L_pieces)],
                            token_pieces={token_piece(*new_t_pos) if curr_t_pos==token.get_position() else token.copy() for token in self.token_pieces},
                            transform=self.transform.copy())
            
            #only renormalize when L1 moved
            # moving L2 doesn't change normalization 
            # (normalization defined by L1)
            if self.player==0:
                state.renormalize()
            gamestate._successors[(self,move)] = state
            gamestate._count_successors+=1
            return gamestate._successors[(self,move)]
    
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
    

    