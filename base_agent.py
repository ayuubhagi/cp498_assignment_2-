"""
Base class every agent implements. The contract is a single method:

    select_move(game) -> int

It receives the current ConnectFour state and returns a legal column to play.
The agent must NOT mutate the game it is handed. If it wants to look ahead it
should use game.copy() or game.apply_move()/game.undo_move() (see INTERFACE.md).
"""

from engine import ConnectFour


class BaseAgent:
    def __init__(self, player=None, name=None):
        # player is 1 or 2; may be set by the harness before a match.
        self.player = player
        self.name = name or self.__class__.__name__

    def select_move(self, game: ConnectFour) -> int:
        """Return a legal column index for the current player. Override me."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement select_move(game)."
        )

    def __str__(self):
        return self.name
