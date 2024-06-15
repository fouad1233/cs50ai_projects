"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
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
    print("x num = " + str(x_count ))
    print("o num = " + str(o_count ))

    if x_count>o_count:
        return O
    else:
        return X
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == None:
                possible_actions.append( (i,j) )
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    game_player = player(board)
    new_board = deepcopy(board)
    if new_board[action[0]][action[1]] != EMPTY:
        #raise Exception("Invalid Move")
        pass
    else:
        new_board[action[0]][action[1]] = game_player
    return new_board    
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    score = utility(board)
    if score == 1:
        return X
    elif score == -1:
        return O
    else:
        return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    for player in [X, O]:
        # Check rows, columns, and diagonals
        for i in range(3):
            #if all elements in the row are the same as the player
            if all(board[i][j] == player for j in range(3)):
                return True
            #if all elements in the column are the same as the player
            if all(board[j][i] == player for j in range(3)):
                return True
            #if all elements in the diagonal are the same as the player
            """
            X 
                X   
                    X
            """
            if all(board[i][i] == player for i in range(3)):
                return True 
            """
                    X
                X   
            X        
            """
            if all(board[i][2 - i] == player for i in range(3)):
                return True
    return False


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
    game_player = player(board)
    if game_player == X:
        all_actions = actions(board)
        scores = []
        for action in all_actions:
            score = min_value(result(board, action))
            scores.append(score)
            if score == 1:
                return action
        max_score = max(scores)
        for score_num in range(0, len(scores)):
            if scores[score_num] == max_score:
                return all_actions[score_num]
    elif game_player == O:
        all_actions = actions(board)
        scores = []
        for action in all_actions:
            score = max_value(result(board, action))
            scores.append(score)
            if score == -1:
                return action
        min_score = min(scores)
        for score_num in range(0, len(scores)):
            if scores[score_num] == min_score:
                return all_actions[score_num]
    else:
        return None


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
