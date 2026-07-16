"""
Agent 2 — Rule-based agent.  OWNER: Teammate 2.

Stub only — Ayuub scaffolded this so the repo layout is complete. Delete this
note and implement select_move(). See INTERFACE.md, "Look-ahead pattern A".

Suggested rules (in priority order):
    1. If you can win this move, take it (check_winning_move).
    2. If the opponent can win next move, block it.
    3. Otherwise prefer the centre column (see the tie-breaking snippet).
"""

from base_agent import BaseAgent
from engine import ConnectFour


class RuleAgent(BaseAgent):
    def __init__(self, player=None, name="Rule"):
        super().__init__(player=player, name=name)

    def select_move(self, game: ConnectFour) -> int:
        raise NotImplementedError("Teammate 2: implement the rule-based agent.")
