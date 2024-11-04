from base_structs.gamestate import gamestate # imports as class 
import numpy as np

# Class Game
class Game:
# Saved
    def __init__(self):
        self.state = gamestate(); 
        self.gamemode = 0 #0 = human vs human, 1 = human vs agent, 2 = agent vs agent
        self.player = 0 # 0 and 1
    
    def getLegalMoves(state):
        # get array save ingame as a set set(l1.coords) smae ofr l2
        return None
    
    def getInput(self):
        if self.gamemode == 0:
            wholeMoves = input(f"Player {self.player+1}: Enter xl1 yl1 dl1 tx ty tx ty: ")
        try:
            move_parts = wholeMoves.split()

            Lx, Ly = int(move_parts[0]), int(move_parts[1])
            Ld = move_parts[2]

            Tx, Ty, newTx, newTy = int(move_parts[3]), int(move_parts[4]), int(move_parts[5]), int(move_parts[6])
        
            
            if self.gamemode == 0 and self.player == 0:
                # self.state.L1.newPos(Lx, Ly, Ld)
                self.state.L1.x = Lx
                self.state.L1.y = Ly
                self.state.L1.short_leg_direction = Ld
                self.state.L1.p0, self.state.L1.p1, self.state.L1.p2, self.state.L1.p3= self.state.L1.compute_L_coords()
                self.player = 1
            else:
                self.state.L2.x = Lx
                self.state.L2.y = Ly
                self.state.L2.short_leg_direction = Ld
                self.state.L2.p0, self.state.L2.p1, self.state.L2.p2, self.state.L2.p3= self.state.L2.compute_L_coords()
                self.player = 0

            if (Tx !=0 or Ty!=0 or newTx!=0 or newTy!=0):
                    if (self.state.T1.x == Tx and self.state.T1.y == Ty):
                        self.state.T1.x = newTx
                        self.state.T1.y = newTy
                    elif (self.state.T2.x == Tx and self.state.T2.y == Ty):
                        self.state.T2.x = newTx
                        self.state.T2.y = newTy
                    else:
                        print("No coin at (",Tx,", ", Ty, ")")

            self.display()

   
                    
        except ValueError as e:
            print(f"Invalid input: {e}.")
            return self.getInput()  

    def display(self):
        board = np.full((4, 4), "  ") # 4 by 4 of empty string
        
        # print(self.state.L1.p0, self.state.L1.p1, self.state.L1.p2, self.state.L1.p3)
        for px, py in [self.state.L1.p0, self.state.L1.p1, self.state.L1.p2, self.state.L1.p3]:
            board[py-1, px-1] = "L1"
        for px, py in [self.state.L2.p0, self.state.L2.p1, self.state.L2.p2, self.state.L2.p3]:
            board[py-1, px-1] = "L2" 
      
        T1x, T1y = self.state.T1.get_position()
        board[T1y - 1, T1x - 1] = "T1"

        T2x, T2y = self.state.T2.get_position()
        board[T2y - 1, T2x - 1] = "T2"


        rows = ["|" + "|".join(f"{cell:>2}" for cell in row) + "|" for row in board]
        #left wall then the row then the ending right wall
        # f"{cell:>2}" align cell to the right > with a width of 2 spaces. 

        horizontal_separator = "-------------\n"
        
        board_str = horizontal_separator + f"\n{horizontal_separator}".join(rows) + "\n" + horizontal_separator
        print(board_str)
        
    def getSuccessor(state, player):
        return True
    
    def isGoal(self):
        return True
    
    def setGamemode(self):
        modeInput = int(input("0 = human vs human, 1 = human vs agent, 2 = agent vs agent, Enter your mode: "))
        self.gamemode = modeInput
    
    def applyAction(action):
        return None


if __name__ == "__main__":
    test = Game()
    test.setGamemode()
    test.display()
    test.getInput()

    test.display()
    test.getInput()

        

