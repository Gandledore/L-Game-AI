from classes.players.player import Player
from classes.base_structs.action import action
from classes.game import Game

class Agent(Player):
    def getMove(self, game: Game) -> action:
        legal_moves = game.getLegalMoves(game.state)
        return legal_moves[0] if legal_moves else None

    # function MINIMAX-SEARCH(game, state) returns an action
    #     player <- game.TO-MOVE(state)
    #     value, move <- MAX-VALUE(game, state)
    #     return move

    # function MAX-VALUE(game, state) returns a (utility, move) pair
    #     if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
    #     v <- -inf
    #     for each a in game.ACTIONS(state) do
    #         v2, a2 <- MIN-VALUE(game, game.RESULT(state, a))
    #         if v2 > v then
    #             v, move <- v2, a
    #     return v, move

    # function MIN-VALUE(game, state) returns a (utility, move) pair
    #     if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
    #     v <- +inf
    #     for each a in game.ACTIONS(state) do
    #         v2, a2 <- MAX-VALUE(game, game.RESULT(state, a))
    #         if v2 < v then
    #         v, move <- v2, a
    #     return v, move
