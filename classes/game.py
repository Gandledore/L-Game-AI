import numpy as np
import copy

from classes.base_structs.gamestate import gamestate # imports as class 
from classes.base_structs.action import action
from classes.base_structs.token_piece import token_piece
from classes.base_structs.L_piece import L_piece

from typing import Union,List,Optional,Tuple
class Game:
    def __init__(self):
        self.state = gamestate(); 
        self.player = 0 # {0,1} who's turn
        
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
        
    #returns list of legal actions for current player
    def getLegalMoves(self,state:gamestate)->List[action]:
        #create list of possible actions
        validActions = []
        for Lpos in self.general_L_pos:                                                 #possible positions L can move in general
            for T in range(len(state.token_pieces)):
                for Tpos in self.general_T_pos:
                    if (Tpos != state.token_pieces[T].get_position()):             #only consider you moving the token.
                        move = action(self.player, Lpos, T, Tpos)
                        if (self.valid_move(state,move)[0]):                                     #only add it if its valid
                            validActions.append(move)
            
            #consider not moving tokens only once per possible l move                    
            move = action(self.player, Lpos, None, None)
            if (self.valid_move(state,move)[0]):                                                 #only add if L pos is valid
                validActions.append(move)
        
        #return list of valid actions
        return validActions

    #returns true if piece is entirely within board
    def withinBoard(self,piece:Union[L_piece, token_piece])->bool:
        if piece>4 or piece<1 :
            return False
        return True

    #return True if valid move, False if invalid
    #feedback to print statements describing first error that's invalid
    def valid_move(self,state:gamestate,move:action)->Tuple[bool,str]:
        
        #check a token is at provided coords
        if move.token_id==-1:
            return False, 'No token in provided position.'
        
        # turn coords of l pieces into sets to check overlap quickly
        new_l_set = set(map(tuple,move.new_l.get_coords()))
        current_L_other_set = set(map(tuple,state.L_pieces[not move.l_piece_id].get_coords()))
        
        if move.token_id!=None:
            other_token = state.token_pieces[not move.token_id]
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
        for i,token in enumerate(state.token_pieces):
            if token.get_position() in new_l_set:
                return False, f'Moved l piece collides with token {i+1}'
    
        #check l pieces don't collide
        if new_l_set.intersection(current_L_other_set)!=set():
            return False, "L pieces overlap."
        
        #check moved l piece was actually moved
        if move.new_l==state.L_pieces[move.l_piece_id]:
            return False, 'L piece not moved.'
        
        #check moved l piece is inside game board
        if not self.withinBoard(move.new_l):
            return False, "L piece not in game board."
        
        return True, "valid move"
    
    #updates game state with action if it is valid, returns true iff successfuly
    #feedback passed through to valid moves
    def apply_action(self,state:gamestate,move:action)->bool:
        valid, feedback = self.valid_move(state,move)
        assert valid, feedback
        
        state.L_pieces[move.l_piece_id] = move.new_l
        if move.token_id!=None:
            state.token_pieces[move.token_id] = move.new_token
        return True
    
    #interface to display game board and pieces
    def display(self)->None:
        board = np.full((4, 4), "  ") # 4 by 4 of empty string
        
        for i,l in enumerate(self.state.L_pieces):
            for px, py in l.get_coords():
                board[py-1, px-1] = "L"+str(i+1)

        for i,t in enumerate(self.state.token_pieces):
            tx, ty = t.get_position()
            board[ty - 1, tx - 1] = "T"+str(i+1)


        rows = ["|" + "|".join(f"{cell:>2}" for cell in row) + "|" for row in board]
        #left wall then the row then the ending right wall
        # f"{cell:>2}" align cell to the right > with a width of 2 spaces. 

        horizontal_separator = "-------------\n"
        
        board_str = horizontal_separator + f"\n{horizontal_separator}".join(rows) + "\n" + horizontal_separator
        print(board_str)
    
    #ASSUMES PROVIDED MOVE IS VALID
    #take state and move, return new gamestate where move is applied
    def getSuccessor(self, state:gamestate, move:action)->Optional[gamestate]:
        copy_state = copy.deepcopy(state)
        try:
            self.apply_action(copy_state,move)
            return copy_state
        except AssertionError as e:
            print(f'Invalid move {e}')
            return None
    
    #checks state is goal
    def isGoal(self,state:gamestate)->bool:
        #game over when no legal moves available
        return len(self.getLegalMoves(state))==0
    
    #checks who wins. Either None, 0 or 1
    def whoWins(self,state)->Optional[int]:
        if self.isGoal(state):
            #winner is previous player
            #current player is stuck
            return int(not self.player)
        #game is not over
        return None
    
    #updates turn
    def next_turn(self)->None:
        self.player = int(not self.player)

if __name__ == "__main__":
    print("run python3 play.py instead")
    test = Game()
    test.display()
    test.getInput()

    test.display()
    test.getInput()

        

