from classes.players.player import Player
from classes.base_structs.action import packed_action
from classes.base_structs.gamestate import gamestate


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
    def getMove(self, state: gamestate, display:bool=True) -> packed_action:

        if display: print('Valid Moves:',len(state.getLegalMoves()))
        
        bestVal = float('-inf')
        bestMove = None
        for suggestmove in state.getLegalMoves(): # i htink the iseu is the moves are normalized moves...
            successor = state.getSuccessor(suggestmove)
            v = self.heuristic(successor)
            if v>bestVal:
                bestVal = v
                bestMove = suggestmove
        bestMove.denormalize(state.transform)
        print("Suggested Move: ", bestMove.suggest_format())
        bestMove.normalize(state.transform)
        
        while True: #this is to capture a transform or a move
            
            print('Undo: u')
            print('Redo: r')
            print('Replay: replay')
            print('Save: s')
            print('Pass off to AI: ai')
            wholeMoves = input(f"Player {state.player+1}: Enter xl1 yl1 dl1 tx ty tx ty or x, y, t, cw, ccw transforms: ")
            move_parts = wholeMoves.split()

            if len(move_parts)==0:
                move = bestMove
                return move

            #Transpose, Reflect x, Reflect y
            if len(move_parts)==1:
                instruction = move_parts[0].lower()
                if instruction == 'u':
                    return 'u'
                elif instruction == 'r':
                    return 'r'
                elif instruction == 'replay':
                    return 'replay'
                elif instruction == 's':
                    return 'save'
                elif instruction == 'ai':
                    return 'ai'
                
                elif instruction == "x":
                    transformList = [True,False,False]
                elif instruction == "y":
                    transformList = [False,True,False]
                elif instruction == "t":
                    transformList = [False,False,True]
                elif instruction == "cw":
                    transformList = [True,False,True]
                elif instruction == "ccw":
                    transformList = [False,True,True]
                else:
                    raise ValueError("Enter commands in specified format")
                
                state.update_denormalization(transformList)
                state.display()
                bestMove.denormalize(state.transform)
                print("Suggested Move: ", bestMove.suggest_format())
                bestMove.normalize(state.transform)
                continue
        
            elif ( (len(move_parts) != 7) and (len(move_parts) != 3) ):
                raise ValueError("Enter commands in specified format")
            else:
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