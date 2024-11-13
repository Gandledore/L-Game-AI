from classes.players.player import Player
from classes.base_structs.action import action
from classes.game import Game

class Human(Player):

    #interface for a play code to get human input
    #needs cleanup

    def getMove(self, game: Game) -> action:
        print('Valid Moves:',len(game.getLegalMoves(game.state)))
        wholeMoves = input(f"Player {game.player+1}: Enter xl1 yl1 dl1 tx ty tx ty: ")
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
            token_id = next((i for i, token in enumerate(game.state.token_pieces) if current_token_pos == token.get_position()), -1)
        elif len(move_parts)==3:
            current_token_pos = None
            new_token_pos = None
            token_id=None
        
        move = action(l_piece_id=game.player,new_l_pos=new_l_pos,token_id=token_id,new_token_pos=new_token_pos)
        return move