serial = 7857


def power_level(x, y, serial):
    """
    >>> power_level(3, 5, 8)
    4
    >>> power_level(122, 79, 57)
    -5
    >>> power_level(217, 196, 39)
    0
    """
    rack_id = x + 10
    return (rack_id * y + serial) * rack_id // 100 % 10 - 5


def level_board(m, n, serial):
    """
    m: int horizontal length
    n: int vertical length

    >>> b = level_board(300, 300, 18)
    >>> b[44][32] == b[44][33] == b[44][34] == 4
    True
    >>> b[45][32] == 3
    True
    >>> b[46][32] == 1 and b[46][33] == 2
    True
    """
    board = []
    for j in range(n):
        board.append([])
        for i in range(m):
            board[j].append(power_level(i+1, j+1, serial))
    return board


def max_level_3x3(board):
    """
    >>> max_level_3x3(level_board(300, 300, 18))
    (29, (33, 45))
    >>> max_level_3x3(level_board(300, 300, 42))
    (30, (21, 61))
    """
    def level_sum_3x3(i, j):
        result = 0
        for ii in range(i, i+3):
            for jj in range(j, j+3):
                result += board[ii][jj]
        return result

    m, n = len(board), len(board[0])
    max_level_sum = float('-inf')
    top_left = None
    for i in range(m-2):
        for j in range(n-2):
            level = level_sum_3x3(i, j)
            if level > max_level_sum:
                max_level_sum = level
                top_left = (j+1, i+1)

    return max_level_sum, top_left


def accum_board(board):
    """
    accum_board[m][n] = sum(board[0...m][0..n])
    +-----------+--------------------+
    |     #1    |         #2         |
    +----------[a]------------------[b]
    |           |                    |
    |     #3    |         #4         |
    +----------[c]------------------[d]

    #4 = accum_board[d] + accum_board[a] - accum_board[b] - accum_board[c]

    >>> accum_board([[1,2], [3,4]])
    [[1, 3], [4, 10]]
    """
    acc_board = []
    m, n = len(board), len(board[0])
    for i in range(m):
        acc_board.append([])
        acc_row = 0
        for j in range(n):
            acc_row += board[i][j]
            if i > 0:
                acc_board[i].append(acc_row + acc_board[i-1][j])
            else:
                acc_board[i].append(acc_row)
    return acc_board


def max_level(board):
    """
    >>> max_level(level_board(300, 300, 18))
    (90, 269, 16)
    >>> max_level(level_board(300, 300, 42))
    (232, 251, 12)
    """
    acc_board = accum_board(board)
    for row in acc_board:
        row.append(0)
    acc_board.append([0]*len(acc_board[0]))
    m, n = len(board), len(board[0])
    max_level_sum = float('-inf')
    top_left = None
    for i in range(m):
        for j in range(n):
            for k in range(min(m-i, n-j)):
                level = (acc_board[i+k][j+k] +
                         acc_board[i-1][j-1] -
                         acc_board[i-1][j+k] -
                         acc_board[i+k][j-1])
                if level > max_level_sum:
                    max_level_sum = level
                    top_left = (j+1, i+1, k+1)
    return top_left


print(max_level_3x3(level_board(300, 300, 7857)))
print(max_level(level_board(300, 300, 7857)))
