import struct

from classes.base_structs.L_piece import L_piece
from classes.base_structs.token_piece import token_piece

from typing import Tuple
import numpy as np

class packed_action:
    __slots__ = ('data',)
    _format = '3B c 4B'

    def __init__(self, l_piece_id:int=0, new_l_pos:Tuple[int,int,str]=(1, 3, 'S'), current_token_pos:Tuple[int,int]=(1,1), new_token_pos:Tuple[int,int]=(3, 1)):
        assert l_piece_id in {0,1},f"action L_id={l_piece_id} not in {0,1}"
        assert current_token_pos in token_piece._POSSIBLE_POS,f"action current_t_pos={current_token_pos} not in {token_piece._POSSIBLE_POS}"
        assert new_token_pos in token_piece._POSSIBLE_POS,f"action current_t_pos={new_token_pos} not in {token_piece._POSSIBLE_POS}"
        assert new_l_pos[0] in L_piece._POSSIBLE_SETS['x'], f"action Lx={new_l_pos[0]} not in {L_piece._POSSIBLE_SETS['x']}"
        assert new_l_pos[1] in L_piece._POSSIBLE_SETS['y'], f"action Lx={new_l_pos[0]} not in {L_piece._POSSIBLE_SETS['y']}"
        assert new_l_pos[2] in L_piece._POSSIBLE_SETS['d'], f"action Lx={new_l_pos[0]} not in {L_piece._POSSIBLE_SETS['d']}"
        
        self.data = struct.pack(packed_action._format, 
                                 l_piece_id, new_l_pos[0], new_l_pos[1], new_l_pos[2].encode('utf-8'), 
                                 current_token_pos[0], current_token_pos[1],
                                 new_token_pos[0], new_token_pos[1])

    def get_rep(self):
        return struct.unpack(packed_action._format, self.data)

    def __repr__(self):
        unpacked = struct.unpack(packed_action._format,self.data)
        return f'({unpacked[0]},({unpacked[1]},{unpacked[2]},{unpacked[3].decode('utf-8')}),({unpacked[4]},{unpacked[5]}),({unpacked[6]},{unpacked[7]}))'
    
    def normalize(self,transform:np.ndarray[bool])->None:
        l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, curr_token_pos_x, curr_token_pos_y, new_token_pos_x,new_token_pos_y = struct.unpack(packed_action._format,self.data)
        new_l_pos_d = new_l_pos_d.decode('utf-8')
        
        #reflect x
        if transform[0]:
            new_l_pos_x = 5 - new_l_pos_x
            if curr_token_pos_x != 0:
                curr_token_pos_x = 5 - curr_token_pos_x
                new_token_pos_x = 5 - new_token_pos_x
            new_l_pos_d = L_piece._reflection_map[new_l_pos_d] if new_l_pos_d in ['E','W'] else new_l_pos_d
        
        #reflect y
        if transform[1]:
            new_l_pos_y = 5 - new_l_pos_y
            if curr_token_pos_y != 0:
                print("if ther is  token move")
                curr_token_pos_y = 5 - curr_token_pos_y
                new_token_pos_y = 5 - new_token_pos_y
            new_l_pos_d = L_piece._reflection_map[new_l_pos_d] if new_l_pos_d in ['N','S'] else new_l_pos_d
        
        #transpose
        if transform[2]:
            new_l_pos_d = (L_piece._transpose_map[new_l_pos_d])
            
            temp = curr_token_pos_x
            curr_token_pos_x = curr_token_pos_y
            curr_token_pos_y = temp
            
            temp = new_token_pos_x
            new_token_pos_x = new_token_pos_y
            new_token_pos_y = temp
        
        #save transformed data
        self.data = struct.pack(packed_action._format,
                                l_piece_id,new_l_pos_x,new_l_pos_y,new_l_pos_d.encode('utf-8'),
                                curr_token_pos_x,curr_token_pos_y,
                                new_token_pos_x,new_token_pos_y)
        
    def denormalize(self,transform:np.ndarray[bool])->None:
        l_piece_id, new_l_pos_x, new_l_pos_y, new_l_pos_d, curr_token_pos_x, curr_token_pos_y, new_token_pos_x,new_token_pos_y = struct.unpack(packed_action._format,self.data)
        new_l_pos_d = new_l_pos_d.decode('utf-8')
        
        #transpose
        if transform[2]:
            new_l_pos_d = (L_piece._transpose_map[new_l_pos_d])
            
            temp = curr_token_pos_x
            curr_token_pos_x = curr_token_pos_y
            curr_token_pos_y = temp
            
            temp = new_token_pos_x
            new_token_pos_x = new_token_pos_y
            new_token_pos_y = temp
        
        #reflect y
        if transform[1]:
            new_l_pos_y = 5 - new_l_pos_y
            curr_token_pos_y = 5 - curr_token_pos_y
            new_token_pos_y = 5 - new_token_pos_y
            new_l_pos_d = L_piece._reflection_map[new_l_pos_d] if new_l_pos_d in ['N','S'] else new_l_pos_d
        
        #reflect x
        if transform[0]:
            new_l_pos_x = 5 - new_l_pos_x
            curr_token_pos_x = 5 - curr_token_pos_x
            new_token_pos_x = 5 - new_token_pos_x
            new_l_pos_d = L_piece._reflection_map[new_l_pos_d] if new_l_pos_d in ['E','W'] else new_l_pos_d