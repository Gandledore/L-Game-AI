from play import play
import numpy as np



#inf minimax vs inf prune
print("\ninf vs infp: \n")
players = ((1,-1,0),(1,-1,1))
winners, turns, turn_times = play(gm=players,N=100000,display=False)


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
print(f'First Turns took: p1: {1000*turn_times[0][0]:3.3f}ms | p2 {1000*turn_times[1][0]:3.3f}ms')
print(f'Avg Turn Times after first turn: p1: {1000*np.mean(turn_times[0][1:]):3.3f}ms | p2: {1000*np.mean(turn_times[1][1:]):3.3f}ms')


#agent vs random
print("\ninf vs ran: \n")
players = ((1,-1,0),(2,None,None))
winners, turns, turn_times = play(gm=players,N=100000,display=False)


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
print(f'First Turns took: p1: {1000*turn_times[0][0]:3.3f}ms | p2 {1000*turn_times[1][0]:3.3f}ms')
print(f'Avg Turn Times after first turn: p1: {1000*np.mean(turn_times[0][1:]):3.3f}ms | p2: {1000*np.mean(turn_times[1][1:]):3.3f}ms')


if len(counts)==3 and counts[2]>0:
    seed_losers = np.where(winners==2)[0]
    print(seed_losers)
    print(turns[seed_losers])








#random vs agent
print("\nran vs inf: \n")
players = ((2,None,None),(1,-1,0))
winners, turns, turn_times = play(gm=players,N=100000,display=False)


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

if len(counts)==3 and counts[2]>0:
    seed_losers = np.where(winners==1)[0]
    print(seed_losers)
    print(turns[seed_losers])




#agent vs agent
print("\ninf vs inf: \n")
players = ((1,-1,0),(1,-1,0))
winners, turns, turn_times = play(gm=players,N=1,display=False)


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





#agent vs agent
print("\ninf vs d1: \n")
players = ((1,-1,0),(1,1,0))
winners, turns, turn_times = play(gm=players,N=1,display=False)


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



#agent vs agent
print("\nd1 vs inf: \n")
players = ((1,1,0),(1,-1,0))
winners, turns, turn_times = play(gm=players,N=1,display=False)

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



print("\nd1 vs d1: \n")
players = ((1,1,0),(1,1,0))
winners, turns, turn_times = play(gm=players,N=1,display=False)


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


print("\nd1p vs d1: \n")
players = ((1,1,0),(1,1,0))
winners, turns, turn_times = play(gm=players,N=1,display=False)


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




print("\nd3 vs d3: \n")
players = ((1,3,0),(1,3,0))
winners, turns, turn_times = play(gm=players,N=1,display=False)


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


print("\nd5 vs d1: \n")
players = ((1,5,0),(1,1,0))
winners, turns, turn_times = play(gm=players,N=1,display=False)


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




print("\nd5P vs d1: \n")
players = ((1,5,1),(1,1,0))
winners, turns, turn_times = play(gm=players,N=1,display=False)


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


print("\nd1 vs d5: \n")
players = ((1,1,0),(1,5,0))
winners, turns, turn_times = play(gm=players,N=1,display=False)

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


print("\nd1 vs d5P: \n")
players = ((1,1,0),(1,5,1))
winners, turns, turn_times = play(gm=players,N=1,display=False)

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


print("\nd5P vs d5: \n")
players = ((1,5,1),(1,5,0))
winners, turns, turn_times = play(gm=players,N=1,display=False)


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


print("\nd5 vs d5P: \n")
players = ((1,5,0),(1,5,1))
winners, turns, turn_times = play(gm=players,N=1,display=False)

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




print("\nd4 vs d4: \n")
players = ((1,4,0),(1,4,0))
winners, turns, turn_times = play(gm=players,N=1,display=False)

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



print("\nd5 vs d4: \n")
players = ((1,5,0),(1,4,0))
winners, turns, turn_times = play(gm=players,N=1,display=False)

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

