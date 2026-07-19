"""
Plays one full Minimax vs Rule-Based game and prints the board each turn.
Used in the demonstration video (Requirement 5): one AI-vs-AI match, move by move.

Run: python3 demo_match.py
"""

from demo_random_vs_random import play_game
from minimax_agent import MinimaxAgent
from rule_agent import RuleAgent

if __name__ == "__main__":
    p1 = MinimaxAgent(player=1, depth=4, name="Minimax-d4")
    p2 = RuleAgent(player=2, seed=7, name="Rule-Based")

    result = play_game(p1, p2, verbose=True)

    print("\n" + "=" * 30)
    if result == 0:
        print("Result: draw")
    else:
        print(f"Result: player {result} ({p1.name if result == 1 else p2.name}) wins")
