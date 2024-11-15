from classes.players.player import Player
from classes.base_structs.action import action
from classes.base_structs.gamestate import gamestate

from typing import Tuple
class Agent(Player):
    def __init__(self,id:int,depth=2):
        super().__init__(id)
        self.depth = depth
        self.visited = set()
        
    def getMove(self, state: gamestate) -> action:
        print('Thinking...')
        bestAction = self.MinimaxSearch(state, self.depth)
        print('Move:',bestAction)
        return bestAction #if bestAction else legal_moves[0] if legal_moves else None

    # function MINIMAX-SEARCH(game, state) returns an action
    def MinimaxSearch(self, state:gamestate, depth:int) -> action:
    #     player <- game.TO-MOVE(state)
        player = state.player
    #     value, move <- MAX-VALUE(game, state)
        value, move = self.MaxValue(state, depth)
    #     return move
        return move

    # function MAX-VALUE(game, state) returns a (utility, move) pair
    def MaxValue(self, state:gamestate, depth:int) -> Tuple[int, action]:
    #     if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
        if state.isGoal():
            return 1, None # value is 0 -1 or 1
        if depth == 0:
            return 0, None
    #     v <- -inf
        v = -float('inf')
    #     for each a in game.ACTIONS(state) do
        print(len(state.getLegalMoves()))
        for i,action in enumerate(state.getLegalMoves()):
            print(f"Max: Evaluating move {i} at depth {depth}")
    #         v2, a2 <- MIN-VALUE(game, game.RESULT(state, a))
            v2, a2 = self.MinValue(state.getSuccessor(action), depth-1)
    #         if v2 > v then
            if v2 > v:
    #             v, move <- v2, a
                v, move = v2, a2
    #     return v, move
            print(f"Max:  Evaluated move {i} at depth {depth}")
        return v, move

    # function MIN-VALUE(game, state) returns a (utility, move) pair
    def MinValue(self, state:gamestate, depth:int) -> Tuple[int, action]:
    #     if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
        if state.isGoal():
            return -1, None
        if depth == 0:
            return 0, None
    #     v <- +inf
        v = float('inf')
    #     for each a in game.ACTIONS(state) do
        print(len(state.getLegalMoves()))
        for i,action in enumerate(state.getLegalMoves()):
    #         v2, a2 <- MAX-VALUE(game, game.RESULT(state, a))
            # print(f"Min: Evaluating move {i} at depth {depth}")
            v2, a2 = self.MaxValue(state.getSuccessor(action), depth-1)
    #         if v2 < v then
            if v2 < v:
    #         v, move <- v2, a
                v, move = v2, a2
            # print(f"Min:  Evaluated move {i} at depth {depth}")
    #     return v, move
        return v, move
