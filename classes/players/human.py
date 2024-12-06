from classes.players.player import Player
from classes.base_structs.action import packed_action
from classes.base_structs.gamestate import gamestate

class Human(Player):
    def __init__(self,id:int):
        super().__init__(id)
    
    #interface for a play code to get human input
    def getMove(self, state: gamestate, display:bool=True) -> packed_action:
        if display: print('Valid Moves:',len(state.getLegalMoves()))
        # print('\nRecieved State:',state)
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
            try:
                current_token_pos = (int(move_parts[3]), int(move_parts[4]))
                new_token_pos = (int(move_parts[5]), int(move_parts[6]))
            except ValueError as e:
                raise ValueError('Use integers for token locations')
            
        elif len(move_parts)==3:
            current_token_pos=(0,0)
            new_token_pos = (0,0)
        
        move = packed_action(l_piece_id=state.player,new_l_pos=new_l_pos,current_token_pos=current_token_pos,new_token_pos=new_token_pos)
        move.normalize(state.transform)
        return move
    def game_reset(self):
        pass