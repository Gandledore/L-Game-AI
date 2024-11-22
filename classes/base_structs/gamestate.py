import pickle
import time
import os
import numpy as np

from classes.base_structs.L_piece import L_piece
from classes.base_structs.token_piece import token_piece
from classes.base_structs.action import packed_action

from typing import Union,List,Optional,Tuple,Callable
from tqdm import tqdm

class gamestate():
    #precompute with static stuff
    _general_L_pos = []
    _general_T_pos = []
    _general_pos_set = set()
    _legalMoves = {}
    _cache_hits = 0
    _cache_misses = 0
    _preprocessing_done = False
    
    _board = {(x,y) for x in range(1,5) for y in range(1,5)}

    def __init__(self, player:int=0, L_pieces:List[L_piece]=[L_piece(x=1,y=3,d='N'),L_piece(x=4,y=2,d='S')], token_pieces:List[token_piece]=[token_piece(x=1,y=1),token_piece(x=4,y=4)]):
        self.player = player
        self.L_pieces = L_pieces
        self.token_pieces = token_pieces
        
        if not gamestate._preprocessing_done:
            gamestate._precompute_gen_L_pos()
            gamestate._precompute_gen_T_pos()
            gamestate._preprocessing_done = True    
            #preprocessing below setting done=True so it doesn't recursively call itself
            # upon initialization of states in preprocessing
            gamestate._preprocess_all_legalMoves()

    #precompute L positions that are generally possible, assuming no other pieces on the board (ie within board)
    @classmethod
    def _precompute_gen_L_pos(cls):
        for x in L_piece._POSSIBLE_LISTS['x']:
            for y in L_piece._POSSIBLE_LISTS['y']:
                for d in L_piece._POSSIBLE_LISTS['d']:
                    l = L_piece(x=x,y=y,d=d)
                    if cls._withinBoard(l):
                        cls._general_L_pos.append((x,y,d))
                        cls._general_pos_set.add((x,y,d))

    #precompute T positions that are generally possible, assuming no other pieces on board (ie within board)
    @classmethod
    def _precompute_gen_T_pos(cls):
        for x in token_piece._POSSIBLE_LISTS['x']:
            for y in token_piece._POSSIBLE_LISTS['y']:
                cls._general_T_pos.append((x,y))#don't need to check within board, cause they are size 1x1
                cls._general_pos_set.add((x,y))
                
    #returns true if piece is entirely within board
    @classmethod
    def _withinBoard(cls,piece:Union[L_piece, token_piece])->bool:
        return piece.get_coords() <= cls._board
    
    @classmethod 
    def _compute_legalMoves(cls,state:"gamestate"):
        #create list of possible actions
        validActions = []
        for Lpos in cls._general_L_pos:                                                 #possible positions L can move in general
            #consider not moving tokens only once per possible l move  
            #consider not moving first because this checks if L move is even possible                  
            move = packed_action(state.player, Lpos, 255, (0,0))
            if state.valid_move(move)[0]:
                validActions.append(move)
                
                #if L piece fails, no point trying tokens
                for T in range(len(state.token_pieces)):
                    for Tpos in cls._general_T_pos:
                        if (Tpos != state.token_pieces[T].get_position()):                   #only consider you moving the token.
                            move = packed_action(state.player, Lpos, T, Tpos)
                            if (state.valid_move(move)[0]):                                  #only add it if its valid
                                validActions.append(move)
        
        cls._legalMoves[state] = np.array(validActions)
    
    @classmethod 
    def _preprocess_all_legalMoves(cls):
        """saves a dictionary mapping any state to a list of the legal moves from that state

            generates all possible states by iterating throough all valid L1 placements
                all valid L2 placements given the L1 position, all valid T1 positions
                given L1 and L2, all valid T2 positions given L1,L2 and T1, 
                and both player turns given the rest

        Returns:
            int: how many states processed
        """
        try:
            with open('legal_moves.pkl','rb') as f:
                print('Loading Preprocessed States...')
                cls._legalMoves = pickle.load(f)
        except FileNotFoundError as e:
            print('Legal Moves not Preprocessed. Processing them now...')
            start = time.time()
            count=0
            for l0_pos in tqdm(cls._general_L_pos):
                l0_set = L_piece._compute_L_coords(*l0_pos)
                l0 = L_piece(*l0_pos)
                for l1_pos in cls._general_L_pos:
                    l1_set = L_piece._compute_L_coords(*l1_pos)
                    if not l0_set & l1_set:
                        l1 = L_piece(*l1_pos)
                        for t0_pos in cls._general_T_pos:
                            if not (t0_pos in l0_set or t0_pos in l1_set):
                                t0 = token_piece(*t0_pos)
                                for t1_pos in cls._general_T_pos:
                                    if not (t1_pos in l0_set or t1_pos in l1_set):
                                        if t0_pos!=t1_pos:
                                            t1 = token_piece(*t1_pos)
                                            for p in [0,1]:
                                                count+=1
                                                state = gamestate(p,[l0,l1],[t0,t1])
                                                cls._compute_legalMoves(state)
                                                # if count%100==0:
                                                #     print(f'\rProcessed {count} states in {time.time()-start:.1f}s',end='')
        return len(cls._legalMoves)
        
    def __repr__(self):
        return f" Player: {self.player}\nL pieces: {[l for l in self.L_pieces]}\nT pieces: {[t for t in self.token_pieces]}"
    def __hash__(self):
        return hash((self.player,tuple(self.L_pieces),tuple(self.token_pieces)))
    def __eq__(self,other:"gamestate"):
        return self.player==other.player and self.L_pieces==other.L_pieces and self.token_pieces==other.token_pieces
    
    #returns list of legal actions for current player
    def getLegalMoves(self)->List[packed_action]:
        cls = type(self)
        if self not in cls._legalMoves:
            cls._compute_legalMoves(self)
            cls._cache_misses+=1
        #     print(f'Cached {len(cls._legalMoves)} states')
        else:
            cls._cache_hits+=1
        #     print('Already Computed Legal moves for this state'+20*'-')
        return cls._legalMoves[self]

    #return True if valid move, False if invalid
    #feedback to for assertions statements describing first error that's invalid
    def valid_move(self,move:packed_action)->Tuple[bool,str]:
        cls = type(self)
        
        l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, token_id, new_token_pos_x,new_token_pos_y = move.get_rep()
        new_l_pos = (new_l_pos_x,new_l_pos_y,new_l_pos_d.decode('utf-8'))
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
        if not new_l_set <= cls._board:
            return False, "L piece not in game board."
        
        if token_id!=255:
            other_token = self.token_pieces[not token_id]
            
            #check if moved token collides with new l pos or other l piece
            if new_t_pos in new_l_set:
                return False, f"Moved token collides with L{l_piece_id+1} piece."
            if new_t_pos in current_L_other_set:
                return False, f"Moved token collides with L{int(not l_piece_id)+1} piece."
            
            #check token isn't moved onto other token
            if new_t_pos==other_token.get_position():
                return False, "Token moved onto other token."
            
        return True, "valid move"
    
    #take state and move, return new gamestate where move is applied
    def getSuccessor(self, move: packed_action) -> "gamestate":
        valid, feedback = self.valid_move(move)
        assert valid, feedback
        
        l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, token_id, new_token_pos_x, new_token_pos_y = move.get_rep()
        new_l_pos = (new_l_pos_x,new_l_pos_y,new_l_pos_d.decode('utf-8'))
        new_t_pos = (new_token_pos_x,new_token_pos_y)
        
        return gamestate(player=int(not self.player),
                        L_pieces=[L_piece(*new_l_pos) if self.player==i else self.L_pieces[i] for i in range(2)],
                        token_pieces=[token_piece(*new_t_pos) if token_id==i else self.token_pieces[i] for i in range(2)])
    
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
    

    