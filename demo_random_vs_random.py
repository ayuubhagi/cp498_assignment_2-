"""
Plays one full Random vs Random game and prints the board each turn.

Doubles as a template for the experiment harness: swap in any two agents that
implement select_move(game) and the play_game() loop below still works.

Run: python3 demo_random_vs_random.py
"""

from engine import ConnectFour
from random_agent import RandomAgent


def play_game(agent1, agent2, verbose=True):
    """
    Play a single game. agent1 is player 1 (moves first), agent2 is player 2.
    Returns the winning player (1 or 2) or 0 for a draw.
    """
    game = ConnectFour()
    agents = {1: agent1, 2: agent2}

    while not game.is_terminal():
        mover = game.current_player
        col = agents[mover].select_move(game)
        game.apply_move(col)
        if verbose:
            print(f"\nPlayer {mover} ({agents[mover]}) -> column {col}")
            print(game)

    result = game.winner()
    return result if result is not None else 0


if __name__ == "__main__":
    p1 = RandomAgent(player=1, seed=1, name="Random-A")
    p2 = RandomAgent(player=2, seed=2, name="Random-B")

    result = play_game(p1, p2, verbose=True)

    print("\n" + "=" * 30)
    if result == 0:
        print("Result: draw")
    else:
        print(f"Result: player {result} wins")
