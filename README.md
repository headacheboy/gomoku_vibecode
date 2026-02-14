# Gomoku (五子棋) — Pygame Prototype

This repository contains a Pygame-based Gomoku prototype.

Quick start

```bash
pip install -r requirements.txt
python -m gomoku.main
```

Run unit tests:

```bash
python -m unittest discover -v
```

Controls (in-game):

- Left-click: place stone
- A: toggle AI on/off
- P: toggle which player AI controls (1 or 2)
- + / = or keypad +: increase AI depth
- - or keypad -: decrease AI depth
- U: undo (in AI mode undoes a human+AI pair)
- R: redo (in AI mode redoes a human+AI pair)
- S: save current game to `savegame.json`
- L: load game from `savegame.json`
- N: new game
- ESC: quit

Notes:
- Saved games are written to `savegame.json` in the repository root.
- The AI uses a minimax search with alpha-beta pruning and a simple transposition table; increase depth for stronger play but expect longer thinking time.
