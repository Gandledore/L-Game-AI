import numpy as np
import copy

from classes.base_structs.gamestate import gamestate # imports as class 
from classes.base_structs.action import action
from classes.base_structs.token_piece import token_piece
from classes.base_structs.L_piece import L_piece

from typing import Union,List,Optional
class Game:
    def __init__(self):
        self.state = gamestate(); 
        self.gamemode = 0 #0 = human vs human, 1 = human vs agent, 2 = agent vs agent
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
                        if (self.valid_move(state,move)):                                     #only add it if its valid
                            validActions.append(move)
            
            #consider not moving tokens only once per possible l move                    
            move = action(self.player, Lpos, None, None)
            if (self.valid_move(state,move)):                                                 #only add if L pos is valid
                validActions.append(move)
        
        #return list of valid actions
        return validActions
     
    
    # #interface for a play code to get human input MOVED TO human.py
    # def getInput(self)->action:#needs cleanup
    #     if self.gamemode == 0:
    #         wholeMoves = input(f"Player {self.player+1}: Enter xl1 yl1 dl1 tx ty tx ty: ")
    #     try:
    #         move_parts = wholeMoves.split()
     
    #         if ( (len(move_parts) != 7) and (len(move_parts) != 3) ):
    #             raise ValueError("Enter commands in specified format")
            
    #         POSSIBLE_SETS = {'0':{1,2,3,4},'1':{1,2,3,4},'2':{'N','E','S','W'}}
            
    #         for i in range(2):
    #             if int(move_parts[i]) not in POSSIBLE_SETS[str(i)]:
    #                 raise ValueError(f"L piece coordinate out of bounds. {move_parts[i]} is not in {POSSIBLE_SETS[str(i)]}")
    #         if move_parts[2] not in POSSIBLE_SETS['2']:
    #             raise ValueError(f"L piece direction invalid. {move_parts[2]} is not in {POSSIBLE_SETS['2']}")


    #         new_l_pos = (int(move_parts[0]), int(move_parts[1]),move_parts[2])

    #         if len(move_parts)==7:
    #             current_token_pos = (int(move_parts[3]), int(move_parts[4]))
    #             new_token_pos = (int(move_parts[5]), int(move_parts[6]))
    #             token_id = next((i for i, token in enumerate(self.state.token_pieces) if current_token_pos == token.get_position()), -1)
    #         elif len(move_parts)==3:
    #             current_token_pos = None
    #             new_token_pos = None
    #             token_id=None
            
    #         move = action(l_piece_id=self.player,new_l_pos=new_l_pos,token_id=token_id,new_token_pos=new_token_pos)
    #         return move

    #     except ValueError as e:
    #         print(f"Invalid input: {e}.")
    #         return self.getInput()

    #returns true if piece is entirely within board
    def withinBoard(self,piece:Union[L_piece, token_piece])->bool:
        if piece>4 or piece<1 :
            return False
        return True

    #return True if valid move, False if invalid
    #feedback to print statements describing first error that's invalid
    def valid_move(self,state:gamestate,move:action,feedback:bool=False)->bool:
        
        #check a token is at provided coords
        if move.token_id==-1:
            if feedback: print('Invalid Token Position')
            return False
        
        # turn coords of l pieces into sets to check overlap quickly
        new_l_set = set(map(tuple,move.new_l.get_coords()))
        current_L_other_set = set(map(tuple,state.L_pieces[not move.l_piece_id].get_coords()))
        
        if move.token_id!=None:
            other_token = state.token_pieces[not move.token_id]
            #check moved token isn't other token
            if move.new_token==other_token:
                if feedback: print("Token moved onto other token")
                return False
            
            #check if moved token collides with new l pos or other l piece
            if move.new_token.get_position() in new_l_set or move.new_token.get_position() in current_L_other_set:
                if feedback: print("moved token collides with l piece")
                return False
            
            #check moved token is inside game board
            if not self.withinBoard(move.new_token):
                if feedback: print("token not in game board")
                return False
            
            #check other token doesn't collide with moved l piece
            #already know other token doesn't collide with other l
            if other_token.get_position() in new_l_set:
                if feedback: print("other token collides with moved l piece")
                return False
        
        #check that moved l piece intersects with neither current token (because L piece moves first)
        for i,token in enumerate(state.token_pieces):
            if token.get_position() in new_l_set:
                if feedback: print(f'moved l piece collides with token {i}')
                return False
    
        #check l pieces don't collide
        if new_l_set.intersection(current_L_other_set)!=set():
            if feedback: print("l pieces intersect")
            return False
        
        #check moved l piece was actually moved
        if move.new_l==state.L_pieces[move.l_piece_id]:
            if feedback: print('l piece not moved')
            return False
        
        #check moved l piece is inside game board
        if not self.withinBoard(move.new_l):
            if feedback: print("l piece not in game board")
            return False
        
        return True
    
    #updates game state with action if it is valid, returns true iff successfuly
    #feedback passed through to valid moves
    def apply_action(self,state:gamestate,move:action,feedback:bool=True)->bool:
        if not self.valid_move(state,move,feedback):
            return False
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
        if self.apply_action(copy_state,move,False):
            return copy_state
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
    
    #sets game mode MOVED TO play.py
    # def setGamemode(self)->None:
    #     modeInput = int(input("0 = human vs human\n1 = human vs agent\n2 = agent vs agent\nEnter your mode: "))
    #     self.gamemode = modeInput
    
    #updates turn
    def next_turn(self)->None:
        self.player = int(not self.player)

if __name__ == "__main__":
    print("run python3 play.py instead")
    test = Game()
    test.setGamemode()
    test.display()
    test.getInput()

    test.display()
    test.getInput()

        

