"""
Agent 2 — Rule-based agent (Assignment 2, Agent 1.5 marks).  OWNER: Khaled.

A prioritized, hand-written rule set. Rules are checked top to bottom; the first
one that applies decides the move. See INTERFACE.md, "Look-ahead pattern A".

Rules, in priority order
------------------------
  1. WIN     - if any move wins immediately, play it.
  2. BLOCK   - else, if the opponent can win on their next move, play in that
               column to block it.
  3/4. POSITIONAL - else, score every legal move with a windowed heuristic that
               rewards centre-column control (rule 3) and extending your own
               lines into 2- and 3-in-a-window threats (rule 4), and heavily
               penalises any move that would hand the opponent an immediate win
               on their next turn. Play the best-scoring move.

Tie-breaking (mandatory, per the assignment)
--------------------------------------------
Whenever several moves are ranked equally best under the applicable rule, one is
chosen UNIFORMLY AT RANDOM from a seedable RNG. The assignment requires this so
that agents don't replay one identical game and the experiment's win/draw rates
stay meaningful. (This deliberately differs from the deterministic centre-out
snippet in INTERFACE.md; centre preference is kept, but only as a scoring rule,
not as the tie-break.)
"""

import random

from base_agent import BaseAgent
from engine import ConnectFour, ROWS, COLS, CONNECT

CENTER_COL = COLS // 2                 # column 3 on a 7-wide board
_GIVES_OPPONENT_WIN = 100_000          # penalty: this move lets the opponent win next


def _all_windows():
    """Every length-CONNECT line on the board, as lists of (row, col)."""
    windows = []
    for r in range(ROWS):                              # horizontal
        for c in range(COLS - CONNECT + 1):
            windows.append([(r, c + i) for i in range(CONNECT)])
    for c in range(COLS):                              # vertical
        for r in range(ROWS - CONNECT + 1):
            windows.append([(r + i, c) for i in range(CONNECT)])
    for r in range(ROWS - CONNECT + 1):                # diagonal up-right
        for c in range(COLS - CONNECT + 1):
            windows.append([(r + i, c + i) for i in range(CONNECT)])
    for r in range(CONNECT - 1, ROWS):                 # diagonal down-right
        for c in range(COLS - CONNECT + 1):
            windows.append([(r - i, c + i) for i in range(CONNECT)])
    return windows


_WINDOWS = _all_windows()


class RuleAgent(BaseAgent):
    def __init__(self, player=None, seed=None, name="Rule"):
        super().__init__(player=player, name=name)
        # Private, seeded RNG -> reproducible random tie-breaking.
        self._rng = random.Random(seed)

    # ------------------------------------------------------------------ #
    def select_move(self, game: ConnectFour) -> int:
        me = game.current_player
        opp = 3 - me
        moves = game.legal_moves()

        # Rule 1: take an immediate win.
        wins = [c for c in moves if game.check_winning_move(c, me)]
        if wins:
            return self._rng.choice(wins)

        # Rule 2: block the opponent's immediate win.
        blocks = [c for c in moves if game.check_winning_move(c, opp)]
        if blocks:
            return self._rng.choice(blocks)

        # Rules 3 & 4: positional scoring, with a blunder guard.
        best_score = None
        best_moves = []
        for c in moves:
            sim = game.copy()          # never mutate the game we were handed
            sim.apply_move(c)          # plays `me`, advances turn to `opp`
            score = self._evaluate(sim.board, me)
            if any(sim.check_winning_move(cc, opp) for cc in sim.legal_moves()):
                score -= _GIVES_OPPONENT_WIN
            if best_score is None or score > best_score:
                best_score = score
                best_moves = [c]
            elif score == best_score:
                best_moves.append(c)

        return self._rng.choice(best_moves)

    # ------------------------------------------------------------------ #
    def _evaluate(self, board, me):
        """Windowed heuristic from `me`'s perspective (higher = better)."""
        opp = 3 - me
        score = 0

        for cells in _WINDOWS:
            mine = theirs = empty = 0
            for (r, c) in cells:
                v = board[r][c]
                if v == me:
                    mine += 1
                elif v == opp:
                    theirs += 1
                else:
                    empty += 1
            if mine and theirs:
                continue                       # mixed window: nobody can use it
            if mine == 4:
                score += 100
            elif mine == 3 and empty == 1:
                score += 5
            elif mine == 2 and empty == 2:
                score += 2
            elif theirs == 3 and empty == 1:
                score -= 4                     # discourage leaving opponent threats

        # Rule 3: centre-column control.
        score += 3 * sum(1 for r in range(ROWS) if board[r][CENTER_COL] == me)
        return score
