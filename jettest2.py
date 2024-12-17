from play import play
import numpy as np

# Define all the player combinations you'd like to test
player_combinations = [
    ((1, -1, 0), (1, -1, 1)),  # Minimax vs Minimax with pruning
    ((1, -1, 0), (2, None, None)),  # Minimax vs Random
    ((1, -1, 1), (2, None, None)),  # Minimax with pruning vs Random
    ((2, None, None), (2, None, None))  # Random vs Random
]

# Run each combination of players
for players in player_combinations:
    print(f"\nTesting with players: {players[0]} vs {players[1]}")
    winners, turns, turn_times = play(gm=players, N=100000, display=False)

    # Count and display the results
    counts = np.bincount(winners)
    for i in range(len(counts)):
        if i == 0:
            print(f'Players tied {counts[i]} times ({100 * counts[i] / np.sum(counts):.3f}%)')
        else:
            print(f'Player {i} won {counts[i]} times ({100 * counts[i] / np.sum(counts):.3f}%)')
    
    # Display statistics
    print()
    print('Avg Turns:', np.mean(turns))
    print('Min Turns:', np.min(turns))
    print('Max Turns:', np.max(turns))
    print(f'Avg Turn Times: p1: {1000 * np.mean(turn_times[0]):3.3f}ms | p2: {1000 * np.mean(turn_times[1]):3.3f}ms')
    print(f'First Turns took: p1: {1000 * turn_times[0][0]:3.3f}ms | p2 {1000 * turn_times[1][0]:3.3f}ms')
    print(f'Avg Turn Times after first turn: p1: {1000 * np.mean(turn_times[0][1:]):3.3f}ms | p2: {1000 * np.mean(turn_times[1][1:]):3.3f}ms')
    
    # Additional analysis for seeded losers if necessary
    if len(counts) == 3 and counts[2] > 0:
        seed_losers = np.where(winners == 2)[0]
        print(f"Seed losers: {seed_losers}")
        print(f"Turns for seed losers: {turns[seed_losers]}")
