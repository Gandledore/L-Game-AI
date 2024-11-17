from classes.players.player import Player
from classes.base_structs.action import action
from classes.base_structs.gamestate import gamestate

from typing import Tuple

CORE = {(2,2), (2,3), (3,2), (3,3)} #or try {} no commas
CORNERS = {(1,1), (1,4), (4,1), (4,4)}

class Agent(Player):
    def __init__(self, id:int, depth=2, prune:bool=True):
        super().__init__(id)
        self.depth = depth
        self.prune = prune
        visited = {} # compute heuristic once and never again, memory outside of local turn save searched states ( may be too memory intensive except for d = inf)

    def getMove(self, state: gamestate) -> action:
        print('Thinking...')
        value, bestAction = self.AlphaBetaSearch(state)
        print(f'Move: {bestAction} | Est: {value}')
        return bestAction #if bestAction else legal_moves[0] if legal_moves else None
    
    def heuristic(self, state) -> int:
        #not state.player is person who called heuristic, 
        # reward and penalize from caller's perspective
        player = not state.player
        opponent = state.player

        opponent_options_weight = -1
        core_weight = 20
        corner_weight = 40
        win_weight = 1000

        #penalize number of moves other person has
        legalmovesofother = opponent_options_weight*len(state.getLegalMoves()) #state is already the other player, just call getLegalMoves
        
        player_l_set = set(map(tuple,state.L_pieces[player].get_coords()))
        opponent_l_set = set(map(tuple,state.L_pieces[opponent].get_coords()))
        
        control_core = core_weight * len(player_l_set.intersection(CORE))    #reward controlling core
        expel_core = -1*core_weight * len(opponent_l_set.intersection(CORE))    #penalize oponent in core
        avoid_corner = -1*corner_weight * len(player_l_set.intersection(CORNERS)) #penalize touching corner
        force_corner = corner_weight * len(opponent_l_set.intersection(CORNERS)) #reward oponent being in corner

        #reward true if they lose
        winning = win_weight * (state.isGoal()) #but htis is colinear with legalmovesofother

        score = legalmovesofother + control_core + expel_core + avoid_corner + force_corner + winning
        # print ("score: ", score)
        return score

    def AlphaBetaSearch(self, state: gamestate) -> action:
        return self.MaxValueAB(state, self.depth)

    def MaxValueAB(self, state: gamestate, depth:int, alpha:float = float('-inf'), beta:float=float('inf')) -> Tuple[int, action]:
        if depth == 0 or state.isGoal():
            return self.heuristic(state), None
      
        v = float('-inf')
        move = None
        moves = state.getLegalMoves()
        numMoves = len(moves)
        for i,action in enumerate(moves):
            print(f"Max: Evaluating move {i} at depth {depth}")
            v2, _ = self.MinValueAB(state.getSuccessor(action), depth-1, alpha, beta)
            if v2 > v:
                v, move = v2, action
                alpha = max(alpha, v)
            if self.prune and v >= beta:
                print(f'Pruned {numMoves-i} actions')
                break
            print(f"Max: Evaluated move {i} at depth {depth} | Best: {v2}")
        return v, move
    

    def MinValueAB(self, state: gamestate, depth:int, alpha:float, beta:float) -> Tuple[int, action]:
        if depth == 0 or state.isGoal():
            return self.heuristic(state), None
        v = float('inf')
        
        move = None
        moves = state.getLegalMoves()
        numMoves = len(moves)
        for i,action in enumerate(moves):
            v2, _ = self.MaxValueAB(state.getSuccessor(action), depth-1, alpha, beta)
            if v2 < v:
                v, move = v2, action
                beta = min(beta, v)
            if self.prune and v <= alpha:
                print(f'Pruned {numMoves-i} actions')
                break
        return v, move
