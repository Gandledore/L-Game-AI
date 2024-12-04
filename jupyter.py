from play import play

#agent vs random
winners, turns, turn_times = play(gm=3,N=100000,display=False)

import numpy as np

counts = np.bincount(winners)
for i in range(len(counts)):
    if i==0:
        print(f'Players tied {counts[i]} times {100*counts[i]/np.sum(counts):.3f}%')
    else:
        try:
            print(f'Player {i} won {counts[i]} times ({100*counts[i]/np.sum(counts):.3f}%)')
        except IndexError as e:
            print(f'Player {i} won 0 times (0%)')
print()
print('Avg Turns:',np.mean(turns))
print('Min Turns:',np.min(turns))
print('Max Turns:',np.max(turns))
print(f'Avg Turn Times: p1: {1000*np.mean(turn_times[0]):3.3f}ms | p2: {1000*np.mean(turn_times[1]):3.3f}ms')
print(f'First Turns took: p1: {turn_times[0][0]:.1f}s | p2 {1000*turn_times[1][0]:3.3f}ms')
print(f'Avg Turn Times after first turn: p1: {1000*np.mean(turn_times[0][1:]):3.3f}ms | p2: {1000*np.mean(turn_times[1][1:]):3.3f}ms')

from play import play

#random vs agent
winners, turns, turn_times = play(gm=4,N=100000,display=False)

import numpy as np

counts = np.bincount(winners)
for i in range(len(counts)):
    if i==0:
        print(f'Players tied {counts[i]} times {100*counts[i]/np.sum(counts):.3f}%')
    else:
        try:
            print(f'Player {i} won {counts[i]} times ({100*counts[i]/np.sum(counts):.3f}%)')
        except IndexError as e:
            print(f'Player {i} won 0 times (0%)')
print()
print('Avg Turns:',np.mean(turns))
print('Min Turns:',np.min(turns))
print('Max Turns:',np.max(turns))
print(f'Avg Turn Times: p1: {1000*np.mean(turn_times[0]):3.3f}ms | p2: {1000*np.mean(turn_times[1]):3.3f}ms')
print(f'First Turns took: p1: {turn_times[0][0]:.1f}s | p2 {1000*turn_times[1][0]:3.3f}ms')
print(f'Avg Turn Times after first turn: p1: {1000*np.mean(turn_times[0][1:]):3.3f}ms | p2: {1000*np.mean(turn_times[1][1:]):3.3f}ms')

from play import play

#agent vs agent
winners, turns, turn_times = play(gm=2,N=10000,display=False)

import numpy as np

counts = np.bincount(winners)
for i in range(len(counts)):
    if i==0:
        print(f'Players tied {counts[i]} times {100*counts[i]/np.sum(counts):.3f}%')
    else:
        try:
            print(f'Player {i} won {counts[i]} times ({100*counts[i]/np.sum(counts):.3f}%)')
        except IndexError as e:
            print(f'Player {i} won 0 times (0%)')
print('Avg Turns:',np.mean(turns))
print('Min Turns:',np.min(turns))
print('Max Turns:',np.max(turns))
print(f'Avg Turn Times: p1: {1000*np.mean(turn_times[0]):3.3f}ms | p2: {1000*np.mean(turn_times[1]):3.3f}ms')
print(f'First Turns took: p1: {turn_times[0][0]:.1f}s | p2 {1000*turn_times[1][0]:3.3f}ms')
print(f'Avg Turn Times after first turn: p1: {1000*np.mean(turn_times[0][1:]):3.3f}ms | p2: {1000*np.mean(turn_times[1][1:]):3.3f}ms')
