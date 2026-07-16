"""
Connect Four game engine — the shared rules layer for CP468 Assignment 2.

This is the piece every agent and the experiment harness build on. The public
interface is FROZEN (see INTERFACE.md). Do not change a method signature without
telling the owner first — a change here breaks all four agents at once.

Board convention:
    - ROWS x COLS grid, row 0 is the BOTTOM row (gravity pulls discs down).
    - board[row][col] holds 0 (empty), 1 (player one) or 2 (player two).
    - heights[col] is the number of discs already in that column, i.e. the row
      index the next disc will land on.

Two ways to look ahead:
    - copy() + apply_move(): simple, safe, good for the random/rule agents.
    - apply_move() + undo_move(): fast in-place, good for deep minimax search.
      check_winning_move() is a non-mutating shortcut for "would this move win?".
"""

ROWS = 6
COLS = 7
CONNECT = 4  # discs in a row needed to win


class ConnectFour:
    def __init__(self):
        # board[row][col]; row 0 is the bottom row.
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.heights = [0] * COLS      # discs per column
        self.current_player = 1        # player to move (1 or 2)
        self.move_count = 0
        self._history = []             # stack of columns played, for undo_move()

    # ------------------------------------------------------------------ #
    #  Move generation / making moves                                    #
    # ------------------------------------------------------------------ #
    def legal_moves(self):
        """Return the list of columns that are not full."""
        return [c for c in range(COLS) if self.heights[c] < ROWS]

    def is_legal(self, col):
        return 0 <= col < COLS and self.heights[col] < ROWS

    def apply_move(self, col):
        """
        Drop the current player's disc into `col` and advance the turn.
        Assumes the move is legal (call legal_moves() / is_legal() first).
        """
        row = self.heights[col]
        self.board[row][col] = self.current_player
        self.heights[col] += 1
        self.move_count += 1
        self._history.append(col)
        self.current_player = 3 - self.current_player  # 1 <-> 2

    def undo_move(self):
        """Reverse the most recent apply_move(). Restores board and turn."""
        col = self._history.pop()
        self.heights[col] -= 1
        row = self.heights[col]
        self.board[row][col] = 0
        self.move_count -= 1
        self.current_player = 3 - self.current_player

    # ------------------------------------------------------------------ #
    #  Win / draw / terminal detection                                   #
    # ------------------------------------------------------------------ #
    def _line_len(self, row, col, dr, dc, player):
        """
        Count consecutive `player` discs starting from (row, col) and stepping
        in (dr, dc), NOT counting the starting cell itself.
        """
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == player:
            count += 1
            r += dr
            c += dc
        return count

    def _wins_at(self, row, col, player):
        """True if `player` occupying (row, col) completes a line of CONNECT."""
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            total = 1 + self._line_len(row, col, dr, dc, player) \
                      + self._line_len(row, col, -dr, -dc, player)
            if total >= CONNECT:
                return True
        return False

    def check_winning_move(self, col, player):
        """
        Non-mutating: would dropping `player`'s disc into `col` win the game?
        Returns False if the column is full. The board is left unchanged, so
        this is safe to call in a search loop without copying.
        """
        if not self.is_legal(col):
            return False
        return self._wins_at(self.heights[col], col, player)

    def winner(self):
        """
        Return 1 or 2 if that player has four in a row anywhere, else None.
        Scans the whole board, so it works even for boards built by hand.
        """
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if p == 0:
                    continue
                # Look right, up, and both diagonals from this cell.
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    if 1 + self._line_len(r, c, dr, dc, p) >= CONNECT:
                        return p
        return None

    def is_draw(self):
        """Board full with no winner."""
        return not self.legal_moves() and self.winner() is None

    def is_terminal(self):
        """Game over: someone has won or the board is full."""
        return self.winner() is not None or not self.legal_moves()

    # ------------------------------------------------------------------ #
    #  Utilities                                                         #
    # ------------------------------------------------------------------ #
    def copy(self):
        """Deep copy of the game state (independent board/heights/history)."""
        clone = ConnectFour()
        clone.board = [row[:] for row in self.board]
        clone.heights = self.heights[:]
        clone.current_player = self.current_player
        clone.move_count = self.move_count
        clone._history = self._history[:]
        return clone

    def __str__(self):
        symbols = {0: ".", 1: "X", 2: "O"}
        rows = []
        for r in range(ROWS - 1, -1, -1):  # print top row first
            rows.append(" ".join(symbols[self.board[r][c]] for c in range(COLS)))
        rows.append(" ".join(str(c) for c in range(COLS)))  # column labels
        return "\n".join(rows)
