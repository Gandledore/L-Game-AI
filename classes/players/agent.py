from classes.players.player import Player
from classes.base_structs.action import action
from classes.game import Game

class Agent(Player):
    def getMove(self, game: Game) -> action:
        # legal_moves = game.getLegalMoves(game.state)
        # return legal_moves[0] if legal_moves else None
        state = game.state
        bestAction = MinimaxSearch(game, state)
        return bestAction

    # function MINIMAX-SEARCH(game, state) returns an action
    def MinimaxSearch(game: Game, state: state) -> action:
    #     player <- game.TO-MOVE(state)
        player = game.player
    #     value, move <- MAX-VALUE(game, state)
        value, move = MaxValue(game, state)
    #     return move
        return move

    # function MAX-VALUE(game, state) returns a (utility, move) pair
    def MaxValue(game, state) -> (value, move):
    #     if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
        if game.isGoal(state):
            return (game.whoWins(state), None) # value is 0 -1 or 1
    #     v <- -inf
        v = -float('inf')
    #     for each a in game.ACTIONS(state) do
        for action in game.getLegalMoves(state):
    #         v2, a2 <- MIN-VALUE(game, game.RESULT(state, a))
            v2, a2 = MinValue(game, game.getSuccessor(state, action))
    #         if v2 > v then
            if v2 > v:
    #             v, move <- v2, a
                v, move = v2, a2
    #     return v, move
        return v, move

    # function MIN-VALUE(game, state) returns a (utility, move) pair
    def MinValue(game, state) -> (value, move):
    #     if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
        if game.isGoal(state):
            return (game.whoWins(state), None)
    #     v <- +inf
        v = float('inf')
    #     for each a in game.ACTIONS(state) do
        for action in game.getLegalMoves(state):
    #         v2, a2 <- MAX-VALUE(game, game.RESULT(state, a))
            v2, a2 = MaxValue(game, game.getSuccessor(state, action))
    #         if v2 < v then
            if v2 < v:
    #         v, move <- v2, a
                v, move = v2, a2
    #     return v, move
        return v, move
