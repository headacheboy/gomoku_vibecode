from gomoku.game import Board
from gomoku import ai

def run_demo(max_moves=200, depth=2):
    board = Board(size=15)
    current = 1
    move_count = 0
    print('Starting AI vs AI demo (depth={})'.format(depth))
    while move_count < max_moves:
        mv = ai.choose_move_minimax(board, current, depth=depth)
        if mv is None:
            print('No moves left, draw')
            break
        x,y = mv
        board.place_move(x,y,current)
        move_count += 1
        print('Move {}: Player {} -> ({},{})'.format(move_count, current, x, y))
        print(board)
        winner, line = board.check_win((x,y,current))
        if winner:
            print('Winner:', winner)
            print('Winning line:', line)
            break
        current = 3 - current
    else:
        print('Reached max moves, stopping.')

if __name__ == '__main__':
    run_demo(depth=2)
