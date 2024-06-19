# CS50 AI Projects 

## Lecture 0: Search

Lecture topics :

* [Depth-First Search](https://cs50.harvard.edu/ai/2024/notes/0/#depth-first-search)
* [Breadth-First Search](https://cs50.harvard.edu/ai/2024/notes/0/#breadth-first-search)
* [Greedy Best-First Search](https://cs50.harvard.edu/ai/2024/notes/0/#greedy-best-first-search)
* [A* Search](https://cs50.harvard.edu/ai/2024/notes/0/#a-search)
* [Minimax for adversial search](https://cs50.harvard.edu/ai/2024/notes/0/#minimax)
* [Alpha-Beta Pruning (optimizing minimax)](https://cs50.harvard.edu/ai/2024/notes/0/#alpha-beta-pruning)

### Lecture 0: Projects

#### TicTacToe

Requirements: 

* Once in the directory for the project, run `pip3 install -r requirements.txt` to install the required Python package (`pygame`) for this project.

Complete the implementations of `player`, `actions`, `result`, `winner`, `terminal`, `utility`, and `minimax`.

* The `player` function should take a `board` state as input, and return which player’s turn it is (either `X` or `O`).
  * In the initial game state, `X` gets the first move. Subsequently, the player alternates with each additional move.
  * Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
* The `actions` function should return a `set` of all of the possible actions that can be taken on a given board.
  * Each action should be represented as a tuple `(i, j)` where `i` corresponds to the row of the move (`0`, `1`, or `2`) and `j` corresponds to which cell in the row corresponds to the move (also `0`, `1`, or `2`).
  * Possible moves are any cells on the board that do not already have an `X` or an `O` in them.
  * Any return value is acceptable if a terminal board is provided as input.
* The `result` function takes a `board` and an `action` as input, and should return a new board state, without modifying the original board.
  * If `action` is not a valid action for the board, your program should [raise an exception](https://docs.python.org/3/tutorial/errors.html#raising-exceptions).
  * The returned board state should be the board that would result from taking the original input board, and letting the player whose turn it is make their move at the cell indicated by the input action.
  * Importantly, the original board should be left unmodified: since Minimax will ultimately require considering many different board states during its computation. This means that simply updating a cell in `board` itself is not a correct implementation of the `result` function. You’ll likely want to make a [deep copy](https://docs.python.org/3/library/copy.html#copy.deepcopy) of the board first before making any changes.
* The `winner` function should accept a `board` as input, and return the winner of the board if there is one.
  * If the X player has won the game, your function should return `X`. If the O player has won the game, your function should return `O`.
  * One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
  * You may assume that there will be at most one winner (that is, no board will ever have both players with three-in-a-row, since that would be an invalid board state).
  * If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the function should return `None`.
* The `terminal` function should accept a `board` as input, and return a boolean value indicating whether the game is over.
  * If the game is over, either because someone has won the game or because all cells have been filled without anyone winning, the function should return `True`.
  * Otherwise, the function should return `False` if the game is still in progress.
* The `utility` function should accept a terminal `board` as input and output the utility of the board.
  * If X has won the game, the utility is `1`. If O has won the game, the utility is `-1`. If the game has ended in a tie, the utility is `0`.
  * You may assume `utility` will only be called on a `board` if `terminal(board)` is `True`.
* The `minimax` function should take a `board` as input, and return the optimal move for the player to move on that board.
  * The move returned should be the optimal action `(i, j)` that is one of the allowable actions on the board. If multiple moves are equally optimal, any of those moves is acceptable.
  * If the `board` is a terminal board, the `minimax` function should return `None`.

For all functions that accept a `board` as input, you may assume that it is a valid board (namely, that it is a list that contains three rows, each with three values of either `X`, `O`, or `EMPTY`). You should not modify the function declarations (the order or number of arguments to each function) provided.

Once all functions are implemented correctly, you should be able to run `python runner.py` and play against your AI. And, since Tic-Tac-Toe is a tie given optimal play by both sides, you should never be able to beat the AI (though if you don’t play optimally as well, it may beat you!)


#### Degrees

**Problem Definition:**

* The task is to find the shortest path between any two actors.
* This path is determined by selecting a sequence of movies that connect the two actors.

**Example:**

* The shortest path between Jennifer Lawrence and Tom Hanks is 2 steps:
  * Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class.”
  * Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”

**Modeling as a Search Problem:**

* **States:** The states are the actors.
* **Actions:** The actions are movies, which allow us to move from one actor to another (it is true that a movie could lead to multiple actors, but this is acceptable for this problem).
* **Initial State and Goal State:** The initial state and goal state are defined by the two actors we are trying to connect.
* **Method:** By using breadth-first search, we can find the shortest path from one actor to another.
