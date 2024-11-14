from classes.players.player import Player
from classes.base_structs.action import action
from classes.game import Game

class Agent(Player):
    def getMove(self, game: Game) -> action:
        legal_moves = game.getLegalMoves(game.state)
        # return legal_moves[0] if legal_moves else None
        state = game.state
        depth = 2
        bestAction = self.AlphaBetaSearch(game, state, depth)
        print(bestAction)
        return bestAction if bestAction else legal_moves[0] if legal_moves else None

    # function MINIMAX-SEARCH(game, state) returns an action
    def MinimaxSearch(self, game: Game, state, depth) -> action:
    #     player <- game.TO-MOVE(state)
        player = game.player
    #     value, move <- MAX-VALUE(game, state)
        value, move = self.MaxValue(game, state, depth)
    #     return move
        return move

    # function MAX-VALUE(game, state) returns a (utility, move) pair
    def MaxValue(self, game, state, depth) -> (int, action):
    #     if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
        if game.isGoal(state):
            return (game.whoWins(state), None) # value is 0 -1 or 1
        if depth == 0:
            return 0, None
    #     v <- -inf
        v = -float('inf')
    #     for each a in game.ACTIONS(state) do
        print(len(game.getLegalMoves(state)))
        for action in game.getLegalMoves(state):
            print(f"Evaluating move {action} at depth {depth}")
    #         v2, a2 <- MIN-VALUE(game, game.RESULT(state, a))
            v2, a2 = self.MinValue(game, game.getSuccessor(state, action), depth-1)
    #         if v2 > v then
            if v2 > v:
    #             v, move <- v2, a
                v, move = v2, a2
    #     return v, move
        return v, move

    # function MIN-VALUE(game, state) returns a (utility, move) pair
    def MinValue(self, game, state, depth) -> (int, action):
    #     if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
        if game.isGoal(state):
            return (game.whoWins(state), None)
        if depth == 0:
            return 0, None
    #     v <- +inf
        v = float('inf')
    #     for each a in game.ACTIONS(state) do
        for action in game.getLegalMoves(state):
    #         v2, a2 <- MAX-VALUE(game, game.RESULT(state, a))
            v2, a2 = self.MaxValue(game, game.getSuccessor(state, action), depth-1)
    #         if v2 < v then
            if v2 < v:
    #         v, move <- v2, a
                v, move = v2, a2
    #     return v, move
        return v, move





    # function ALPHA-BETA-SEARCH(game, state) returns an action
    def AlphaBetaSearch(self, game: Game, state, depth) -> action:
    #     player <- game.TO-MOVE(state)
        player = game.player
    #     value, move <- MAX-VALUE(game, state, -inf, +inf)
        value, move = self.MaxValueAB(game, state, float('-inf'), float('inf'), depth)
    #     return move
        return move

    # function MAX-VALUE(game, state, alpha, beta) returns a (utility, move) pair
    def MaxValueAB(self, game, state, alpha, beta, depth) -> (int, action):
    #     if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
        if game.isGoal(state):
            return (game.whoWins(state), None)
        if depth == 0:
            return 0, None
    #     v <- -inf
        v = float('-inf')
    #     for each a in game.ACTIONS(state) do
        legalMoves = game.getLegalMoves(state);
        for action in legalMoves:
            print(f"Evaluating move {action} at depth {depth}")
    #         v2, a2 <- MIN-VALUE(game, game.RESULT(state, a), alpha, beta)
            v2, a2 = self.MinValueAB(game, game.getSuccessor(state, action), alpha, beta, depth-1)
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
    def MinValueAB(self, game, state, alpha, beta, depth) -> (int, action):
    #     if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
        if game.isGoal(state):
            return (game.whoWIns(state), None)
        if depth == 0:
            return 0, None
    #     v <- +inf
        v = float('inf')
    #     for each a in game.ACTIONS(state) do
        legalMoves = game.getLegalMoves(state);
        for action in legalMoves:
    #         v2, a2 <- MAX-VALUE(game, game.RESULT(state, a), alpha, beta)
            v2, a2 = self.MaxValueAB(game, game.getSuccessor(state, action), alpha, beta, depth-1)
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
