from classes.players.player import Player
from classes.base_structs.action import packed_action
from classes.base_structs.gamestate import gamestate
from classes.base_structs.L_piece import L_piece

from typing import Tuple
import time
import numpy as np


class Agent(Player):
    _CORE = {(2,2), (2,3), (3,2), (3,3)}
    _CORNERS = {(1,1), (1,4), (4,1), (4,4)}
    _KILLER_TOKENS = {(2,1), (3,1), (1,2), (1,3), (4,2), (4,3), (2,4), (3,4)}
    _heuristics = {}
    
    def __init__(self, id:int, depth=-1, prune:bool=True):
        super().__init__(id)
        self.depth = depth
        self.prune = prune
    
    def getMove(self, state: gamestate,display:bool=False) -> packed_action:
        if display: print('Thinking...')
        start = time.time()
        value, bestAction = self.AlphaBetaSearch(state)
        end = time.time()
        if display: print(f'Time: {end-start:.1f}s | Pruned: {100*self.num_prune/self.max_prune:.1f}% ({self.num_prune}/{self.max_prune})')
        return bestAction
    
    def action_heuristic(self,move:packed_action)->int:
        core_weight = 20
        corner_weight = 40
        killer_token_weight = 10
        
        l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, curr_token_pos_x, curr_token_pos_y, new_token_pos_x,new_token_pos_y = move.get_rep()
        new_l_pos = (new_l_pos_x,new_l_pos_y,new_l_pos_d.decode('utf-8'))
        curr_t_pos = (curr_token_pos_x,curr_token_pos_y)
        new_t_pos = (new_token_pos_x,new_token_pos_y)
        
        l_set = L_piece._compute_L_coords(*new_l_pos)

        control_core = core_weight * len(l_set & Agent._CORE)           #reward controlling core
        avoid_corner = -1*corner_weight * int(bool(l_set & Agent._CORNERS))   #penalize touching corner
        killer_token = killer_token_weight * int(new_t_pos in Agent._KILLER_TOKENS if curr_t_pos!=(0,0) else 0) #reward placing tokens in killer positions
        
        return control_core + avoid_corner + killer_token
    
    def heuristic(self, state:gamestate) -> int:
        if state not in Agent._heuristics:
            player = not state.player   #not state.player is person who called heuristic
            opponent = state.player     # reward and penalize from caller's perspective

            opponent_options_weight = -1
            core_weight = 20
            corner_weight = 40
            win_weight = 1000

            #penalize number of moves other person has
            legalmovesofother = opponent_options_weight*len(state.getLegalMoves()) #state is already the other player, just call getLegalMoves
            
            player_l_set = state.L_pieces[player].get_coords()
            opponent_l_set = state.L_pieces[opponent].get_coords()
            
            control_core = core_weight * len(player_l_set & Agent._CORE)           #reward controlling core
            expel_core = -1*core_weight * len(opponent_l_set & Agent._CORE)        #penalize oponent in core
            avoid_corner = -1*corner_weight * len(player_l_set & Agent._CORNERS)   #penalize touching corner
            force_corner = corner_weight * len(opponent_l_set & Agent._CORNERS)    #reward oponent being in corner

            #reward true if they lose
            winning = win_weight * state.isGoal() #colinear with legalmovesofother

            score = legalmovesofother + control_core + expel_core + avoid_corner + force_corner + winning
            Agent._heuristics[state]=score

        return Agent._heuristics[state]

    def AlphaBetaSearch(self, state: gamestate) -> Tuple[int,packed_action]:
        self.max_prune = 0
        self.num_prune = 0
        self.visited = set() #store states already seen for this turn
        return self.MaxValueAB(state, self.depth)

    def MaxValueAB(self, state: gamestate, depth:int, alpha:float = float('-inf'), beta:float=float('inf')) -> Tuple[int, packed_action]:
        if depth == 0 or state.isGoal():
            # print(depth,len(self.visited))
            return self.heuristic(state), None

        moves = state.getLegalMoves()
        numMoves = len(moves)
        self.max_prune+= numMoves
        
        if state in self.visited:
            self.num_prune+=numMoves
            # print(depth,len(self.visited))
            return self.heuristic(state),None
        
        heuristics = np.array([self.action_heuristic(move) for move in moves])
        sort_indexes = np.argsort(heuristics)[::-1]
        moves = moves[sort_indexes]
        
        next_states = [state.getSuccessor(m) for m in moves]
        self.visited |= set(next_states)
        
        v = float('-inf')
        for i,m in enumerate(moves):
            v2, _ = self.MinValueAB(next_states[i], depth-1, alpha, beta)
            if v2 > v:
                v, move = v2, m
                alpha = max(alpha, v)
            if self.prune and v >= beta:
                # print(f'Pruned {numMoves-i}/{numMoves} actions')
                self.num_prune+= numMoves-i
                break
        # print(depth,len(self.visited))
        return v, move
    

    def MinValueAB(self, state: gamestate, depth:int, alpha:float, beta:float) -> Tuple[int, packed_action]:
        if depth == 0 or state.isGoal():
            # print(depth,len(self.visited))
            return self.heuristic(state), None
      
        moves = state.getLegalMoves()
        numMoves = len(moves)
        self.max_prune+= numMoves
        
        if state in self.visited:
            self.num_prune+=numMoves
            # print(depth,len(self.visited))
            return self.heuristic(state),None
            
        heuristics = np.array([self.action_heuristic(move) for move in moves])
        sort_indexes = np.argsort(heuristics)[::-1]
        moves = moves[sort_indexes]
        
        next_states = [state.getSuccessor(m) for m in moves]
        self.visited |= set(next_states)
        
        v = float('inf')
        for i,m in enumerate(moves):
            v2, _ = self.MaxValueAB(next_states[i], depth-1, alpha, beta)
            if v2 < v:
                v, move = v2, m
                beta = min(beta, v)
            if self.prune and v <= alpha:
                # print(f'Pruned {numMoves-i}/{numMoves} actions')
                self.num_prune+=numMoves-i
                break
        # print(depth,len(self.visited))
        return v, move
