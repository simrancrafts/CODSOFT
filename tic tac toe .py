import math

# Initialize the board
board = [' ' for _ in range(9)]

def print_board():
    print()
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')
    print()

def available_moves():
    return [i for i, spot in enumerate(board) if spot == ' ']

def winner(player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # columns
        [0, 4, 8], [2, 4, 6]             # diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def is_full():
    return ' ' not in board

def minimax(depth, is_maximizing):
    if winner('O'):
        return 1
    if winner('X'):
        return -1
    if is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves():
            board[move] = 'O'
            score = minimax(depth + 1, False)
            board[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in available_moves():
            board[move] = 'X'
            score = minimax(depth + 1, True)
            board[move] = ' '
            best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -math.inf
    move = None
    for m in available_moves():
        board[m] = 'O'
        score = minimax(0, False)
        board[m] = ' '
        if score > best_score:
            best_score = score
            move = m
    board[move] = 'O'

def play_game():
    print("Welcome to Tic-Tac-Toe!")
    print_board()

    while True:
        # Human turn
        move = int(input("Choose your move (0-8): "))
        if board[move] != ' ':
            print("Invalid move! Try again.")
            continue
        board[move] = 'X'
        print_board()
        if winner('X'):
            print("You win!")
            break
        if is_full():
            print("It's a tie!")
            break

        # AI turn
        ai_move()
        print("AI move:")
        print_board()
        if winner('O'):
            print("AI wins!")
            break
        if is_full():
            print("It's a tie!")
            break

if __name__ == "__main__":
    play_game()
