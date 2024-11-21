import struct

from classes.base_structs.L_piece import L_piece
from classes.base_structs.token_piece import token_piece

from typing import Tuple
from typing import Optional

class packed_action:
    __slots__ = ('_data',)
    _format = '3B c 3B'

    def __init__(self, l_piece_id:int=0, new_l_pos:Tuple[int,int,str]=(1, 3, 'S'), token_id:int=0, new_token_pos:Tuple[int,int]=(3, 1)):
        assert l_piece_id in {0,1},f"action L_id={l_piece_id} not in {0,1}"
        assert token_id in {0,1,255},f"action T_id={token_id} not in {0,1,255}"
        assert new_l_pos[0] in L_piece._POSSIBLE_SETS['x'], f"action Lx={new_l_pos[0]} not in {L_piece._POSSIBLE_SETS['x']}"
        assert new_l_pos[1] in L_piece._POSSIBLE_SETS['y'], f"action Lx={new_l_pos[0]} not in {L_piece._POSSIBLE_SETS['y']}"
        assert new_l_pos[2] in L_piece._POSSIBLE_SETS['d'], f"action Lx={new_l_pos[0]} not in {L_piece._POSSIBLE_SETS['d']}"
        
        self._data = struct.pack(packed_action._format, 
                                 l_piece_id, new_l_pos[0], new_l_pos[1], new_l_pos[2].encode('utf-8'), 
                                 token_id, new_token_pos[0], new_token_pos[1])

    def get_rep(self):
        return struct.unpack(packed_action._format, self._data)

    def __repr__(self):
        unpacked = struct.unpack(packed_action._format,self._data)
        return f'({unpacked[0]},({unpacked[1]},{unpacked[2]},{unpacked[3].decode('utf-8')}),{unpacked[4]},({unpacked[5]},{unpacked[6]})'