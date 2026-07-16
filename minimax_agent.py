"""
Agent 3 — Minimax / alpha-beta agent.  OWNER: Teammate 3.

Stub only — Ayuub scaffolded this so the repo layout is complete. Delete this
note and implement select_move(). See INTERFACE.md, "Look-ahead pattern B".

Head start baked into the engine for you:
    - apply_move() / undo_move(): search in place, no copies in the recursion.
    - check_winning_move(col, player): prune moves that win outright.
Write an evaluate(game, player) heuristic and a depth-limited negamax/alpha-beta.
"""

from base_agent import BaseAgent
from engine import ConnectFour


class MinimaxAgent(BaseAgent):
    def __init__(self, player=None, depth=4, name="Minimax"):
        super().__init__(player=player, name=name)
        self.depth = depth

    def select_move(self, game: ConnectFour) -> int:
        raise NotImplementedError("Teammate 3: implement minimax / alpha-beta.")
