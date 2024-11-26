from classes.players.player import Player
from classes.base_structs.action import packed_action
from classes.base_structs.gamestate import gamestate
from classes.base_structs.L_piece import L_piece
from classes.base_structs.token_piece import token_piece

from typing import Tuple
import time
import numpy as np


class Agent(Player):
    _CORE = {(2,2), (2,3), (3,2), (3,3)}
    _CORNERS = {(1,1), (1,4), (4,1), (4,4)}
    _KILLER_TOKENS = {(2,1), (3,1), (1,2), (1,3), (4,2), (4,3), (2,4), (3,4)}
    
    def __init__(self, id:int, depth=-1, prune:bool=False):
        super().__init__(id)
        self.depth = depth
        self.prune = prune
        self.finished = {} #stores state:(d,v) tuple of depth and best backpropagated value of highest depth search (-1 = infinite depth)
        self.check_tie_depth = 5 #look 5 ahead, cause according to wikipedia, you can avoid losing if you look 5 steps ahead
        self.ties = set()
        self.last = 0
        self.max_score = 1
        self.heuristics = {}
        
    def getMove(self, state: gamestate,display:bool=False) -> packed_action:
        if display: print('Thinking...')
        start = time.time()
        value, bestAction = self.AlphaBetaSearch(state)
        end = time.time()
        if display: 
            print(f'Finished MinMaxing {len(self.finished)} states')
            print(f'Choosing Move:{bestAction} for value: {value}')
            print(f'Time: {end-start:.1f}s | Pruned: {100*self.num_prune/self.max_prune:.1f}% ({self.num_prune}/{self.max_prune})')
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
        if state not in self.heuristics:
            player = not state.player   #not state.player is person who called heuristic
            opponent = state.player     # reward and penalize from caller's perspective

            opponent_options_weight = 0#-1
            core_weight = 0#20
            corner_weight = 0#40
            win_weight = 1#1000

            #penalize number of moves other person has
            legalmovesofother = opponent_options_weight*len(state.getLegalMoves()) #state is already the other player, just call getLegalMoves
            
            player_l_set = state.L_pieces[player].get_coords()
            opponent_l_set = state.L_pieces[opponent].get_coords()
            
            control_core = core_weight * len(player_l_set & Agent._CORE)           #reward controlling core
            expel_core = -1*core_weight * len(opponent_l_set & Agent._CORE)        #penalize oponent in core
            avoid_corner = -1*corner_weight * len(player_l_set & Agent._CORNERS)   #penalize touching corner
            force_corner = corner_weight * len(opponent_l_set & Agent._CORNERS)    #reward oponent being in corner

            #reward true if they lose
            winning = win_weight * (2*int(self.id != state.player) - 1) * state.isGoal() #colinear with legalmovesofother

            score = legalmovesofother + control_core + expel_core + avoid_corner + force_corner + winning
            self.heuristics[state]=score

        return self.heuristics[state]
    
    def AlphaBetaSearch(self, state: gamestate) -> Tuple[int,packed_action]:
        self.max_prune = 1
        self.num_prune = 0
        self.parity = self.depth%2
        self.seen = {state:[self.depth]}
        return self.MaxValueAB(state, self.depth)

    def MaxValueAB(self, state: gamestate, depth:int, alpha:float = float('-inf'), beta:float=float('inf')) -> Tuple[int, packed_action]:
        # if self.last < len(self.finished) and len(self.finished)%100==0:
        #     self.last = len(self.finished)
        #     print(f'Cached: {self.last} states')

        #if we have already finished evaluating this state with at least this much depth, return saved value
        if state in self.finished:
            if ((depth>=0 and self.finished[state][0]>=depth or self.finished[state][0]==self.check_tie_depth) or self.finished[state][0]<0 or abs(self.finished[state][1])>=self.max_score):
                # self.num_prune+=numMoves-1
                # if depth==-1: print(f'MAX USING saved test state {self.finished[state]} for depth {depth}')
                return self.finished[state][1],self.finished[state][2]
            # else: print(f'NOT using saved {self.finished[state]} for current depth {depth}')
        
        if depth == 0 or state.isGoal():
            h =self.heuristic(state)
            # self.finished[state] = (depth,self.heuristic(state),None)
            # print(f'SAVING evaluation {state}\n(D,V):{self.finished[state]}')
            return h, None
        
        moves = state.getLegalMoves()
        numMoves = len(moves)
        self.max_prune+= numMoves
        
        heuristics = np.array([self.action_heuristic(move) for move in moves])
        sort_indexes = np.argsort(heuristics)[::-1]
        moves = moves[sort_indexes]
        
        v = float('-inf')
        move = None
        # testing_state=False
        for i,m in enumerate(moves):
            next_state = state.getSuccessor(m)
            if next_state in self.ties:
                v2 = 0
            elif next_state in self.seen and len(self.seen[next_state])>0:
                d = self.check_tie_depth-1 if depth<0 else min(depth-1,self.check_tie_depth-1)
                self.seen[next_state].append(d)
                v2,_ = self.MinValueAB(next_state,d,alpha,beta)
                if v2==0 and d==self.check_tie_depth-1:
                    self.ties.add(next_state)
                self.seen[next_state].pop()
            else:
                self.seen[next_state] = []
                self.seen[next_state].append(depth)
                v2, _ = self.MinValueAB(next_state, depth-1, alpha, beta)
                self.seen[next_state].pop()
            if v2 > v:
                v, move = v2, m
                alpha = max(alpha, v)
            if self.prune and v >= beta:
                self.num_prune+= numMoves-i-1
                break
        
        self.finished[state] = (depth,v,move)
        return v, move
    
    def MinValueAB(self, state: gamestate, depth:int, alpha:float = float('-inf'), beta:float=float('inf')) -> Tuple[int, packed_action]:
        # if self.last < len(self.finished) and len(self.finished)%100==0:
        #     self.last = len(self.finished)
        #     print(f'Cached: {self.last} states')
        
        #if we have already finished evaluating this state with at least this much depth, return saved value
        if state in self.finished:
            if ((depth>=0 and self.finished[state][0]>=depth or self.finished[state][0]==self.check_tie_depth-1) or self.finished[state][0]<0 or abs(self.finished[state][1])>=self.max_score):
                # print(f'USING Saved evaluation | {self.finished[state]}')
                return self.finished[state][1],self.finished[state][2]
            # else: print(f'NOT using saved {self.finished[state]} for current depth {depth}')

        if depth == 0 or state.isGoal():
            h = self.heuristic(state)
            # self.finished[state] = (depth,h,None)
            # print(f'SAVING evaluation {state}\n(D,V):{self.finished[state]}')
            return h, None
      
        moves = state.getLegalMoves()
        numMoves = len(moves)
        self.max_prune+= numMoves
        
        heuristics = np.array([self.action_heuristic(move) for move in moves])
        sort_indexes = np.argsort(heuristics)[::-1]
        moves = moves[sort_indexes]
        
        v = float('inf')
        move = None
        for i,m in enumerate(moves):
            next_state = state.getSuccessor(m)
            if next_state in self.ties:
                v2=0
            elif next_state in self.seen and len(self.seen[next_state])>0:
                d = self.check_tie_depth if depth<0 else min(depth-1,self.check_tie_depth)
                self.seen[next_state].append(d)
                v2,_ = self.MaxValueAB(next_state,d,alpha,beta)
                if v2==0 and d==self.check_tie_depth:
                    self.ties.add(next_state)
                self.seen[next_state].pop()
            else:
                self.seen[next_state] = []
                self.seen[next_state].append(depth)
                v2, _ = self.MaxValueAB(next_state, depth-1, alpha, beta)
                self.seen[next_state].pop()
            if v2 < v:
                v, move = v2, m
                beta = min(beta, v)
            if self.prune and v <= alpha:
                self.num_prune+=numMoves-i-1
                break
            
        self.finished[state] = (depth,v,move)
        return v, move
