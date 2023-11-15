board = [
    [2, 2, 2, 2],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]
for ind_lien, line in enumerate(board):
    for ind_cell, cell in enumerate(line[:-1]):
        right_cell = board[ind_lien][ind_cell + 1]
        if cell == right_cell:
            board[ind_lien][ind_cell] = cell + right_cell
            board[ind_lien][ind_cell + 1] = 0
            continue

[print(*line) for line in board]
