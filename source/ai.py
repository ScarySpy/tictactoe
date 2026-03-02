import random


def get_bot_move(cells, algo):
    moves = [i for i in range(1, 10) if not isinstance(cells[i], str)]
    if not moves:
        return None
    if algo == "simple":
        return random.choice(moves)

    best_val, best_move = -float("inf"), moves[0]
    for i in moves:
        trial = list(cells)
        trial[i] = "o"
        score = minimax(trial, 0, False)
        if score > best_val:
            best_val, best_move = score, i
    return best_move


def minimax(b, depth, is_max):
    def check(p, board):
        c = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],
            [1, 5, 9],
            [3, 5, 7],
        ]
        return any(
            board[idx[0]] == p and board[idx[1]] == p and board[idx[2]] == p
            for idx in c
        )

    if check("o", b):
        return 10
    if check("x", b):
        return -10
    moves = [i for i in range(1, 10) if not isinstance(b[i], str)]
    if not moves:
        return 0

    if is_max:
        best = -float("inf")
        for i in moves:
            b2 = list(b)
            b2[i] = "o"
            best = max(best, minimax(b2, depth + 1, False))
        return best
    else:
        best = float("inf")
        for i in moves:
            b2 = list(b)
            b2[i] = "x"
            best = min(best, minimax(b2, depth + 1, True))
        return best

