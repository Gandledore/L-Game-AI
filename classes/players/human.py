from classes.players.player import Player
from classes.base_structs.action import action
from classes.base_structs.gamestate import gamestate

import Players
import copy

class Human(Player):
    def __init__(self,id:int):
        super().__init__(id)
    
    #interface for a play code to get human input
    def getMove(self, state: gamestate) -> action:

        print('Valid Moves:',len(state.getLegalMoves()))
        suggestedmove = Players.Agent(0, 2).getMove(copy.deepcopy(state)) # get move from a alphabeta heuristic depth 1 search
        print("Suggested Move: ", suggestedmove.format_move())
        wholeMoves = input(f"Player {state.player+1}: Enter xl1 yl1 dl1 tx ty tx ty: ")
        move_parts = wholeMoves.split()
    
        if ( (len(move_parts) != 7) and (len(move_parts) != 3) ):
            raise ValueError("Enter commands in specified format")
        
        #raises value error if can't cast to int
        try:
            new_l_pos = (int(move_parts[0]), int(move_parts[1]),move_parts[2])
        except ValueError as e:
            raise ValueError('Use integers for xl1 yl1')
        
        if len(move_parts)==7:
            current_token_pos = (int(move_parts[3]), int(move_parts[4]))
            new_token_pos = (int(move_parts[5]), int(move_parts[6]))
            token_id = next((i for i, token in enumerate(state.token_pieces) if current_token_pos == token.get_position()), -1)
        elif len(move_parts)==3:
            current_token_pos = None
            new_token_pos = None
            token_id=None
        
        move = action(l_piece_id=state.player,new_l_pos=new_l_pos,token_id=token_id,new_token_pos=new_token_pos)
        return move
    
