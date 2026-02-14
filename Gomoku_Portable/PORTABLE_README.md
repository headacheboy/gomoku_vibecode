# Gomoku Game - Portable Version

## Quick Start

### Windows
1. Double-click START_GAME.bat
2. The game window should open automatically
3. Dependencies will be installed automatically on first run

### Linux/macOS
1. Make the script executable: chmod +x start_game.sh
2. Run: ./start_game.sh
3. Or run directly: python gomoku_launcher.py

## Requirements
- Python 3.5+ must be installed
- Internet connection (for dependency installation on first run)

## Game Controls
- **Left Click**: Place stone
- **A**: Toggle AI on/off
- **P**: Switch AI player (1=Black, 2=White)
- **+/-**: Increase/decrease AI search depth
- **U/R**: Undo/Redo
- **N**: New game
- **S**: Save game
- **L**: Load game
- **ESC**: Quit

## Optimizations
- Numba JIT acceleration enabled for AI evaluator
- Fast byte-grid caching
- Minimax with alpha-beta pruning + killer moves + history heuristic

Enjoy playing!
