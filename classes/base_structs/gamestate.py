from classes.base_structs.L_piece import L_piece
from classes.base_structs.token_piece import token_piece
from classes.base_structs.action import action

from typing import Union,List,Optional,Tuple
import copy
class gamestate():
    def __init__(self):
        self.player = 0
        self.L_pieces = [L_piece(x=1,y=3,d='N'),L_piece(x=4,y=2,d='S')]
        self.token_pieces = [token_piece(x=1,y=1),token_piece(x=4,y=4)]

        #precompute L positions that are generally possible, assuming no other pieces on the board (ie within board)
        self.general_L_pos = []
        for x in L_piece.POSSIBLE_SETS['x']:
            for y in L_piece.POSSIBLE_SETS['y']:
                for d in L_piece.POSSIBLE_SETS['short_leg_direction']:
                    l = L_piece(x=x,y=y,d=d)
                    if self.withinBoard(l):
                        self.general_L_pos.append((x,y,d))
        
        #precompute T positions that are generally possible, assuming no other pieces on board (ie within board)
        self.general_T_pos = []
        for x in token_piece.POSSIBLE_SETS['x']:
            for y in token_piece.POSSIBLE_SETS['y']:
                self.general_T_pos.append((x,y))#don't need to check within board, cause they are size 1x1
    
    
    def __repr__(self):
        return f"L pieces: {[l for l in self.L_pieces]}\nT pieces {[t for t in self.token_pieces]}"
    def __hash__(self):
        return hash((tuple(self.L_pieces),tuple(self.token_pieces)))
    def __eq__(self,other:"gamestate"):
        return self.L_pieces==other.L_pieces and self.token_pieces==other.token_pieces
    
    #returns list of legal actions for current player
    def getLegalMoves(self)->List[action]:
        #create list of possible actions
        validActions = []
        for Lpos in self.general_L_pos:                                                 #possible positions L can move in general
            for T in range(len(self.token_pieces)):
                for Tpos in self.general_T_pos:
                    if (Tpos != self.token_pieces[T].get_position()):             #only consider you moving the token.
                        move = action(self.player, Lpos, T, Tpos)
                        if (self.valid_move(move)[0]):                                     #only add it if its valid
                            validActions.append(move)
            
            #consider not moving tokens only once per possible l move                    
            move = action(self.player, Lpos, None, None)
            if (self.valid_move(move)[0]):                                                 #only add if L pos is valid
                validActions.append(move)
        
        #return list of valid actions
        return validActions

    #returns true if piece is entirely within board
    def withinBoard(self,piece:Union[L_piece, token_piece])->bool:
        if piece>4 or piece<1 :
            return False
        return True

    #return True if valid move, False if invalid
    #feedback to for assertions statements describing first error that's invalid
    def valid_move(self,move:action)->Tuple[bool,str]:
        
        #check a token is at provided coords
        if move.token_id==-1:
            return False, 'No token in provided position.'
        
        # turn coords of l pieces into sets to check overlap quickly
        new_l_set = set(map(tuple,move.new_l.get_coords()))
        current_L_other_set = set(map(tuple,self.L_pieces[not move.l_piece_id].get_coords()))
        
        if move.token_id!=None:
            other_token = self.token_pieces[not move.token_id]
            #check moved token isn't other token
            if move.new_token==other_token:
                return False, "Token moved onto other token."
            
            #check if moved token collides with new l pos or other l piece
            if move.new_token.get_position() in new_l_set:
                return False, f"Moved token collides with L{move.l_piece_id+1} piece."
            if move.new_token.get_position() in current_L_other_set:
                return False, f"Moved token collides with L{int(not move.l_piece_id)+1} piece."
            
            
            #check moved token is inside game board
            if not self.withinBoard(move.new_token):
                return False, "Token not in game board."
            
            # #check other token doesn't collide with moved l piece
            if other_token.get_position() in new_l_set:
                return False, f"Moved l piece collides with token {int(not move.token_id)+1}"
        
        #check that moved l piece intersects with neither current token (because L piece moves first)
        #already know other token doesn't collide with other l
        for i,token in enumerate(self.token_pieces):
            if token.get_position() in new_l_set:
                return False, f'Moved l piece collides with token {i+1}'
    
        #check l pieces don't collide
        if new_l_set.intersection(current_L_other_set)!=set():
            return False, "L pieces overlap."
        
        #check moved l piece was actually moved
        if move.new_l==self.L_pieces[move.l_piece_id]:
            return False, 'L piece not moved.'
        
        #check moved l piece is inside game board
        if not self.withinBoard(move.new_l):
            return False, "L piece not in game board."
        
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
            return int(not self.state.player)
        #game is not over
        return None
    

    