from classes.players.player import Player
from classes.base_structs.action import packed_action
from classes.base_structs.gamestate import gamestate

class Human(Player):
    def __init__(self,id:int):
        super().__init__(id)
    
    #interface for a play code to get human input
    def getMove(self, state: gamestate) -> packed_action:
        print('Valid Moves:',len(state.getLegalMoves()))
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
            
            token_id = next((i for i, token in enumerate(state.token_pieces) if current_token_pos == token.get_position()), -1)
            assert token_id!=-1, f'No Token at {new_token_pos}.'
        elif len(move_parts)==3:
            token_id=255
            new_token_pos = (0,0)
        
        move = packed_action(l_piece_id=state.player,new_l_pos=new_l_pos,token_id=token_id,new_token_pos=new_token_pos)
        return move