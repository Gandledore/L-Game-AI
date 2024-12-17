from classes.players.player import Player
from classes.base_structs.action import packed_action
from classes.base_structs.gamestate import gamestate

import numpy as np

class Human(Player):
    _CORE = {(2,2), (2,3), (3,2), (3,3)}
    _CORNERS = {(1,1), (1,4), (4,1), (4,4)}
    _KILLER_TOKENS = {(2,1), (3,1), (1,2), (1,3), (4,2), (4,3), (2,4), (3,4)}
    _heuristics = {}

    def __init__(self,id:int):
        super().__init__(id)
    
    def heuristic(self, state:gamestate) -> int:
        player = self.id
        opponent = int(not self.id)
        flip_factor = 2*int(player == state.player) - 1 #1 if my turn, -1 if opponent's turn

        options_weight = 1
        core_weight = 25
        corner_weight = 40
        win_weight = 1000

        #penalize number of moves other person has
        control_options = flip_factor * options_weight * len(state.getLegalMoves()) #state is already the other player, just call getLegalMoves
        
        player_l_set = state.L_pieces[player].get_coords()
        opponent_l_set = state.L_pieces[opponent].get_coords()
        
        control_core = core_weight * len(player_l_set & Human._CORE)           #reward controlling core
        expel_core = -1*core_weight * len(opponent_l_set & Human._CORE)        #penalize oponent in core
        avoid_corner = -1*corner_weight * len(player_l_set & Human._CORNERS)   #penalize touching corner
        force_corner = corner_weight * len(opponent_l_set & Human._CORNERS)    #reward oponent being in corner

        #negative flip because if state is goal, current player lost. 
        # flip is +1 when its agent's turn, but want to penalize losing
        winning = -1*flip_factor*win_weight * state.isGoal() #colinear with legalmovesofother

        score = control_options + control_core + expel_core + avoid_corner + force_corner + winning
        return score
    

    #interface for a play code to get human input
    def getMove(self, state: gamestate, move_parts) -> packed_action:
        if len(move_parts)==7 or len(move_parts)==3:
            try:    #raises value error if can't cast to int
                new_l_pos = (int(move_parts[0]), int(move_parts[1]),move_parts[2])
            except ValueError as e:
                raise ValueError('Use integers for x and y.')
            
            if len(move_parts)==7:
                try:
                    current_token_pos = (int(move_parts[3]), int(move_parts[4]))
                    new_token_pos = (int(move_parts[5]), int(move_parts[6]))
                except ValueError as e:
                    raise ValueError('Use integers for token locations.')
            elif len(move_parts)==3:
                current_token_pos=(0,0)
                new_token_pos = (0,0)
        
            move = packed_action(l_piece_id=state.player,new_l_pos=new_l_pos,current_token_pos=current_token_pos,new_token_pos=new_token_pos)
            move.normalize(state.transform)
        else:
            raise ValueError(f"Enter commands in specified format.")
        return move

    def instructionHandler(self, state:gamestate, display:bool=False):
        if display: print('Valid Moves:',len(state.getLegalMoves()))
        
        moves = state.getLegalMoves()
        vals = np.array([self.heuristic(state.getSuccessor(move)) for move in state.getLegalMoves()])
        bestMove = moves[np.argmax(vals)]

        bestMove.denormalize(state.transform)
        print("Suggested Move: ", bestMove.suggest_format())
        bestMove.normalize(state.transform)
        
        instruction = input("Enter instruction: ")
        pieces = instruction.split()
        if len(pieces)==0:
            return ('move',bestMove)
        instruction = pieces[0]
        if instruction not in ('undo','redo','replay','save','swap','x','y','t','cw','ccw','help'):
            return ('move',self.getMove(state,pieces))
        elif instruction == "x":
            return ('view',[True,False,False])
        elif instruction == "y":
            return ('view',[False,True,False])
        elif instruction == "t":
            return ('view',[False,False,True])
        elif instruction == "cw":
            return ('view',[True,False,True])
        elif instruction == "ccw":
            return ('view',[False,True,True])
        elif instruction == 'replay':
            return ('view','replay')
        elif instruction in ('undo','redo','save','help'):
            return ('control',instruction)
        elif instruction=='swap':
            return ('swap','ai')
        else:
            raise ValueError(f"Invalid instruction {instruction}.")
        
    def game_reset(self):
        pass