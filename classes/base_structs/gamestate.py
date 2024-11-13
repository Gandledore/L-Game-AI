from classes.base_structs.L_piece import L_piece
from classes.base_structs.token_piece import token_piece

class gamestate():
    def __init__(self):
        self.L_pieces = [L_piece(x=1,y=3,d='N'),L_piece(x=4,y=2,d='S')]
        self.token_pieces = [token_piece(x=1,y=1),token_piece(x=4,y=4)]
    def __repr__(self):
        return f"L pieces: {[l for l in self.L_pieces]}\nT pieces {[t for t in self.token_pieces]}"
