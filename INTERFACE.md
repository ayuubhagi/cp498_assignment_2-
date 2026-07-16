# Engine Interface — build against this, don't read the whole engine

The engine is **frozen**. Teammates 2, 3, and 4: code against the methods below.
If you think you need to change a signature, ping the engine owner first — a change
here breaks all four agents at once.

## Getting a game going

```python
from engine import ConnectFour, ROWS, COLS   # ROWS = 6, COLS = 7

game = ConnectFour()      # empty board, player 1 to move
```

## State you can read

| Thing | What it is |
|---|---|
| `game.board[row][col]` | `0` empty, `1` player one, `2` player two. **Row 0 is the bottom.** |
| `game.heights[col]` | how many discs are in that column (the row the next disc lands on) |
| `game.current_player` | `1` or `2`, whose turn it is |
| `game.move_count` | total discs played |

## Methods

| Call | Returns / does |
|---|---|
| `game.legal_moves()` | list of columns that aren't full, e.g. `[0,1,2,3,4,5,6]` |
| `game.is_legal(col)` | `True/False` |
| `game.apply_move(col)` | drops current player's disc, flips the turn |
| `game.undo_move()` | reverses the last `apply_move` |
| `game.check_winning_move(col, player)` | **non-mutating** — would `player` win by playing `col`? |
| `game.winner()` | `1`, `2`, or `None` |
| `game.is_draw()` | board full, no winner |
| `game.is_terminal()` | someone won or board full |
| `game.copy()` | independent deep copy |

## Writing an agent

Subclass `BaseAgent` and implement the one required method. **Never mutate the
`game` you're handed** — copy it or use apply/undo.

```python
from base_agent import BaseAgent

class MyAgent(BaseAgent):
    def select_move(self, game):
        return game.legal_moves()[0]   # return a legal column
```

### Look-ahead pattern A — simple (rule-based agent)

Safe and readable. Copy, try the move, inspect.

```python
for col in game.legal_moves():
    if game.check_winning_move(col, self.player):
        return col                     # take an immediate win
```

### Look-ahead pattern B — fast (minimax agent)

No copies inside the recursion — apply, recurse, undo.

```python
def negamax(game, depth, player):
    if game.is_terminal() or depth == 0:
        return evaluate(game, player)
    best = -float("inf")
    for col in game.legal_moves():
        if game.check_winning_move(col, game.current_player):
            return WIN                 # prune: this move wins outright
        game.apply_move(col)
        best = max(best, -negamax(game, depth - 1, 3 - player))
        game.undo_move()
    return best
```

### Tie-breaking (use this so results are reproducible)

Prefer the centre column when scores are equal — it's the strongest opening in
Connect Four and keeps runs deterministic.

```python
ORDER = [3, 2, 4, 1, 5, 0, 6]          # centre-out
moves = [c for c in ORDER if c in game.legal_moves()]
```

## Running things

```bash
python3 test_engine.py            # 8 correctness tests, must stay green
python3 demo_random_vs_random.py  # one full game; template for the harness
```

**Rule for the repo:** `main` must always pass `python3 test_engine.py`.
Don't merge anything that breaks it.
