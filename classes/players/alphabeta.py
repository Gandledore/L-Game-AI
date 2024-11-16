from classes.players.player import Player
from classes.base_structs.action import action
from classes.base_structs.gamestate import gamestate

from typing import Tuple
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
    
    def evaluateState(self, state: gamestate) -> int:
       winner = state.whoWins()
       if winner is not None:
           return 1 if winner == self.player else -1
       return 0 

    # function ALPHA-BETA-SEARCH(game, state) returns an action
    def AlphaBetaSearch(self, state: gamestate, depth) -> action:
    #     player <- game.TO-MOVE(state)
        player = state.player
        alpha = float('-inf')
        beta = float('inf')
    #     value, move <- MAX-VALUE(game, state, -inf, +inf)
    #     value, move = self.MaxValueAB(game, state, float('-inf'), float('inf'), depth)
    # #     return move
    #     return move
        if state.isGoal() or depth ==0:
            return self.evaluateState(state), state.getLegalMoves()[0]
        if player == 0:
            return self.MaxValueAB(state, alpha, beta, depth, player)
        else:
            return self.MinValueAB(state, alpha, beta, depth, player)
    # function MAX-VALUE(game, state, alpha, beta) returns a (utility, move) pair
    def MaxValueAB(self, state: gamestate, alpha, beta, depth:int, player) -> Tuple[int, action]:
    #     if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
        # if game.isGoal(state):
        #     return (game.whoWins(state), None)
        if depth == 0:
            return 0, None
    #     v <- -inf
        v = float('-inf')
    #     for each a in game.ACTIONS(state) do
        move = None
        for i,action in enumerate(state.getLegalMoves()):
            # print(f"Max: Evaluating move {i} at depth {depth}")
    #         v2, a2 <- MIN-VALUE(game, game.RESULT(state, a), alpha, beta)
            v2, _ = self.MinValueAB(state.getSuccessor(action), alpha, beta, depth-1, 1)
    #         if v2 > v then
            if v2 > v:
    #             v, move <- v2, a
                v, move = v2, action
    #         alpha <- MAX(alpha, v)
                alpha = max(alpha, v)
    #         if v >= beta then return v, move
            if v >= beta:
                return v, move
    #     return v, move
        return v, move

    # function MIN-VALUE(game, state, alpha, beta) returns a (utility, move) pair
    def MinValueAB(self, state: gamestate, alpha, beta, depth:int, player) -> Tuple[int, action]:
    #     if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
        # if game.isGoal(state):
        #     return (game.whoWIns(state), None)
        if depth == 0:
            return 0, None
    #     v <- +inf
        v = float('inf')
    #     for each a in game.ACTIONS(state) do
        move = None
        
        for i,action in enumerate(state.getLegalMoves()):
    #         v2, a2 <- MAX-VALUE(game, game.RESULT(state, a), alpha, beta)
            v2, _ = self.MaxValueAB(state.getSuccessor(action), alpha, beta, depth-1, 0)
    #         if v2 < v then
            if v2 < v:
    #             v, move <- v2, a
                v, move = v2, action
    #         beta <- MIN(beta, v)
                beta = min(beta, v)
    #         if v <= alpha then return v, move
            if v <= alpha:
                return v, move
    #     return v, move
        return v, move
