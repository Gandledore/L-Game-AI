# L-Game-AI
CSE 175 Project to design an AI agent to play the L-Game

Ryan Milstrey
Jet Lin
Carolyn Cui
16 December 2024
L Game Report
Sources, Packages, and Dependencies

External:
pip 24.2
numpy 2.1.x
tqdm 4.67.1
Built-in:
sys, subprocess, time
Typing, pickle, abc, random


“L Game.” Wikipedia, Wikimedia Foundation, 10 Dec. 2023, en.wikipedia.org/wiki/L_game. 
Russell, Stuart J., and Peter Norvig. Artificial Intelligence: A Modern Approach. Pearson, 2021. 
L Game Interactive - Henry Wise Wood Math Club, hwwmath.looiwenli.com/l-game. Accessed 16 Dec. 2024. 
Contribution
Ryan
Project direction
Normalization
Caching
Jet
Heuristic implementation
Alpha beta and Minimax implementation.
Bonus features: Suggested move, transformations, initial state.
Carolyn
Bonus features: undo, redo, save, load, switch to AI/computer play, UI, instruction handling
Improved heuristics, unit testing
Designing the L Game
We chose an object-oriented approach to enhance modularization and standardization in code. We wanted changing and updating players to be easy and for each object to interface cleanly with each other.
Players
We took an object-oriented approach to implementing our players. We have an abstract class Player which definites a player ID, and 2 abstract classes, instructionHandler, and getMove, which are inherited by three types of players:

Human
Agent
Random
Controlled by user
Can transform board
Undo
Redo replay
Swap to AI	
Suggested move
Minimax depth customizable (int or infinite)
Prune parameter
Can’t lose with depth at least 2
Plays random legal move

Gamestate Design
Normalization
To reduce search space and memory, the game was refactored so that internally it only played within a normalized subset of all states, exploiting equivalence in transformations such as reflection, rotation and transposition.  To achieve this, a normalized state was defined as the first player’s L piece corner being in the top left quadrant, with the long leg facing east. Any state’s normalization transformation can be computed in constant time.  In order to have it display correctly for the human, a transform function was stored, to effectively remember which branch a human expects to be on.
Game Loop
The play function controls the overall flow of the game. At game initialization, the script asks whether the user would like to load a game. If none is provided or if the user does not want to load a saved file, then the 

If no game is loaded, the user is prompted to input initial coordinates or use the default starting configuration. The entered configuration is then validated internally and externally confirmed by the user, and if it passes the check, a new Game object is created. There is exception handling for incorrectly entered configurations. 

The core game loop continues until a player wins or a tie condition (max turns) occurs. Each iteration of the loop represents a single turn.

Firstly, the board is displayed. The game determines the current player (0 or 1) and a message indicating the current player’s turn and the total turn count is printed.

The instruction handler comes into play next, as the game enters a loop that runs for a maximum of 5 times, which allows the player to attempt up to 5 moves (not counting valid moves or instructions). Once 5 attempts have been used, the game terminates.

The instruction handler is called on each player’s turn to get an instruction from them (or, if the player is an agent, it simply requests a move). There is exception handling for invalid inputs.

The game concludes when there are no more legal moves for a player, or when the maximum turn (64) is reached. The winning player is printed or the game is declared a draw. The total number of turns taken is also printed. 64 was chosen as the maximum number of moves before a tie is declared because the longest game lasted 32 moves when putting our agent against a random agent; we simply doubled this number.

A post-game menu allows the user to replay the game, save the game, or continue, after which they are prompted as to whether they would like to play again.
Designing the Agent
Heuristic Evaluation Function
Our heuristic comprises two parts:
Action Heuristic
The action heuristic evaluates the value of a single move. We check to see if we have already computed the score for this move. If so, then return the known score. Otherwise, the score is calculated.

There are three components, each with a different weight and evaluated at the end before being added together for a final score:
core_weight = 25
Evaluation: Positive; reward states with more of the L in the core
corner_weight = 40
Evaluation: Negative; if a part of the L exists in the corner, penalize
killer_token_weight = 10
Evaluation: Positive; reward states where the tokens are in “killer” positions

After evaluating this move, we add the individual components together, save the result into our existing dictionary of action heuristics, and then return the result.
State Heuristic
Our heuristic takes in the opponent’s state.  
We then calculate the score based on 6 contributors/criteria:
The number of moves the state has is penalized if it's the opponent's turn, and rewarded if the player's turn.
We find the intersection of the player L coordinates and the core coordinates, and reward the size of this intersection or penalize if it's the opponent’s turn. The reasoning for this is there are 15 possible winning states each involving the winning L piece controlling the core of the board.
Expel core is synonymous with the criteria 2 where we penalize the player when the opponent is controlling the core.
We penalize being in the corner with the same intersection trick and reward forcing the opponent into a corner, because all 15 losing states involve the losing piece occupying the corners.
If the state is a state in which the player or opponent can force a win, it is considered a death state.  If a state is a death state, it is penalized with infinite value if it’s the opponents problem, or rewarded similarly if it's the player’s turn.
We then return the weighted sum of these.
Minimax Core
The minimax algorithm comprises:
AlphaBetaSearch
MaxValueAB
MinValueAB

MaxValueAB and MinValueAB functions represent the maximizing and minimizing player's turns, respectively. They recursively call each other, exploring the game tree up to the specified depth for the agent. At the terminal nodes (depth reached, game over, or death state), the value of the state is estimated by the heuristic functions described above.

