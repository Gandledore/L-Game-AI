from classes.players.player import Player
from classes.base_structs.action import action
from classes.base_structs.gamestate import gamestate

from typing import Tuple

CORE = {(2,2), (2,3), (3,2), (3,3)} #or try {} no commas
CORNERS = {(1,1), (1,4), (4,1), (4,4)}

class AlphaBeta(Player):
    def __init__(self, id:int, depth=2):
        super().__init__(id)
        self.depth = depth
        visited = set()

    def getMove(self, state: gamestate) -> action:
        print('Thinking...')
        _, bestAction = self.AlphaBetaSearch(state, self.depth)
        print('Move:',bestAction)
        return bestAction #if bestAction else legal_moves[0] if legal_moves else None
    
    def heuristic(self, state) -> int:
        player = state.player
        w1 = 100
        w2 = 50
        w3 = -50
        w4 = 150

        legalmovesofother = w1*len(state.getLegalMoves()) #state is already the other player, just call getLegalMoves

        #Tiles In Core
        #get hte intersectoin between Lcoords and the fixed core 2,2 2,3 3,2 3,3 define CORE outside as a const 
        #CORE = set((2,2), (2,3), (3,2), (3,3))
        print (state.L_pieces[player].get_coords())
        l_set = set(map(tuple,state.L_pieces[player].get_coords()))
        tilesincore = w2 * len(l_set.intersection(CORE))

        inthecorner = w3 * len(l_set.intersection(CORNERS))


        winning = w4 * (state.isGoal()) # this means other opersons is good.  but htis is colinear with legalmovesofother

        score = legalmovesofother + tilesincore + inthecorner + winning
        print ("score: ", score)
        return score


    # def evaluateState(self, state: gamestate) -> int:
    #    winner = state.whoWins()
    #    if winner is not None:
    #        return heuristic(state)
    #     #    return 1 if winner == self.player else -1
    #    return 0 

    # function ALPHA-BETA-SEARCH(game, state) returns an action
    def AlphaBetaSearch(self, state: gamestate, depth) -> action:
        player = state.player
        alpha = float('-inf')
        beta = float('inf')

        if state.isGoal() or depth ==0:
            return self.heuristic(state), state.getLegalMoves()[0]
        if player == 0:
            return self.MaxValueAB(state, alpha, beta, depth, player)
        else:
            return self.MinValueAB(state, alpha, beta, depth, player)
        
    def MaxValueAB(self, state: gamestate, alpha, beta, depth:int, player) -> Tuple[int, action]:
        if depth==0 or state.isGoal():
            return self.heuristic(state), None
        v = float('-inf')
        move = None
        for i,action in enumerate(state.getLegalMoves()):
            # print(f"Max: Evaluating move {i} at depth {depth}")
            v2, _ = self.MinValueAB(state.getSuccessor(action), alpha, beta, depth-1, player+1)
            if v2 > v:
                v, move = v2, action
                alpha = max(alpha, v)
            if v >= beta:
                break
        return v, move

    def MinValueAB(self, state: gamestate, alpha, beta, depth:int, player) -> Tuple[int, action]:
        if depth==0 or state.isGoal():
            return self.heuristic(state), None
        v = float('inf')
        move = None
        
        for i,action in enumerate(state.getLegalMoves()):
            v2, _ = self.MaxValueAB(state.getSuccessor(action), alpha, beta, depth-1, player-1)
            if v2 < v:
                v, move = v2, action
                beta = min(beta, v)
            if v <= alpha:
                break
        return v, move
