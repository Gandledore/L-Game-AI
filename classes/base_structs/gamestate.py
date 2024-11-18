from classes.base_structs.L_piece import L_piece
from classes.base_structs.token_piece import token_piece
from classes.base_structs.action import action

from typing import Union,List,Optional,Tuple
import copy

class gamestate():
    #precompute with static stuff
    _count = 0
    _general_L_pos = []
    _general_T_pos = []
    _general_pos_set = set()
    _legalMoves = {}
    _cache_hits = 0
    _cache_misses = 0
    _preprocessing_done = False
    
    def __init__(self):
        self.player = 0
        self.L_pieces = [L_piece(x=1,y=3,d='N'),L_piece(x=4,y=2,d='S')]
        self.token_pieces = [token_piece(x=1,y=1),token_piece(x=4,y=4)]
        gamestate._count+=1
        if not gamestate._preprocessing_done:
            gamestate._precompute_gen_L_pos()
            gamestate._precompute_gen_T_pos()
            gamestate._preprocessing_done = True
            
    #precompute L positions that are generally possible, assuming no other pieces on the board (ie within board)
    @classmethod
    def _precompute_gen_L_pos(cls):
        for x in L_piece.POSSIBLE_LISTS['x']:
            for y in L_piece.POSSIBLE_LISTS['y']:
                for d in L_piece.POSSIBLE_LISTS['short_leg_direction']:
                    l = L_piece(x=x,y=y,d=d)
                    if cls._withinBoard(l):
                        cls._general_L_pos.append((x,y,d))
                        cls._general_pos_set.add((x,y,d))
    
    #precompute T positions that are generally possible, assuming no other pieces on board (ie within board)
    @classmethod
    def _precompute_gen_T_pos(cls):
        for x in token_piece.POSSIBLE_LISTS['x']:
            for y in token_piece.POSSIBLE_LISTS['y']:
                cls._general_T_pos.append((x,y))#don't need to check within board, cause they are size 1x1
                cls._general_pos_set.add((x,y))
                
    #returns true if piece is entirely within board
    @classmethod
    def _withinBoard(cls,piece:Union[L_piece, token_piece])->bool:
        if cls._preprocessing_done:
            return piece.get_tuple() in cls._general_pos_set
        if piece>4 or piece<1:
            return False
        return True
    
    @classmethod 
    def _compute_legalMoves(cls,state:"gamestate"):
        #create list of possible actions
        validActions = []
        for Lpos in cls._general_L_pos:                                                 #possible positions L can move in general
            #consider not moving tokens only once per possible l move  
            #consider not moving first because this checks if L move is even possible                  
            move = action(state.player, Lpos, None, None)
            if (state.valid_move(move)[0]): 
                validActions.append(move)
                
                #skip trying to move any tokens, cause L piece moved first
                for T in range(len(state.token_pieces)):
                    for Tpos in cls._general_T_pos:
                        if (Tpos != state.token_pieces[T].get_position()):                   #only consider you moving the token.
                            move = action(state.player, Lpos, T, Tpos)
                            if (state.valid_move(move)[0]):                                  #only add it if its valid
                                validActions.append(move)

        cls._legalMoves[state] = validActions
        
    def __repr__(self):
        return f"L pieces: {[l for l in self.L_pieces]}\nT pieces {[t for t in self.token_pieces]}"
    def __hash__(self):
        return hash((self.player,tuple(self.L_pieces),tuple(self.token_pieces)))
    def __eq__(self,other:"gamestate"):
        return self.player==other.player and self.L_pieces==other.L_pieces and self.token_pieces==other.token_pieces
    def __deepcopy__(self, memo):
        cls = type(self)
        new_copy = cls.__new__(cls)  # Create a new instance without calling __init__
        memo[id(self)] = new_copy    # Avoid infinite recursion
        new_copy.__dict__ = copy.deepcopy(self.__dict__, memo)  # Deepcopy instance attributes
        cls._count += 1             # Increment the counter for the new copy
        return new_copy
    
    #returns list of legal actions for current player
    def getLegalMoves(self)->List[action]:
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
    def valid_move(self,move:action)->Tuple[bool,str]:
        cls = type(self)
        #check a token is at provided coords
        if move.token_id==-1:
            return False, 'No token in provided position.'
        
        #check moved l piece was actually moved
        if move.new_l==self.L_pieces[move.l_piece_id]:
            return False, 'L piece not moved.'
        
        # turn coords of l pieces into sets to check overlap quickly
        new_l_set = set(map(tuple,move.new_l.get_coords()))
        current_L_other_set = set(map(tuple,self.L_pieces[not move.l_piece_id].get_coords()))
        
        #check l pieces don't collide
        if len(new_l_set.intersection(current_L_other_set))!=0:
            return False, "L pieces overlap."
        
        #check that moved l piece intersects with neither current token (because L piece moves first)
        #already know other token doesn't collide with other l
        for i,token in enumerate(self.token_pieces):
            if token.get_position() in new_l_set:
                return False, f'Moved l piece collides with token {i+1}'
        
        #check moved l piece is inside game board
        if not cls._withinBoard(move.new_l):
            return False, "L piece not in game board."
        
        if move.token_id!=None:
            other_token = self.token_pieces[not move.token_id]
            #check if moved token collides with new l pos or other l piece
            if move.new_token.get_position() in new_l_set:
                return False, f"Moved token collides with L{move.l_piece_id+1} piece."
            if move.new_token.get_position() in current_L_other_set:
                return False, f"Moved token collides with L{int(not move.l_piece_id)+1} piece."
            
            #check moved token isn't other token
            if move.new_token==other_token:
                return False, "Token moved onto other token."
            
            #not necessary because token construction asserts position within gameboard
            #check moved token is inside game board
            # if not cls._withinBoard(move.new_token):
            #     return False, "Token not in game board."
            
        return True, "valid move"
    
    #take state and move, return new gamestate where move is applied
    def getSuccessor(self, move:action)->"gamestate":
        valid, feedback = self.valid_move(move)
        assert valid, feedback
        state = copy.deepcopy(self)
        state.player = int(not self.player)
        state.L_pieces[move.l_piece_id] = move.new_l
        if move.token_id!=None:
            state.token_pieces[move.token_id] = move.new_token
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
    

    