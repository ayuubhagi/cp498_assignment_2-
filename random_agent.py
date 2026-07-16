"""
Agent 1 — Random baseline (Assignment 2, Agent 1, 0.5 marks).

Picks a uniformly random legal column. Seeded so a run can be reproduced
exactly, which matters for the experiment write-up.
"""

import random

from base_agent import BaseAgent
from engine import ConnectFour


class RandomAgent(BaseAgent):
    def __init__(self, player=None, seed=None, name="Random"):
        super().__init__(player=player, name=name)
        self._rng = random.Random(seed)

    def select_move(self, game: ConnectFour) -> int:
        return self._rng.choice(game.legal_moves())
