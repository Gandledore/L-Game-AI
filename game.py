from base_structs import gamestate, displayer
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
        input = input();
        return input;
    def display(state):
        board = np.full((4, 4), " ") # 4 by 4 of empty string
        formatted_rows = np.array2string(board, separator="|", formatter={'str_kind': lambda x: f"{x:>2}"})
        horizontal_separator = " -------------\n"
        print(horizontal_separator + horizontal_separator.join(formatted_rows.splitlines()) + "\n" + horizontal_separator)
        
    def getSuccessor(state, player):
        return True
    def isGoal():
        return True
    def setGamemode(mode):
        self.gamemode = mode;
    def applyAction(action):
        return None


        

