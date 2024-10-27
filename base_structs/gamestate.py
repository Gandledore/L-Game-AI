import L_piece
import token_piece

class gamestate():
    def __init__(self):
        self.L1 = L_piece(x=1,y=3,d='E')
        self.L2 = L_piece(x=4,y=2,d='W')
        self.T1 = token_piece(x=1,y=1)
        self.T2 = token_piece(x=4,y=4)