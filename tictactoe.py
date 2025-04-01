
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
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    # since X starts first, if the counts are equal, it's X's turn
    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:  # check for empty space
                result.add((i, j))
    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid action: Cell is already occupied.")
    
    # create a copy of board to avoid modifying original
    new_board = []
    for row in board:
        new_board.append(row[:])

    # set current player mark
    new_board[action[0]][action[1]] = player(board)
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win = utility(board)
    if win == 1:
        return X
    elif win == -1:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check for winner
    if winner(board) is not None:
        return True
    
    # check for empty spaces
    for row in board:
        if EMPTY in row:
            return False
    
    # match is draw
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    for i in range(3):
        #check rows
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return 1 if board[i][0] == X else -1
        #check columns
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return 1 if board[0][i] == X else -1
    #check first diagonal
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return 1 if board[0][0] == X else -1

    #check second diagonal
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return 1 if board[0][2] == X else -1

    return 0


def minimax(board, alpha=float('-inf'), beta=float('inf')):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)

    def max_value(board, alpha, beta): #helper function for maximizing "X"
        if terminal(board):
            return utility(board), None
        v, best_action = float('-inf'), None # initialize v to negative infinity
        for action in actions(board): # iterate through all possible actions
            new_v, _ = min_value(result(board, action), alpha, beta) # returns the winner if action is taken
            if new_v > v:
                v, best_action = new_v, action
            alpha = max(alpha, v)
            if alpha >= beta:  # Pruning step
                break
        return v, best_action

    def min_value(board, alpha, beta): #helper function for minimizing "O"
        if terminal(board):
            return utility(board), None
        v, best_action = float('inf'), None # initialize v to positive infinity
        for action in actions(board): # iterate through all possible actions
            new_v, _ = max_value(result(board, action), alpha, beta) # returns the winner if action is taken
            if new_v < v:
                v, best_action = new_v, action
            beta = min(beta, v)
            if alpha >= beta:  # Pruning step
                break
        return v, best_action

    _, best_move = max_value(board, alpha, beta) if current_player == X else min_value(board, alpha, beta)
    return best_move
