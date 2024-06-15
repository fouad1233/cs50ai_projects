"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if all(board[i][j] == EMPTY for i in range(3) for j in range(3)):
        return X
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    if x_count>o_count:
        return O
    else:
        return X
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    for player in [X, O]:
        # Check rows, columns, and diagonals
        for i in range(3):
            #if all elements in the row are the same as the player
            if all(board[i][j] == player for j in range(3)):
                return 1 
            #if all elements in the column are the same as the player
            if all(board[j][i] == player for j in range(3)):
                return 1 
            #if all elements in the diagonal are the same as the player
            """
            X 
                X   
                    X
            """
            if all(board[i][i] == player for i in range(3)):
                return 1 
            """
                    X
                X   
            X        
            """
            if all(board[i][2 - i] == player for i in range(3)):
                return 1 
    return 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    for player in [X, O]:
        # Check rows, columns, and diagonals
        for i in range(3):
            #if all elements in the row are the same as the player
            if all(board[i][j] == player for j in range(3)):
                return 1 if player == X else -1
            #if all elements in the column are the same as the player
            if all(board[j][i] == player for j in range(3)):
                return 1 if player == X else -1
            #if all elements in the diagonal are the same as the player
            """
            X 
                X   
                    X
            """
            if all(board[i][i] == player for i in range(3)):
                return 1 if player == X else -1
            """
                    X
                X   
            X        
            """
            if all(board[i][2 - i] == player for i in range(3)):
                return 1 if player == X else -1
    #if no player has won
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
