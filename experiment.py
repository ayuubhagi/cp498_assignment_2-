"""
Experiment harness — runs the matchups and reports results.  OWNER: Teammate 4.

Stub only — Ayuub scaffolded this so the repo layout is complete. Delete this
note and build it out. play_game() in demo_random_vs_random.py is a working
template you can lift directly.

What this needs to do:
    - Run N games per matchup, alternating who goes first (fairness).
    - Use fixed seeds so results are reproducible.
    - Tally wins/losses/draws and print (or save to results/) a summary table.
"""

from demo_random_vs_random import play_game
from random_agent import RandomAgent
# from rule_agent import RuleAgent          # uncomment as agents land
# from minimax_agent import MinimaxAgent


def run_matchup(make_a, make_b, games=100):
    """Play `games` games, alternating first player. Returns (a_wins, b_wins, draws)."""
    raise NotImplementedError("Teammate 4: implement the experiment harness.")


if __name__ == "__main__":
    print("Experiment harness not implemented yet — see the stub in experiment.py.")
