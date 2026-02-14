from typing import Tuple, Optional, List
import random

# caches to speed repeated evaluations
EVAL_CACHE = {}

# optional Cython accelerated evaluator
try:
    from .ai_cy import evaluate_board as _cy_evaluate_board
    CY_EVAL_AVAILABLE = True
except Exception:
    _cy_evaluate_board = None
    CY_EVAL_AVAILABLE = False

# optional numba JIT acceleration
try:
    import numpy as np
    from .ai_numba import evaluate_board_numba
    NUMBA_EVAL_AVAILABLE = True
except Exception:
    evaluate_board_numba = None
    NUMBA_EVAL_AVAILABLE = False


def _grid_bytes(board) -> bytes:
    size = board.size
    ba = bytearray(size * size)
    for y in range(size):
        row = board.grid[y]
        off = y * size
        for x in range(size):
            ba[off + x] = int(row[x])
    return bytes(ba)


def choose_move_random(board) -> Optional[Tuple[int, int]]:
    empties = [(x, y) for y in range(board.size) for x in range(board.size) if board.grid[y][x] == 0]
    if not empties:
        return None
    return random.choice(empties)


def _neighbors(board, dist: int = 2, depth: int = 2) -> List[Tuple[int, int]]:
    pts = {}
    size = board.size
    for y in range(size):
        for x in range(size):
            if board.grid[y][x] != 0:
                for dy in range(-dist, dist + 1):
                    for dx in range(-dist, dist + 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < size and 0 <= ny < size and board.grid[ny][nx] == 0:
                            pts[(nx, ny)] = pts.get((nx, ny), 0) + 1
    if not pts:
        center = board.size // 2
        return [(center, center)]
    center = board.size // 2
    items = sorted(pts.items(), key=lambda kv: (-kv[1], abs(kv[0][0] - center) + abs(kv[0][1] - center)))
    if depth <= 2:
        max_candidates = 30
    elif depth == 3:
        max_candidates = 18
    elif depth == 4:
        max_candidates = 10
    else:
        max_candidates = 6
    return [p for p, _ in items[:max_candidates]]


def _terminal_score(board, player: int) -> Optional[int]:
    if board.history:
        last = board.history[-1]
        winner, _ = board.check_win(last)
        if winner == player:
            return 10000
        elif winner is not None:
            return -10000
    return None


def _py_evaluate_board(board, player: int) -> int:
    # faster byte-based cache key
    grid_key = _grid_bytes(board)
    cache_key = (grid_key, player)
    if cache_key in EVAL_CACHE:
        return EVAL_CACHE[cache_key]

    size = board.size
    grid = board.grid

    def iter_lines():
        # rows
        for y in range(size):
            yield grid[y]
        # cols
        for x in range(size):
            col = [grid[y][x] for y in range(size)]
            yield col
        # main diagonals
        for k in range(-size + 1, size):
            diag = []
            for y in range(size):
                x = y - k
                if 0 <= x < size:
                    diag.append(grid[y][x])
            if len(diag) >= 1:
                yield diag
        # anti-diagonals
        for k in range(0, 2 * size - 1):
            adiag = []
            for y in range(size):
                x = k - y
                if 0 <= x < size:
                    adiag.append(grid[y][x])
            if len(adiag) >= 1:
                yield adiag

    def score_for_player(pval: int) -> int:
        score = 0
        p = pval
        opp = 3 - p
        for line in iter_lines():
            if len(line) < 2:
                continue
            padded = [0] + list(line) + [0]
            L = len(padded)
            # check five-in-row and smaller patterns using sliding windows
            # five-in-row
            for i in range(0, L - 4):
                slice5 = padded[i:i + 5]
                if all(v == p for v in slice5):
                    score += 100000
            # open4: 0 p p p p 0  (length 6 window)
            for i in range(0, L - 5):
                s6 = padded[i:i + 6]
                if s6[0] == 0 and all(v == p for v in s6[1:5]) and s6[5] == 0:
                    score += 10000
            # four (closed or not fully open)
            for i in range(0, L - 4):
                s5 = padded[i:i + 5]
                if sum(1 for v in s5 if v == p) == 4 and not all(v == p for v in s5):
                    score += 1000
            # open3: 0 p p p 0
            for i in range(0, L - 4):
                s5 = padded[i:i + 5]
                if s5[0] == 0 and s5[4] == 0 and sum(1 for v in s5[1:4] if v == p) == 3:
                    score += 500
            # three (not open)
            for i in range(0, L - 3):
                s4 = padded[i:i + 4]
                if sum(1 for v in s4 if v == p) == 3 and not (s4[0] == 0 and s4[-1] == 0):
                    score += 100
            # open2
            for i in range(0, L - 3):
                s4 = padded[i:i + 4]
                if s4[0] == 0 and s4[-1] == 0 and sum(1 for v in s4[1:3] if v == p) == 2:
                    score += 10
        return score

    my = score_for_player(player)
    their = score_for_player(3 - player)
    val = my - their
    EVAL_CACHE[cache_key] = val
    return val


def evaluate_board(board, player: int) -> int:
    # wrapper: use Cython or numba evaluator when available; fall back to Python
    grid_key = _grid_bytes(board)
    cache_key = (grid_key, player)
    if cache_key in EVAL_CACHE:
        return EVAL_CACHE[cache_key]
    if CY_EVAL_AVAILABLE and _cy_evaluate_board is not None:
        val = _cy_evaluate_board(board, player)
    elif NUMBA_EVAL_AVAILABLE and evaluate_board_numba is not None:
        # Convert grid to numpy array for numba evaluation
        import numpy as np
        grid_array = np.array(board.grid, dtype=np.int32)
        val = evaluate_board_numba(grid_array, player)
    else:
        val = _py_evaluate_board(board, player)
    EVAL_CACHE[cache_key] = val
    return val


TT = {}

# killer moves and history heuristic
KILLERS = {}  # depth -> list of killer moves (mx,my)
HISTORY = {}  # (player,x,y) -> score


def minimax(board, depth: int, alpha: int, beta: int, maximizing: bool, player: int) -> Tuple[int, Optional[Tuple[int, int]]]:
    gb = _grid_bytes(board)
    key = (gb, depth, maximizing, player)
    if key in TT:
        return TT[key]
    term = _terminal_score(board, player)
    if term is not None:
        TT[key] = (term, None)
        return term, None
    if depth == 0:
        val = evaluate_board(board, player)
        TT[key] = (val, None)
        return val, None
    moves = _neighbors(board, depth=depth)
    if not moves:
        center = board.size // 2
        val = evaluate_board(board, player)
        TT[key] = (val, (center, center))
        return val, (center, center)
    # lightweight local scoring for move ordering (adjacency-based)
    def move_score_simple(b, x, y, p):
        s = 0
        size = b.size
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size:
                    if b.grid[ny][nx] == p:
                        s += 10
                    elif b.grid[ny][nx] == 0:
                        s += 1
        return s

    scored_moves = []
    killers_here = KILLERS.get(depth, [])
    for (mx, my) in moves:
        sc = move_score_simple(board, mx, my, player if maximizing else (3 - player))
        hist = HISTORY.get((player, mx, my), 0)
        killer_bonus = 200000 if (mx, my) in killers_here else 0
        total = sc + hist + killer_bonus
        scored_moves.append((total, (mx, my)))
    scored_moves.sort(key=lambda t: -t[0] if maximizing else t[0])
    ordered = [m for _, m in scored_moves]
    best_move = None
    if maximizing:
        max_eval = -9999999
        for (mx, my) in ordered:
            board.place_move(mx, my, player)
            val, _ = minimax(board, depth - 1, alpha, beta, False, player)
            board.undo()
            if val > max_eval:
                max_eval = val
                best_move = (mx, my)
            alpha = max(alpha, val)
            if beta <= alpha:
                # record killer move and history increment for this move
                kd = depth - 1
                KILLERS.setdefault(kd, [])
                if (mx, my) not in KILLERS[kd]:
                    KILLERS[kd].insert(0, (mx, my))
                    KILLERS[kd] = KILLERS[kd][:2]
                HISTORY[(player, mx, my)] = HISTORY.get((player, mx, my), 0) + (1 << depth)
                break
        TT[key] = (max_eval, best_move)
        return max_eval, best_move
    else:
        min_eval = 9999999
        for (mx, my) in ordered:
            board.place_move(mx, my, 3 - player)
            val, _ = minimax(board, depth - 1, alpha, beta, True, player)
            board.undo()
            if val < min_eval:
                min_eval = val
                best_move = (mx, my)
            beta = min(beta, val)
            if beta <= alpha:
                # record killer move and history increment for this move (opponent perspective)
                kd = depth - 1
                KILLERS.setdefault(kd, [])
                if (mx, my) not in KILLERS[kd]:
                    KILLERS[kd].insert(0, (mx, my))
                    KILLERS[kd] = KILLERS[kd][:2]
                HISTORY[(3 - player, mx, my)] = HISTORY.get((3 - player, mx, my), 0) + (1 << depth)
                break
        TT[key] = (min_eval, best_move)
        return min_eval, best_move


def choose_move_minimax(board, player: int, depth: int = 2) -> Optional[Tuple[int, int]]:
    term = _terminal_score(board, player)
    if term is not None:
        return None
    _, move = minimax(board, depth, -9999999, 9999999, True, player)
    if move is None:
        return choose_move_random(board)
    return move

