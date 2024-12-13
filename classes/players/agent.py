from classes.players.player import Player
from classes.base_structs.action import packed_action
from classes.base_structs.gamestate import gamestate
from classes.base_structs.L_piece import L_piece
from classes.base_structs.token_piece import token_piece

from typing import Tuple
import time
import numpy as np
import pickle
from tqdm import tqdm

import sys
sys.setrecursionlimit(5000)#maybe this can be improved

class Agent(Player):

    # Constants for heuristic

    _CORE = {(2,2), (2,3), (3,2), (3,3)}
    _CORNERS = {(1,1), (1,4), (4,1), (4,4)}
    _KILLER_TOKENS = {(2,1), (3,1), (1,2), (1,3), (4,2), (4,3), (2,4), (3,4)}
    _optimal_moves_path = 'optimal_moves'
    _force_loss_states = {  gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(1,3),token_piece(4,1)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(1,4),token_piece(4,2)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(1,4),token_piece(4,1)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(4,3),token_piece(4,1)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(3,4),token_piece(4,3)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(4,3),token_piece(4,2)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(3,4),token_piece(4,2)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(3,4),token_piece(4,1)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(4,2),token_piece(4,1)}),
                            gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(3,3,'N')],token_pieces={token_piece(4,2),token_piece(4,1)}),
                            gamestate(0,L_pieces=[L_piece(2,1,'S'),L_piece(1,3,'N')],token_pieces={token_piece(3,2),token_piece(3,4)}),
                            gamestate(0,L_pieces=[L_piece(2,1,'S'),L_piece(3,3,'N')],token_pieces={token_piece(1,2),token_piece(4,2)}),
                            gamestate(0,L_pieces=[L_piece(2,1,'S'),L_piece(1,3,'N')],token_pieces={token_piece(3,2),token_piece(4,4)}),
                            gamestate(0,L_pieces=[L_piece(1,2,'N'),L_piece(1,3,'S')],token_pieces={token_piece(3,1),token_piece(4,2)}),
                            
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(1,3),token_piece(4,1)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(1,4),token_piece(4,2)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(1,4),token_piece(4,1)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(4,3),token_piece(4,1)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(3,4),token_piece(4,3)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(4,3),token_piece(4,2)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(3,4),token_piece(4,2)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(3,4),token_piece(4,1)}),
                            gamestate(1,L_pieces=[L_piece(2,2,'E'),L_piece(1,1,'S')],token_pieces={token_piece(4,2),token_piece(4,1)}),
                            gamestate(1,L_pieces=[L_piece(3,3,'N'),L_piece(1,1,'S')],token_pieces={token_piece(4,2),token_piece(4,1)}),
                            gamestate(1,L_pieces=[L_piece(1,3,'N'),L_piece(2,1,'S')],token_pieces={token_piece(3,2),token_piece(3,4)}),
                            gamestate(1,L_pieces=[L_piece(3,3,'N'),L_piece(2,1,'S')],token_pieces={token_piece(1,2),token_piece(4,2)}),
                            gamestate(1,L_pieces=[L_piece(1,3,'N'),L_piece(2,1,'S')],token_pieces={token_piece(3,2),token_piece(4,4)}),
                            gamestate(1,L_pieces=[L_piece(1,3,'S'),L_piece(1,2,'N')],token_pieces={token_piece(3,1),token_piece(4,2)})}
    
    
    def __init__(self, id:int, depth=-1, prune:bool=False):
        super().__init__(id)
        
        self.display=False
        self.depth = depth
        # if depth<0: self.prune = False
        # else: self.prune = bool(prune)
        self.prune = bool(prune)
        # TRANSPOSITION TABLE
        # check bugs here (saving depth it solved to)
        # <1 = assuming fully solved, may not be correct assumption
        # stores all moves of equivalent value
        self.finished = {} #stores state:(d,v) tuple of depth and best backpropagated value of highest depth search (-1 = infinite depth)
        self.action_heuristics = {}
        self.check_tie_depth = 2#min(depth,11)%12 #look >5 ply ahead, cause according to wikipedia, you can avoid losing if you look 5 steps ahead
        # how to check ties: if encounter a looped state or a state we've already seen, say hey we've already seen this state, potentially a tie, then depth limited search starting from depth 11 because wikipedia says a player can win in 4 turns (check assumption)
        # in the next 11 turns, can a win or loss be forced? backtrack
        self.last = 0
        # not actually the max score, a lazy approximation of it (did not want to compute max score)
        # if the |score| is >900 consider a forced terminal state
        # forced = one player can win no matter what the opponent plays -> can force a terminal state
        self.max_score = float('inf')
        self.played_states = {}
        
        if self.depth<0:self.preprocess_optimal_moves(gamestate(player=self.id))
    
    def preprocess_optimal_moves(self,state):
        solved_path = Agent._optimal_moves_path+'_id'+str(self.id)+'.pkl'
        try:
            with open(solved_path,'rb') as f:
                print('Loading Solved Game...',end='')
                self.finished = pickle.load(f)
                print('\rLoaded Solved Game    ')
        except FileNotFoundError:
            print('Game not Solved. Solving game now...')
            # _,_ = self.AlphaBetaSearch(state)
            for s in gamestate._legalMoves.keys():
                if s.player==self.id:
                    _,_ = self.AlphaBetaSearch(s)
                # if s.player!=self.id:
                #     self.max_prune = 1
                #     self.num_prune = 0
                #     self.seen = {s:True}
                #     _,_ = self.MinValueAB(s,self.depth)
            
            with open(solved_path,'wb') as f:
                print('Saving Optimal Moves...',end='')
                pickle.dump(self.finished,f)
                print('\rSaved Optimal Moves    ')
            
    def getMove(self, state: gamestate,display:bool=False) -> packed_action:
        self.display=display
        if self.display: 
            print('Thinking...')
            # print(len(state.getLegalMoves()))
        start = time.time()
        value, bestAction = self.AlphaBetaSearch(state)
        end = time.time()

        if self.display:
            print(f'Finished MinMaxing {len(self.finished)} states')
            bestAction.denormalize(state.transform)
            # print(f'Choosing Move:{bestAction} for value: {value} from depth {self.finished[state][0]} out of {len(bestActions)} options')
            print(f'Choosing Move:{bestAction} for value: {value}')
            bestAction.normalize(state.transform)
            print(f'Time: {end-start:.1f}s | Pruned: {100*self.num_prune/self.max_prune:.1f}% ({self.num_prune}/{self.max_prune})')
        return bestAction
    
    def action_heuristic(self,move:packed_action)->int:
        try: 
            return self.action_heuristics[move]
        except KeyError:
            core_weight = 25
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
            
            score = control_core + avoid_corner + killer_token
            self.action_heuristics[move]=score
            return score
    
    def heuristic(self, state:gamestate) -> float:
        player = self.id
        opponent = int(not self.id)
        flip_factor = 2*int(player == state.player) - 1 #1 if my turn, -1 if opponent's turn

        options_weight = 1
        core_weight = 25
        corner_weight = 40
        win_weight = float('inf')

        #penalize number of moves other person has
        control_options = flip_factor * options_weight * len(state.getLegalMoves()) #state is already the other player, just call getLegalMoves
        
        player_l_set = state.L_pieces[player].get_coords()
        opponent_l_set = state.L_pieces[opponent].get_coords()
        
        control_core = core_weight * len(player_l_set & Agent._CORE)           #reward controlling core
        expel_core = -1*core_weight * len(opponent_l_set & Agent._CORE)        #penalize oponent in core
        avoid_corner = -1*corner_weight * len(player_l_set & Agent._CORNERS)   #penalize touching corner
        force_corner = corner_weight * len(opponent_l_set & Agent._CORNERS)    #reward oponent being in corner

        #negative flip because if state is goal, current player lost. 
        # flip is +1 when its agent's turn, but want to penalize losing
        endgame = state in Agent._force_loss_states
        winning = -1*flip_factor*win_weight if state.isGoal() or endgame else 0 #colinear with legalmovesofother

        score = control_options + control_core + expel_core + avoid_corner + force_corner + winning
        return score
    
    # wrapper for max value with some setup
    def AlphaBetaSearch(self, state: gamestate) -> Tuple[int,packed_action]:
        self.max_prune = 1
        self.num_prune = 0
        self.seen = {state:True}
        return self.MaxValueAB(state, self.depth)

    # max and min are basically the same, difference = sign flips
    def MaxValueAB(self, state: gamestate, depth:int, alpha:float = float('-inf'), beta:float=float('inf')) -> Tuple[int, packed_action]:
        if self.display and self.last < len(self.finished) and len(self.finished)%100==0:
            self.last = len(self.finished)
            print(f'Cached: {self.last} states')

        #if we have already finished evaluating this state with at least this much depth, return saved value
        # try except = reduces hash lookups
        try:
            # finished state stores
            # - initiating a search from that depth on that state, as in knows the depth # of next moves
            # - value it backpropagated
            # - optimal move for state being accessed (var "state")

            stored_depth,saved_alpha,saved_beta,optimal_move = self.finished[state]

            # if using finite depth and stored depth is deeper than what's necessary, use it
            saved_deeper_search = depth>=0 and stored_depth>=depth

            # we want for negative depth saved = this has been fully searched
            # CHECK THIS (check maintaining)
            # the only way to have negative depth is if you start with negative depth (so this is only a check for negative depth)
            state_fully_searched = stored_depth<0

            # if we've seen this state before, and we've seen it at a depth greater than the check_tie_depth, then we can assume it's a tie
            tied_state = stored_depth>=self.check_tie_depth

            prunable = saved_alpha>=beta
            exact = saved_beta==saved_alpha
            if (saved_deeper_search or state_fully_searched or tied_state):
                if exact or prunable:
                    return saved_alpha,optimal_move
        except KeyError:
            pass
        
        if depth == 0 or state.isGoal():
            h =self.heuristic(state)
            self.finished[state] = (depth,h,h,None)
            return h, None
        
        moves = state.getLegalMoves()
        numMoves = len(moves)
        self.max_prune+= numMoves
        
        # calculate heuristic score for each move
        # sort by score (descending) and then apply that order to moves
        heuristics = np.array([self.action_heuristic(move) for move in moves])
        sort_indexes = np.argsort(heuristics)[::-1]
        moves = moves[sort_indexes]
        
        if state in Agent._force_loss_states:
            h = self.heuristic(state)
            self.finished[state] = (-1,h,h,None)
            return h,None
        
        # v is the value of the best move
        v = float('-inf')
        optimal_move = None
        for i,m in enumerate(moves):
            next_state = state.getSuccessor(m)
            # if we've seen this state before, then we've seen it at a depth of at least check_tie_depth or negative depth
            if next_state in self.seen and self.seen[next_state]:
                d = self.check_tie_depth if depth<0 else min(depth-1,self.check_tie_depth)
            else:
                d = depth-1
            
            # v2 is the value of the best move for the opponent
            self.seen[next_state]=True
            v2,_ = self.MinValueAB(next_state, d, alpha, beta)
            self.seen[next_state]=False
            
            if v2 > v:
                v, optimal_move = v2, m
                alpha = max(alpha, v)
            if self.prune and v >= beta:
                self.num_prune+= numMoves-i-1
                self.finished[state] = (depth,v, float('inf'),optimal_move)
                return v,optimal_move
        
        self.finished[state] = (depth,v,v,optimal_move)
        return v, optimal_move
    
    def MinValueAB(self, state: gamestate, depth:int, alpha:float = float('-inf'), beta:float=float('inf')) -> Tuple[int, packed_action]:
        
        if self.display and self.last < len(self.finished) and len(self.finished)%100==0:
            self.last = len(self.finished)
            print(f'Cached: {self.last} states')
        
        #if we have already finished evaluating this state with at least this much depth, return saved value
        try:
            stored_depth,saved_alpha,saved_beta,optimal_move = self.finished[state]
            saved_deeper_search = depth>=0 and stored_depth>=depth
            state_fully_searched = stored_depth<0
            tied_state = stored_depth>=self.check_tie_depth
            prunable = saved_beta<=alpha
            exact = saved_beta==saved_alpha
            if (saved_deeper_search or state_fully_searched or tied_state):
                if exact or prunable:
                    # if state == self.test_state:
                    #     print(self.finished[state])
                    return saved_beta,optimal_move
        except KeyError:
            pass
        
        if depth == 0 or state.isGoal():
            h = self.heuristic(state)
            self.finished[state] = (depth,h,h,None)
            return h, None
      
        moves = state.getLegalMoves()
        numMoves = len(moves)
        self.max_prune+= numMoves
        
        heuristics = np.array([self.action_heuristic(move) for move in moves])
        sort_indexes = np.argsort(heuristics,stable=True)[::-1]
        moves = moves[sort_indexes]
        
        if state in Agent._force_loss_states:
            h = self.heuristic(state)
            self.finished[state] = (-1,h,h,None)
            return h,None
        
        v = float('inf')
        optimal_move = None
        for i,m in enumerate(moves):
            next_state = state.getSuccessor(m)
            
            if next_state in self.seen and self.seen[next_state]:
                d = self.check_tie_depth if depth<0 else min(depth-1,self.check_tie_depth)
            else:
                d = depth-1
                
            self.seen[next_state] = True
            v2,_ = self.MaxValueAB(next_state, d, alpha, beta)
            self.seen[next_state] = False
            
            if v2 < v:
                v, optimal_move = v2, m
                beta = min(beta, v)
            if self.prune and v <= alpha:
                self.num_prune+=numMoves-i-1
                self.finished[state] = (depth,float('-inf'),v,optimal_move)
                return v,optimal_move

        self.finished[state] = (depth,v,v,optimal_move)
        return v, optimal_move

    def game_reset(self):
        # pass
        self.played_states = {}