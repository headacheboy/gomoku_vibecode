from typing import List, Optional, Tuple

class Board:
    def __init__(self, size: int = 15):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.history = []  # list of (x,y,player)
        self._redo_stack = []

    def is_valid_move(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size and self.grid[y][x] == 0

    def place_move(self, x: int, y: int, player: int) -> bool:
        if not self.is_valid_move(x, y):
            return False
        self.grid[y][x] = player
        self.history.append((x, y, player))
        self._redo_stack.clear()
        return True

    def undo(self) -> Optional[Tuple[int,int,int]]:
        if not self.history:
            return None
        x,y,player = self.history.pop()
        self.grid[y][x] = 0
        self._redo_stack.append((x,y,player))
        return (x,y,player)

    def redo(self) -> Optional[Tuple[int,int,int]]:
        if not self._redo_stack:
            return None
        x,y,player = self._redo_stack.pop()
        self.grid[y][x] = player
        self.history.append((x,y,player))
        return (x,y,player)

    def _count_dir(self, x:int, y:int, dx:int, dy:int, player:int) -> int:
        cnt = 0
        cx, cy = x+dx, y+dy
        while 0 <= cx < self.size and 0 <= cy < self.size and self.grid[cy][cx] == player:
            cnt += 1
            cx += dx
            cy += dy
        return cnt

    def check_win(self, last_move: Optional[Tuple[int,int,int]] = None) -> Tuple[Optional[int], List[Tuple[int,int]]]:
        """Return (winner_player or None, winning_line_coords list). If last_move provided, check only around it."""
        candidates = []
        if last_move is None:
            if not self.history:
                return None, []
            x,y,player = self.history[-1]
        else:
            x,y,player = last_move
        directions = [(1,0),(0,1),(1,1),(1,-1)]
        for dx,dy in directions:
            left = self._count_dir(x,y,-dx,-dy,player)
            right = self._count_dir(x,y,dx,dy,player)
            total = left + 1 + right
            if total >= 5:
                # build winning coords
                coords = []
                # go to the farthest negative
                sx = x - dx*left
                sy = y - dy*left
                for i in range(total):
                    coords.append((sx + i*dx, sy + i*dy))
                return player, coords
        return None, []

    def __str__(self):
        lines = []
        for row in self.grid:
            lines.append(''.join(['.' if v==0 else ('X' if v==1 else 'O') for v in row]))
        return '\n'.join(lines)
