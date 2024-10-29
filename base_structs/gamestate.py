from base_structs.L_piece import L_piece
from base_structs.token_piece import token_piece

class gamestate():
    def __init__(self):
        self.L1 = L_piece(x=1,y=3,d='N')
        self.L2 = L_piece(x=4,y=2,d='S')
        self.T1 = token_piece(x=1,y=1)
        self.T2 = token_piece(x=4,y=4)
