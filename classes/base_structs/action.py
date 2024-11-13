from classes.base_structs.L_piece import L_piece
from classes.base_structs.token_piece import token_piece

from typing import Tuple
from typing import Optional


class action():
    def __init__(self,l_piece_id:int,new_l_pos:Tuple[int,int,str],token_id:Optional[int],new_token_pos:Optional[Tuple[int,int]]):
        self.l_piece_id = l_piece_id
        self.new_l = L_piece(*new_l_pos)
        self.token_id = token_id
        if new_token_pos!=None:
            self.new_token = token_piece(*new_token_pos)
        else:
            self.new_token = None