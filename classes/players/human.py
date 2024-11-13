from classes.players.player import Player
from classes.base_structs.action import action
from classes.game import Game

class Human(Player):

    #interface for a play code to get human input
    #needs cleanup

    def getMove(self, game: Game) -> action:

        wholeMoves = input(f"Player {game.player+1}: Enter xl1 yl1 dl1 tx ty tx ty: ")
        try:
            move_parts = wholeMoves.split()
     
            if ( (len(move_parts) != 7) and (len(move_parts) != 3) ):
                raise ValueError("Enter commands in specified format")
            
            POSSIBLE_SETS = {'0':{1,2,3,4},'1':{1,2,3,4},'2':{'N','E','S','W'}}
            
            for i in range(2):
                if int(move_parts[i]) not in POSSIBLE_SETS[str(i)]:
                    raise ValueError(f"L piece coordinate out of bounds. {move_parts[i]} is not in {POSSIBLE_SETS[str(i)]}")
            if move_parts[2] not in POSSIBLE_SETS['2']:
                raise ValueError(f"L piece direction invalid. {move_parts[2]} is not in {POSSIBLE_SETS['2']}")


            new_l_pos = (int(move_parts[0]), int(move_parts[1]),move_parts[2])

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

        except ValueError as e:
            print(f"Invalid input: {e}.")
            return self.getMove()    

