"""
Agent 3 — Minimax / alpha-beta agent.  OWNER: Teammate 3.
 
Depth-limited negamax with alpha-beta pruning. Searches in place with
apply_move()/undo_move() (no copies inside the recursion — see INTERFACE.md,
"Look-ahead pattern B"), and uses check_winning_move() to prune outright wins
without recursing a full ply deeper.
 
Evaluation (used at the depth cutoff and at terminal nodes reached mid-search):
a windowed heuristic in the same spirit as the rule-based agent — every
length-4 window on the board is scored based on how many of the mover's discs
vs the opponent's discs it contains, plus a bonus for centre-column control.
Terminal wins/losses are scored as a large constant, nudged by remaining depth
so the search prefers faster wins and slower losses.
"""

from base_agent import BaseAgent
from engine import ConnectFour, ROWS, COLS, CONNECT

CENTER_COL = COLS // 2
ORDER = [3, 2, 4, 1, 5, 0, 6]

WIN_SCORE = 1_000_000

def _all_windows():
    """Every length-CONNECT line on the board, as lists of (row, col)."""
    windows = []
    # Horizontal
    for r in range(ROWS):                              
        for c in range(COLS - CONNECT + 1):
            windows.append([(r, c + i) for i in range(CONNECT)])
    # Vertical
    for c in range(COLS):                             
        for r in range(ROWS - CONNECT + 1):
            windows.append([(r + i, c) for i in range(CONNECT)])
    # Diagonal Up-right
    for r in range(ROWS - CONNECT + 1):                
        for c in range(COLS - CONNECT + 1):
            windows.append([(r + i, c + i) for i in range(CONNECT)])
    # Diagonal Down-right
    for r in range(CONNECT - 1, ROWS):
        for c in range(COLS - CONNECT + 1):
            windows.append([(r - i, c + i) for i in range(CONNECT)])
    return windows

_WINDOWS = _all_windows()

class MinimaxAgent(BaseAgent):
    def __init__(self, player=None, depth=4, name="Minimax"):
        super().__init__(player=player, name=name)
        self.depth = depth

    # 
    def select_move(self, game: ConnectFour) -> int:
        me = game.current_player
        opp = 3 - me
        moves = [c for c in ORDER if c in game.legal_moves()]
 
        # Take an immediate win without spending a search ply on it.
        for c in moves:
            if game.check_winning_move(c, me):
                return c
 
        best_score = -float("inf")
        best_move = moves[0]
        alpha, beta = -float("inf"), float("inf")
 
        for c in moves:
            game.apply_move(c)
            score = -self._negamax(game, self.depth - 1, -beta, -alpha, opp)
            game.undo_move()
 
            if score > best_score:
                best_score = score
                best_move = c
            alpha = max(alpha, score)
 
        return best_move
    
    # 
    def _negamax(self, game: ConnectFour, depth, alpha, beta, player):
        """
        Score the position from `player`'s point of view (the player about to
        move at this node). Positive is good for `player`.
        """
        opp = 3 - player
        moves = game.legal_moves()
 
        winner = game.winner()
        if winner is not None:
            if winner == player:
                return WIN_SCORE + depth       # faster wins score higher
            else:
                return -(WIN_SCORE + depth)    # slower losses score higher
        # draw
        if not moves:
            return 0
 
        if depth == 0:
            return self._evaluate(game.board, player)
 
        ordered = [c for c in ORDER if c in moves]
 
        # Prune: if `player` can win immediately, that's the best possible
        # outcome from this node — no need to search deeper.
        for c in ordered:
            if game.check_winning_move(c, player):
                return WIN_SCORE + depth
 
        value = -float("inf")
        for c in ordered:
            game.apply_move(c)
            score = -self._negamax(game, depth - 1, -beta, -alpha, opp)
            game.undo_move()
 
            if score > value:
                value = score
            if value > alpha:
                alpha = value
            # alpha-beta cutoff
            if alpha >= beta:
                break           
        return value
    
    # 
    def _evaluate(self, board, player):
        """Windowed heuristic from `player`'s perspective (higher = better)."""
        opp = 3 - player
        score = 0
 
        for cells in _WINDOWS:
            mine = theirs = empty = 0
            for (r, c) in cells:
                v = board[r][c]
                if v == player:
                    mine += 1
                elif v == opp:
                    theirs += 1
                else:
                    empty += 1
            # mixed window: nobody can use it
            if mine and theirs:
                continue                      
            if mine == 3 and empty == 1:
                score += 50
            elif mine == 2 and empty == 2:
                score += 10
            elif mine == 1 and empty == 3:
                score += 1
            elif theirs == 3 and empty == 1:
                score -= 45
            elif theirs == 2 and empty == 2:
                score -= 8
 
        # Centre-column control.
        score += 3 * sum(1 for r in range(ROWS) if board[r][CENTER_COL] == player)
        return score
