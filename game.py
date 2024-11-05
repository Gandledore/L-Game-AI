import numpy as np

from base_structs.gamestate import gamestate # imports as class 
from base_structs.action import action

# Class Game
class Game:
# Saved
    def __init__(self):
        self.state = gamestate(); 
        self.gamemode = 0 #0 = human vs human, 1 = human vs agent, 2 = agent vs agent
        self.player = 0 # {0,1} who's turn
    
    def getLegalMoves(state):
        # get array save ingame as a set set(l1.coords) smae ofr l2
        
        #currently dummy response to test whoWins()
        ans = input("Are you stuck: ")
        if(ans=='y'):
            print('game over')
            return []
        else:
            print('game not over')
            return [1]
     
    def getInput(self):
        if self.gamemode == 0:
            wholeMoves = input(f"Player {self.player+1}: Enter xl1 yl1 dl1 tx ty tx ty: ")
        try:
            move_parts = wholeMoves.split()
            
            new_l_pos = (int(move_parts[0]), int(move_parts[1]),move_parts[2])
            # print('new l pos:',new_l_pos)

            if len(move_parts)==7:
                current_token_pos = (int(move_parts[3]), int(move_parts[4]))
                new_token_pos = (int(move_parts[5]), int(move_parts[6]))
                token_id = next((i for i, token in enumerate(self.state.token_pieces) if current_token_pos == token.get_position()), -1)
            elif len(move_parts)==3:
                current_token_pos = None
                new_token_pos = None
                token_id=None
            
            # print('current token pos:',current_token_pos)
            # print('new token pos:',new_token_pos)
            # print('token_id:',token_id)
            
            move = action(l_piece_id=self.player,new_l_pos=new_l_pos,token_id=token_id,new_token_pos=new_token_pos)
            return move

        except ValueError as e:
            print(f"Invalid input: {e}.")
            return self.getInput()

    def valid_move(self,move:action)->bool:#return True if valid move, False if invalid
        if move.token_id==-1:#check a token is at provided coords
            print('Invalid Token Position')
            return False
        
        new_l_set = set(map(tuple,move.new_l.get_coords()))
        current_L_other_set = set(map(tuple,self.state.L_pieces[not move.l_piece_id].get_coords()))
        
        if move.token_id!=None:
            other_token = self.state.token_pieces[not move.token_id]
            #check moved token isn't other token
            if move.new_token==other_token:
                print("Token moved onto other token")
                return False
            
            #check if moved token collides with either l piece
            if move.new_token.get_position() in new_l_set or move.new_token.get_position() in current_L_other_set:
                print("moved token collides with l piece")
                return False
            
            #check moved token is inside game board
            if move.new_token>4 or move.new_token<1:
                print("token not in game board")
                return False
            
            #check other token doesn't collide with moved l piece
            #already know other token doesn't collide with other l
            if other_token.get_position() in new_l_set:
                print("other token collides with moved l piece")
                return False
        else:
            #check moved l piece doesn't intersect with either token
            for i,token in enumerate(self.state.token_pieces):
                if token.get_position() in new_l_set:
                    print(f'moved l piece collides with token {i}')
                    return False
        
        #check l pieces don't collide
        if new_l_set.intersection(current_L_other_set)!=set():
            print("l pieces intersect")
            return False
        
        #check moved l piece was actually moved
        if move.new_l==self.state.L_pieces[move.l_piece_id]:
            print('l piece not moved')
            return False
        
        #check moved l piece is inside game board
        if move.new_l>4 or move.new_l<1 :
            print("l piece not in game board")
            return False
        
        return True
       
    def apply_action(self,move:action)->bool: #true if action applied successfuly, false if failed
        if not self.valid_move(move):
            return False
        self.state.L_pieces[move.l_piece_id] = move.new_l
        if move.token_id!=None:
            self.state.token_pieces[move.token_id] = move.new_token
        return True
    
    def display(self):
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
        
    def getSuccessor(state, player):
        return True
    
    def isGoal(self):
        return len(self.getLegalMoves())==0
    
    def whoWins(self):
        if self.isGoal():
            #winner is previous player
            #current player is stuck
            return int(not self.player)+1 
        return None
    
    def setGamemode(self):
        modeInput = int(input("0 = human vs human, 1 = human vs agent, 2 = agent vs agent, Enter your mode: "))
        self.gamemode = modeInput
    
    def applyAction(self,action):
        return None
    
    def next_turn(self):
        self.player = not self.player

if __name__ == "__main__":
    test = Game()
    test.setGamemode()
    test.display()
    test.getInput()

    test.display()
    test.getInput()

        

