from .game import Board
from . import ai
from . import storage
try:
    import tkinter as _tk
    from tkinter import filedialog as _filedialog
    _TK_AVAILABLE = True
except Exception:
    _TK_AVAILABLE = False

import pygame
from typing import Optional, List, Tuple


def run_ui(board_size: int = 15):
    try:
        pygame.init()
    except Exception:
        print("Pygame initialization failed. Ensure pygame is installed.")
        return

    CELL = 40
    MARGIN = 30
    size = board_size
    width = MARGIN * 2 + CELL * (size - 1) + 100
    height = MARGIN * 2 + CELL * (size - 1) + 100
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Gomoku')
    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    board = Board(size=size)
    current_player = 1
    running = True
    game_over = False
    winner = None
    winning_line = []
    vs_ai = False
    ai_player = 2
    ai_depth = 3

    def coord_to_pixel(x: int, y: int) -> Tuple[int, int]:
        px = MARGIN + x * CELL
        py = MARGIN + y * CELL
        return px, py

    def pixel_to_coord(px: int, py: int) -> Optional[Tuple[int, int]]:
        rx = (px - MARGIN) / CELL
        ry = (py - MARGIN) / CELL
        ix = int(round(rx))
        iy = int(round(ry))
        if 0 <= ix < size and 0 <= iy < size:
            dx = abs(rx - ix) * CELL
            dy = abs(ry - iy) * CELL
            # accept if click is within reasonable radius
            if (dx * dx + dy * dy) ** 0.5 <= CELL * 0.6:
                return ix, iy
        return None

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key == pygame.K_u:
                    # undo
                    if vs_ai:
                        # if last move was AI, undo AI+human as a pair
                        if board.history:
                            last = board.history[-1]
                            if last[2] == ai_player:
                                board.undo()
                                if board.history:
                                    board.undo()
                                game_over = False
                                winner = None
                                winning_line = []
                                current_player = 3 - ai_player
                            else:
                                # last was human, undo single
                                board.undo()
                                game_over = False
                                winner = None
                                winning_line = []
                                current_player = 3 - ai_player
                    else:
                        undone = board.undo()
                        if undone:
                            game_over = False
                            winner = None
                            winning_line = []
                            current_player = 3 - current_player
                elif e.key == pygame.K_r:
                    # redo
                    if vs_ai:
                        # attempt to redo human+AI pair when possible
                        first = board.redo()
                        second = None
                        if first:
                            second = board.redo()
                        if second:
                            current_player = 3 - ai_player
                        elif first:
                            # only one move redone
                            # set to other player
                            current_player = 3 - first[2]
                    else:
                        redone = board.redo()
                        if redone:
                            current_player = 3 - current_player
                elif e.key == pygame.K_n:
                    # new game
                    board = Board(size=size)
                    current_player = 1
                    game_over = False
                    winner = None
                    winning_line = []
                elif e.key == pygame.K_a:
                    # toggle AI mode
                    vs_ai = not vs_ai
                elif e.key == pygame.K_p:
                    # switch which player the AI controls (1 or 2)
                    ai_player = 1 if ai_player == 2 else 2
                elif e.key == pygame.K_s:
                    # save game (open save dialog if tkinter available)
                    try:
                        if _TK_AVAILABLE:
                            root = _tk.Tk()
                            root.withdraw()
                            path = _filedialog.asksaveasfilename(title='Save game', defaultextension='.json', filetypes=[('JSON','*.json')])
                            root.destroy()
                        else:
                            path = 'savegame.json'
                        if path:
                            state = {
                                'grid': board.grid,
                                'history': board.history,
                                'current_player': current_player,
                                'vs_ai': vs_ai,
                                'ai_player': ai_player,
                                'ai_depth': ai_depth,
                                'game_over': game_over,
                            }
                            storage.save_state(path, state)
                            print('Game saved to', path)
                    except Exception as ex:
                        print('Failed to save game:', ex)
                elif e.key == pygame.K_l:
                    # load game (open file dialog if tkinter available)
                    try:
                        if _TK_AVAILABLE:
                            root = _tk.Tk()
                            root.withdraw()
                            path = _filedialog.askopenfilename(title='Load game', filetypes=[('JSON','*.json')])
                            root.destroy()
                        else:
                            path = 'savegame.json'
                        if path:
                            data = storage.load_state(path)
                            board.grid = [list(row) for row in data.get('grid', board.grid)]
                            # restore history as list of tuples
                            board.history = [tuple(h) for h in data.get('history', [])]
                            board._redo_stack = []
                            current_player = data.get('current_player', current_player)
                            vs_ai = data.get('vs_ai', vs_ai)
                            ai_player = data.get('ai_player', ai_player)
                            ai_depth = data.get('ai_depth', ai_depth)
                            game_over = data.get('game_over', False)
                            winner = None
                            winning_line = []
                            # recompute winner if possible
                            if board.history:
                                last = board.history[-1]
                                w, line = board.check_win(last)
                                if w is not None:
                                    game_over = True
                                    winner = w
                                    winning_line = line
                            print('Game loaded from', path)
                    except Exception as ex:
                        print('Failed to load game:', ex)
                elif e.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    # decrease AI depth
                    ai_depth = max(1, ai_depth - 1)
                elif e.key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                    # increase AI depth (accept '=' as '+')
                    ai_depth = min(8, ai_depth + 1)
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not game_over and not (vs_ai and current_player == ai_player):
                pos = pixel_to_coord(*e.pos)
                if pos:
                    x, y = pos
                    placed = board.place_move(x, y, current_player)
                    if placed:
                        w, line = board.check_win((x, y, current_player))
                        if w is not None:
                            game_over = True
                            winner = w
                            winning_line = line
                        else:
                            current_player = 3 - current_player

        # AI move handling
        if vs_ai and not game_over and current_player == ai_player:
            try:
                import gomoku.ai as ai_mod
                mv = ai_mod.choose_move_minimax(board, ai_player, depth=ai_depth)
            except Exception:
                mv = None
            if mv:
                x, y = mv
                placed = board.place_move(x, y, current_player)
                if placed:
                    w, line = board.check_win((x, y, current_player))
                    if w is not None:
                        game_over = True
                        winner = w
                        winning_line = line
                    else:
                        current_player = 3 - current_player

        screen.fill((245, 222, 179))
        # draw grid
        for i in range(size):
            start = (MARGIN + i * CELL, MARGIN)
            end = (MARGIN + i * CELL, MARGIN + (size - 1) * CELL)
            pygame.draw.line(screen, (0, 0, 0), start, end, 2)
            start = (MARGIN, MARGIN + i * CELL)
            end = (MARGIN + (size - 1) * CELL, MARGIN + i * CELL)
            pygame.draw.line(screen, (0, 0, 0), start, end, 2)

        # draw stones
        for y in range(size):
            for x in range(size):
                v = board.grid[y][x]
                if v != 0:
                    px, py = coord_to_pixel(x, y)
                    color = (0, 0, 0) if v == 1 else (255, 255, 255)
                    pygame.draw.circle(screen, color, (px, py), CELL // 2 - 4)
                    pygame.draw.circle(screen, (0,0,0), (px, py), CELL // 2 - 4, 1)

        # highlight last move
        if board.history:
            lx, ly, lp = board.history[-1]
            px, py = coord_to_pixel(lx, ly)
            pygame.draw.circle(screen, (255, 0, 0), (px, py), 6)

        # highlight winning line
        if winning_line:
            for (wx, wy) in winning_line:
                px, py = coord_to_pixel(wx, wy)
                pygame.draw.circle(screen, (0, 255, 0), (px, py), CELL // 2 - 2, 4)

        # status text
        status = "Player {}'s turn".format(current_player)
        if game_over and winner:
            status = "Player {} wins! (N to restart)".format(winner)
        # AI status
        ai_status = "AI: On (depth {})".format(ai_depth) if vs_ai else "AI: Off"
        txt = font.render(status + '   ' + ai_status, True, (0, 0, 0))
        screen.blit(txt, (MARGIN, MARGIN + (size) * CELL + 10))

        help_txt = font.render("A:toggle AI  +/-:depth  U:undo  R:redo  N:new  ESC:quit", True, (0,0,0))
        screen.blit(help_txt, (MARGIN, MARGIN + (size) * CELL + 35))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

__all__ = ["run_ui"]

