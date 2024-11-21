from classes.base_structs.L_piece import L_piece
from classes.base_structs.token_piece import token_piece

from typing import Tuple
from typing import Optional

class action():
    def __init__(self,l_piece_id:int,new_l_pos:Tuple[int,int,str],token_id:Optional[int],new_token_pos:Optional[Tuple[int,int]]):
        assert l_piece_id in {0,1},f"action initialization failed. {l_piece_id} not in {0,1}"
        assert token_id in {None,-1,0,1},f"action initialization failed. {token_id} not in {None,-1,0,1}"
        
        self.l_piece_id = l_piece_id
        self.new_l = L_piece(*new_l_pos)
        self.token_id = token_id
        if new_token_pos!=None:
            self.new_token = token_piece(*new_token_pos)
        else:
            self.new_token = None
            
    def __repr__(self):
        return f'L_id: {self.l_piece_id} | new_L_pos: {self.new_l} | T_id: {self.token_id} | new_T_pos: {self.new_token}'

    def format_move(self) -> str:
        l_str = f"{self.new_l.x} {self.new_l.y} {self.new_l.short_leg_direction}"
        if self.new_token is not None:
            t_str = f"{self.new_token.x} {self.new_token.y}"
            return f"L{self.l_piece_id+1}: {l_str} | T{self.token_id+1}: {t_str}"
        else:
            return l_str