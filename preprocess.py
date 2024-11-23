from classes.base_structs.gamestate import gamestate
from classes.base_structs.action import packed_action

import numpy as np
import pickle
from pympler import asizeof as asf

s = gamestate()

print(f"Computed {len(gamestate._legalMoves)} states' legal mvoes")

lm = gamestate._legalMoves

print(f"Memory: {asf.asizeof(lm)/1000000:.2f} MB")
b = np.array([len(v) for k,v in lm.items()])
avg_b = np.mean(b)
max_b = np.max(b)
print(f'Avg branching factor: {avg_b:.1f}')
print(f'Max branching factor: {max_b}')

with open(gamestate._legalMoves_path,'rb') as f:
    preprocessed_data = pickle.load(f)
    
print(f"Saved Memory: {asf.asizeof(lm)/1000000:.2f} MB")
print(f"Loaded Memory: {asf.asizeof(preprocessed_data)/1000000:.2f} MB")

print(s)
s.denormalize()
print(s)
s.normalize(s.transform)
print(s)

print('Test 0:',type(preprocessed_data[s])==np.ndarray)
print('Test 1:',type(preprocessed_data[s][0])==packed_action)
print('Test 2:',all(k.player==m.get_rep()[0] for k,v in preprocessed_data.items() for m in v))
g = s.getSuccessor(preprocessed_data[s][7])
print('Test 3:',type(preprocessed_data[g])==np.ndarray)
print('Test 4:',type(preprocessed_data[g][0])==packed_action)