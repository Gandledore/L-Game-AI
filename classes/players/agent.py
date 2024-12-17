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
    _CORE = {(2,2), (2,3), (3,2), (3,3)}                                        #the coordinates of the core
    _CORNERS = {(1,1), (1,4), (4,1), (4,4)}                                     #the coordinates of the corner
    _KILLER_TOKENS = {(2,1), (3,1), (1,2), (1,3), (4,2), (4,3), (2,4), (3,4)}   #the coordinates of the attacking token positions
    
    #states where an optimal oponent can force us to loss, according to wikipedia (and confirmed via previous testing)
    _death_states = {  gamestate(0,L_pieces=[L_piece(1,1,'S'),L_piece(2,2,'E')],token_pieces={token_piece(1,3),token_piece(4,1)}),
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
    
    
    def __init__(self, id:int, depth=-1, prune:bool=False,):
        super().__init__(id)
        
        self.prune = bool(prune)
        
        #default depth to search a state, -1 does infinite depth and solves whole game
        self.depth = depth
        
        # TRANSPOSITION TABLE (state: (depth,alpha,beta,optimal_moves_list))
        # depth=d means the state was searched up to depth d (equivalent to directly calling search from the state with depth d)
        # alpha,beta are pruning bounds.  alpha==beta implies all children were evaluated, or its a terminal node, or state is a death state
        # optimal moves stores all moves of equivalent value (best value found for the node so far)
        self.finished = {}
        
        #save heuristics for actions cause they're called a lot for sorting moves
        self.action_heuristics = {}
        
        # depth necessary to be confident a repeated state is a tie
        # 2 because we have stored all possible death states
        self.check_tie_depth = 2
        
        #keep track of states seen in current game, so that we can switch moves to hopefully confuse opponent
        self.played_states = {}
        
        #location for saved optimal moves, or location to save it
        self.optimal_moves_path = 'optimal_moves_id'+str(self.id)+'.pkl'
        self.display=False
        
        #only pre-process optimal moves for states when running infinite depth
        if self.depth<0:self.preprocess_optimal_moves()
    
    #load or precompute and save optimal moves
    def preprocess_optimal_moves(self):
        """
            loads or precomputes and save optimal moves
            looks for file stored in self.optimal_moves_path
            if it doesn't exist, runs through states solving optimal moves and saves in file specified by self.optimal_moves_path
        """
        #try to load saved file
        try:
            with open(self.optimal_moves_path,'rb') as f:
                print('Loading Solved Game...',end='')
                self.finished = pickle.load(f)
                print('\rLoaded Solved Game    ')
        
        #if file not found, process optimal moves and save
        except FileNotFoundError:
            print('Game not Solved. Solving game now...')
            #run through each state and optimize move for it
            for s in gamestate._legalMoves.keys():
                if s.player==self.id:#only have to optimize for states I will see
                    _,_ = self.AlphaBetaSearch(s)
            
            #save optimal moves in pickle file
            with open(self.optimal_moves_path,'wb') as f:
                print('Saving Optimal Moves...',end='')
                pickle.dump(self.finished,f)
                print('\rSaved Optimal Moves    ')
           
    #takes a state and wether do display information, and returns an action
    #called by play when this players turn 
    def getMove(self, state: gamestate,display:bool=False) -> packed_action:
        self.display=display
        if self.display: print('Thinking...')
        
        #call alpha beta search and measure time to compute next move
        start = time.time()
        value, bestActions = self.AlphaBetaSearch(state)
        end = time.time()

        #keep track of number of times seen this state in a game
        attempt = self.played_states.get(state)
        if attempt is None:
            attempt=0
            self.played_states[state]=0
        self.played_states[state]+=1
        
        #choose the kth move of bestActions after seeing it k times.
        #this switches up move to throw off opponent
        bestAction = bestActions[attempt%len(bestActions)]

        if self.display:
            if self.depth>0: print(f'Finished MinMaxing {len(self.finished)} states')
            bestAction.denormalize(state.transform) #to print as human expects
            print(f'Choosing Move:{bestAction} for value: {value}')
            bestAction.normalize(state.transform)   #to return as game expects
            print(f'Time: {1000*(end-start):.3f}ms | Pruned: {100*self.num_prune/self.max_prune:.2f}% ({self.num_prune}/{self.max_prune})')
        return bestAction
    
    #heuristic to estimate how good an action is (current version not very good)
    def action_heuristic(self,move:packed_action)->int:
        #if already known, return it
        h = self.action_heuristics.get(move)
        if h is not None:
            return h
        
        #otherwise compute it
        core_weight = 25                #weight for being in the core
        corner_weight = 40              #weight for being in the corner
        killer_token_weight = 10        #weight for placing a token in a killer position
        
        l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, curr_token_pos_x, curr_token_pos_y, new_token_pos_x,new_token_pos_y = move.get_rep()
        new_l_pos = (new_l_pos_x,new_l_pos_y,new_l_pos_d.decode('utf-8'))
        curr_t_pos = (curr_token_pos_x,curr_token_pos_y)
        new_t_pos = (new_token_pos_x,new_token_pos_y)
        
        l_set = L_piece._compute_L_coords(*new_l_pos)

        control_core = core_weight * len(l_set & Agent._CORE)                   #reward controlling core
        avoid_corner = -1*corner_weight * int(bool(l_set & Agent._CORNERS))     #penalize touching corner
        killer_token = killer_token_weight * int(new_t_pos in Agent._KILLER_TOKENS if curr_t_pos!=(0,0) else 0) #reward placing tokens in killer positions
        
        score = control_core + avoid_corner + killer_token
        self.action_heuristics[move]=score      #save score for later
        return score
    
    #estimate how good a state is (current version not very good)
    def heuristic(self, state:gamestate) -> float:
        player = self.id
        opponent = int(not self.id)
        flip_factor = 2*int(player == state.player) - 1 #1 if my turn, -1 if opponent's turn

        options_weight = 1          #weight for how many moves this state has
        core_weight = 25            #weight for being in the core
        corner_weight = 40          #weight for being in the corner
        win_weight = float('inf')   #weight for winning or losing

        #penalize number of moves other person has
        control_options = flip_factor * options_weight * len(state.getLegalMoves()) #reward me having moves, penalize moves for opponent
        
        player_l_set = state.L_pieces[player].get_coords()
        opponent_l_set = state.L_pieces[opponent].get_coords()
        
        # reward for controlling core
        control_core = core_weight * len(player_l_set & Agent._CORE)
        # penalize opponent in core
        expel_core = -1*core_weight * len(opponent_l_set & Agent._CORE)
        # penalize touching corner
        avoid_corner = -1*corner_weight * len(player_l_set & Agent._CORNERS)
        # reward opponent being in corner (we want to trap them in a corner / basically all win states involve opponent in corner)
        force_corner = corner_weight * len(opponent_l_set & Agent._CORNERS)

        # negative flip because if state is goal, current player lost.
        # flip_factor is +1 when its agent's turn, but want to penalize losing
        endgame = state in Agent._death_states
        winning = -1*flip_factor*win_weight if state.isGoal() or endgame else 0 #colinear with legalmovesofother

        score = control_options + control_core + expel_core + avoid_corner + force_corner + winning
        return score
    
    # wrapper for max value with some setup
    def AlphaBetaSearch(self, state: gamestate) -> Tuple[int,packed_action]:
        #for pruning quanitfication
        self.max_prune = 1
        self.num_prune = 0
        
        #keeps track of dfs path to detect tie
        self.seen = {state:1}
        return self.MaxValueAB(state, self.depth)

    # max and min are basically the same
    def MaxValueAB(self, state: gamestate, depth:int, alpha:float = float('-inf'), beta:float=float('inf')) -> Tuple[int, packed_action]:
        
        # if we have already finished evaluating this state with at least this much depth, return saved value
        cached_data = self.finished.get(state)
        if cached_data is not None:
            # finished state stores
            # - initiating a search from that depth on that state, as in knows the depth # of next moves
            # - alpha and beta as bounds for pruning
            # - optimal moves for state being accessed (any moves with equivalent value to best so far)

            stored_depth,saved_alpha,saved_beta,optimal_moves = cached_data

            # if using finite depth and stored depth is deeper than what's necessary, use it
            saved_deeper_search = depth>=0 and stored_depth>=depth

            # negative depth saved => state fully searched
            # the only way to have negative depth is if you start with negative depth (so this is only true when solving whole game)
            state_fully_searched = stored_depth<0

            # if the depth searched is greater than tie state, we can assume it is a tie
            tied_state = stored_depth>=self.check_tie_depth

            #if the state being accessed was pruned, then check if it can be pruned again without any searching
            prunable = saved_alpha>beta
            exact = saved_beta==saved_alpha #state fully searched for saved depth, or endgame state (terminal or death)
            if (saved_deeper_search or state_fully_searched or tied_state):
                if exact or prunable:
                    return saved_alpha,optimal_moves
        
        moves = state.getLegalMoves()
        numMoves = len(moves)
        self.max_prune+= numMoves       #keep track for pruning data
        
        # calculate heuristic score for each move
        # sort by score (descending) and then apply that order to moves
        # if action heuristic is good, should prune a lot
        heuristics = np.array([self.action_heuristic(move) for move in moves])
        sort_indexes = np.argsort(heuristics,stable=True)[::-1]     #sort reverse cause standard sorts in increasing order, but higher heuristic is better
        moves = moves[sort_indexes]
        
        if state in Agent._death_states:
            h = self.heuristic(state)
            self.finished[state] = (-1,h,h,moves)
            return h,moves
        
        if depth == 0 or state.isGoal():
            h = self.heuristic(state)
            self.finished[state] = (depth,h,h,None)
            return h, None
        
        # v is the value of the best move
        v = float('-inf')
        optimal_moves = []
        for i,m in enumerate(moves):
            next_state = state.getSuccessor(m)
            # if we've seen this state before, then start a check from check_tie_depth instead of continuing infinite search
            num_seen = self.seen.get(next_state)
            
            if num_seen is None:
                self.seen[next_state]=0
                d=depth-1
            elif num_seen>0:
                d = self.check_tie_depth if depth<0 else min(depth-1,self.check_tie_depth)
            else:
                d = depth-1
                
            # v2 is the value of the best move for the opponent (could be a pruned value, in which case its ignored)
            self.seen[next_state]+=1
            v2,_ = self.MinValueAB(next_state, d, v, beta)      #pass v to ensure not pruning on parent's data (because saving to transposition table)
            self.seen[next_state]-=1
            
            #if new best, update optimal moves and v
            if v2 > v:
                v, optimal_moves = v2, [m]
                alpha = max(alpha, v)
            elif v2==v:
                optimal_moves.append(m)         #save other moves with value equal to current equivalent
            if self.prune and v > beta:         #don't prune on equality because saving equal values. parent node would add it to its optimal moves list
                self.num_prune+= numMoves-i-1
                self.finished[state] = (depth,v, float('inf'),optimal_moves)        #max can do at least as well as alpha, could be any amount higher
                return v,optimal_moves
        
        self.finished[state] = (depth,v,v,optimal_moves)
        return v, optimal_moves
    
    def MinValueAB(self, state: gamestate, depth:int, alpha:float = float('-inf'), beta:float=float('inf')) -> Tuple[int, packed_action]:
        #if we have already finished evaluating this state with at least this much depth, return saved value
        cached_data = self.finished.get(state)
        
        if cached_data is not None:
            stored_depth,saved_alpha,saved_beta,optimal_moves = cached_data
            saved_deeper_search = depth>=0 and stored_depth>=depth
            state_fully_searched = stored_depth<0
            tied_state = stored_depth>=self.check_tie_depth
            prunable = saved_beta<alpha
            exact = saved_beta==saved_alpha
            if (saved_deeper_search or state_fully_searched or tied_state):
                if exact or prunable:
                    return saved_beta,optimal_moves
            
        #not prune on equality when saving equal states
        moves = state.getLegalMoves()
        numMoves = len(moves)
        self.max_prune+= numMoves
        
        heuristics = np.array([self.action_heuristic(move) for move in moves])
        sort_indexes = np.argsort(heuristics,stable=True)[::-1]
        moves = moves[sort_indexes]
        
        if state in Agent._death_states:
            h = self.heuristic(state)
            self.finished[state] = (-1,h,h,moves)
            return h,moves
      
        if depth == 0 or state.isGoal():
            h = self.heuristic(state)
            self.finished[state] = (depth,h,h,None)
            return h, None
        
        v = float('inf')
        optimal_moves = []
        for i,m in enumerate(moves):
            next_state = state.getSuccessor(m)
            
            num_seen = self.seen.get(next_state)
            
            if num_seen is None:
                self.seen[next_state]=0
                d=depth-1
            elif num_seen>0:
                d = self.check_tie_depth if depth<0 else min(depth-1,self.check_tie_depth)
            else:
                d = depth-1
            
            self.seen[next_state]+=1
            v2,_ = self.MaxValueAB(next_state, d, alpha, v)
            self.seen[next_state]-=1
            
            if v2 < v:
                v, optimal_moves = v2, [m]
                beta = min(beta, v)
            elif v2==v:
                optimal_moves.append(m)
            if self.prune and v < alpha:
                self.num_prune+=numMoves-i-1
                self.finished[state] = (depth,float('-inf'),v,optimal_moves)
                return v,optimal_moves

        self.finished[state] = (depth,v,v,optimal_moves)
        return v, optimal_moves

    def game_reset(self):
        # pass
        self.played_states = {}#reset this so that it starts from best of bestActions