Specific loss states are pre-calculated and stored in a set of “death states” to reduce computation and increase efficiency for infinite lookahead search, and to improve small depth searches, to prevent them from losing.
Checking for Ties and Cycles
To check for ties if we encounter a repeated state in a DFS path, then we are potentially dealing with a tie. From there, we conduct a search limited in depth to “check_tie_depth,” which has been set to 2, because of the known death states and how a loss can be forced within two plays. This is essentially a quiescence check for the tie state (i.e. “Can a win or loss be forced in the next check_tie_depth turns?”).  This is necessary because we have not evaluated all children of the original state in the DFS path.
Optimizations
Move Switching (self.played_states)
To avoid predictable play and in the case a loop is encountered, the agent keeps track of how many times each state has been encountered during a game. It then selects a different optimal move (among the equivalency in values for best optimal moves) each time a state is revisited.
Transposition Table (self.finished) and Caching:
This dictionary stores previously evaluated game states and their associated values (search depth, alpha, beta, optimal moves). A dictionary was chosen for its O(1) lookup access. This way, we avoid re-evaluating entire subtrees multiple times, substantially speeding up the search process, particularly during full-depth searches (infinite lookahead). The depth is used to ensure the data is sufficiently accurate for current needs, the alpha and beta allow determining if immediate pruning is possible, and optimal moves stores all moves found with value equivalent to best value, move switching.
Packed Action
Previously, precomputing all legal moves took an unreasonable amount of time, mainly due to the size of the action variable.  The class was modified to use a struct.pack, which compresses the data to only a few bytes to store the data, rather than variables with large overhead which is the tendency of Python.  This compressed it from 1.2kB each, to just under 40B.
Bonus Features
Customizable Initial State
A player has the ability to specify an initial configuration of the L pieces and tokens. Apart from being a cool feature, it was quite useful when dueling with other AI agents or wanting to debug specific scenarios. After receiving a valid initial board configuration, the board is displayed and the player can confirm whether this is the state they intended. If not, they can re-enter the state or just hit enter for the default state as usual.
Suggested Move
Suggested Move for Human players gets the move with the best heuristic score, which is equivalent to a depth 1 minimax search.
Board Transformations: Reflection, Transposition, and CW & CCW
A Human player can enter “x” or “y" for reflection across its respective axis, “t” for transposition (visually identical to matrix transpositions), “cw” for clockwise rotation, and “ccw” for counterclockwise rotation. 
These transformations were done by creating a transformation list. Then, we take our normalized state and apply an “update_denormalization” when displaying the game so that our new display has the user’s transformations. It would be incorrect to update the actual data, as the normalized state does not change under any such transformation. We then make sure the suggested bestMove is also re-denormalized for user readability.
Switch Human Player to Computer (AI) — “swap”
A human player has the ability to pass off the game to an AI agent with a depth and prune status of their choosing. Once the AI has taken over, there is no way to take back control…
Undo, Redo, & Replay
In order to optimize undo, redo and replay, we opted to track the game history through a list of game states, indexed by a turn counter. Undo and Redo return a boolean representing success, while Replay simply displays all game states up to the current turn, with a short delay between each.

In the new implementation that only uses history accesses and overwrites in the case of a new move, Undo is not possible (returns False) if there are fewer than 3 total turns in the game (because we save the initial state as well), taking into account alternating players. If there are more than 3 turns, then we decrement turns by 2, returning to the last action executed by the current player. The state is set to the state at that turn. Moves are still saved only after a new move.

Replay simply prints all the moves made since the game started by accessing the history list one entry at a time, with a one-second delay between accesses.
Save & Load Game
Human players can choose to save the game at any point in time, which “pickles” the gamestate history list and saves everything except the players. At the start of the game, the user is prompted to load a game. If a game file is successfully loaded, they can then customize the players again.
Game Over Menu & Play Again
When a game concludes, users are prompted with a menu that asks if they’d like to save the game, replay it, or continue. Afterward, users are prompted again: would they like to play again (y/n)?
Instruction Handler
To clean up the human player’s interactive menu and clean up code, we implemented an instruction handler that prompts the human while routing inputs and outputs depending on the player. The instructions are shown once at the start of the game, and users can bring it up again by entering “help.” Though the instruction handler is just a wrapper for getMove for the agent and random agent, it also parses all human inputs for the 6 possible instructions we have: help, move, undo, redo, replay, save, transform, and let the AI take over.
Known Bugs
“Loading/Loaded preprocessed states” is printed twice when running L-game.py. This is not the case when running play.py
There is an incompatibility when generating saved game files from different versions of the game. The .pkl files generated by L-game.py (single file version) cannot be used by play.py. However, play.py’s generated files can be used by L-game.py.
Future Ideas
States could potentially be normalized by player turn as well, so that the current player’s turn is always the first L position.
Better heuristic and use a neural network or other technique (e.g. Bayesian optimization) to find optimal weights.
The heuristic could be improved by rewarding more advanced offensive techniques like blocking off a 3x3 square or blocking off half the board, as suggested by the Wikipedia L Game article. This should be easily implemented given the normalized space.
Easy, Medium, Hard mode
Modularize the heuristic to be a passable parameter to agent
Adjust heuristic to be less or more aggressive (weights, no corner/core detection, etc.)
Random Agent can use a noisy heuristic to approximate a decent player that makes mistakes randomly.
L Game Discussion
Typical branching factor
Unlike games like chess, there is no definite branching factor and it is heavily dependent on the players. From computing the legal moves, we have determined the average is 88.9, the max is 221, and the minimum is 0 when there are no moves possible.
Maximum game depth
This implementation of the L game can run up to an infinite depth. Actually, when infinite lookahead is requested, the agent will go ahead and pre-compute all possible moves and save all states to the transposition table.
Terminal states
Under no transformations and for each player, there are 15 possible terminal states.
