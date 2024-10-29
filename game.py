from base_structs.gamestate import gamestate # imports as class 
import numpy as np

# Class Game
class Game:
# Saved
    def __init__(self):
        self.state = gamestate(); 
        self.gamemode = 0 #0 = human vs human, 1 = human vs agent, 2 = agent vs agent
        self.player = 0; 
    
    def getLegalMoves(state):
        return None
    def getInput():
        inputs = input();
        return inputs;
    def display(self):
        board = np.full((4, 4), "XX") # 4 by 4 of empty string
        
       
        for px, py in [self.state.L1.p0, self.state.L1.p1, self.state.L1.p2, self.state.L1.p3]:
            board[3 - (py - 1), px - 1] = "L1" 
        for px, py in [self.state.L2.p0, self.state.L2.p1, self.state.L2.p2, self.state.L2.p3]:
            board[3 - (py - 1), px - 1] = "L2" 
      
        T1x, T1y = self.state.T1.get_position()
        board[3 - (T1y - 1), T1x - 1] = "T1"

        T2x, T2y = self.state.T2.get_position()
        board[3 - (T2y - 1), T2x - 1] = "T2"

        

        rows = ["|" + "|".join(f"{cell:>2}" for cell in row) + "|" for row in board]
        #left wall then the row then the ending right wall
        # f"{cell:>2}" align cell to the right > with a width of 2 spaces. 

        horizontal_separator = "-------------\n"
        
        board_str = horizontal_separator + f"\n{horizontal_separator}".join(rows) + "\n" + horizontal_separator
        print(board_str)
        
    def getSuccessor(state, player):
        return True
    def isGoal():
        return True
    def setGamemode(mode):
        self.gamemode = mode;
    def applyAction(action):
        return None


if __name__ == "__main__":
    test = Game()
    test.display()
        

