"""
Optional numba JIT acceleration for hot AI routines.
Numba compiles Python functions to machine code at runtime,
providing near-C performance without requiring a C compiler.
"""
import numba
import numpy as np


@numba.jit(nopython=True)
def score_line_numba(line_array, p):
    """
    Numba-accelerated line scoring.
    line_array: 1D numpy array of ints (0, 1, or 2)
    p: player value (1 or 2)
    Returns score for this player on this line.
    """
    L = len(line_array)
    if L == 0:
        return 0
    
    # Pad with zeros
    padded = np.zeros(L + 2, dtype=np.int32)
    padded[1:L+1] = line_array
    
    s = 0
    padded_len = L + 2
    
    # five-in-row
    for i in range(0, padded_len - 4):
        if (padded[i] == p and padded[i+1] == p and padded[i+2] == p 
            and padded[i+3] == p and padded[i+4] == p):
            s += 100000
    
    # open4: 0 p p p p 0
    for i in range(0, padded_len - 5):
        if (padded[i] == 0 and padded[i+5] == 0 
            and padded[i+1] == p and padded[i+2] == p 
            and padded[i+3] == p and padded[i+4] == p):
            s += 10000
    
    # open2: 0 p p 0
    for i in range(0, padded_len - 3):
        if (padded[i] == 0 and padded[i+3] == 0 
            and padded[i+1] == p and padded[i+2] == p):
            s += 10
    
    return s


@numba.jit(nopython=True)
def evaluate_board_numba(grid_array, player):
    """
    Numba-accelerated board evaluation.
    grid_array: 2D numpy array of ints (0, 1, or 2)
    player: 1 or 2
    Returns evaluation score.
    """
    size = grid_array.shape[0]
    p = player
    opp = 3 - p
    val = 0
    
    # Score rows for player
    for y in range(size):
        val += score_line_numba(grid_array[y, :], p)
    
    # Score cols for player
    for x in range(size):
        val += score_line_numba(grid_array[:, x], p)
    
    # Score diagonals for player
    for k in range(-size + 1, size):
        diag = np.zeros(size, dtype=np.int32)
        diag_len = 0
        for y in range(size):
            x = y - k
            if 0 <= x < size:
                diag[diag_len] = grid_array[y, x]
                diag_len += 1
        if diag_len > 0:
            val += score_line_numba(diag[:diag_len], p)
    
    # Score anti-diagonals for player
    for k in range(0, 2 * size - 1):
        diag = np.zeros(size, dtype=np.int32)
        diag_len = 0
        for y in range(size):
            x = k - y
            if 0 <= x < size:
                diag[diag_len] = grid_array[y, x]
                diag_len += 1
        if diag_len > 0:
            val += score_line_numba(diag[:diag_len], p)
    
    # Score opponent (subtract from total)
    opp_score = 0
    
    # Score rows for opponent
    for y in range(size):
        opp_score += score_line_numba(grid_array[y, :], opp)
    
    # Score cols for opponent
    for x in range(size):
        opp_score += score_line_numba(grid_array[:, x], opp)
    
    # Score diagonals for opponent
    for k in range(-size + 1, size):
        diag = np.zeros(size, dtype=np.int32)
        diag_len = 0
        for y in range(size):
            x = y - k
            if 0 <= x < size:
                diag[diag_len] = grid_array[y, x]
                diag_len += 1
        if diag_len > 0:
            opp_score += score_line_numba(diag[:diag_len], opp)
    
    # Score anti-diagonals for opponent
    for k in range(0, 2 * size - 1):
        diag = np.zeros(size, dtype=np.int32)
        diag_len = 0
        for y in range(size):
            x = k - y
            if 0 <= x < size:
                diag[diag_len] = grid_array[y, x]
                diag_len += 1
        if diag_len > 0:
            opp_score += score_line_numba(diag[:diag_len], opp)
    
    return val - opp_score
