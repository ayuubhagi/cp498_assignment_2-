"""
Experiment harness — Requirement 3, Experimental Evaluation.  OWNER: Khaled.

Runs the three required head-to-head pairings, alternating which agent moves
first for fairness, and reports per-agent win rate, draw rate, and average
decision time per move. Everything is seeded so results reproduce exactly.

Required pairings:
    Random    vs Rule-Based   (baseline vs simple heuristics)
    Rule-Based vs Minimax      (heuristics vs search)
    Minimax   vs Random        (search vs baseline)

Usage:
    python3 experiment.py                      # 30 games/pairing, seed 42, depth 4
    python3 experiment.py --games 30 --seed 42 --depth 4 --csv results.csv

Note: the Minimax agent is a separate teammate's part. Until it is implemented
this harness still runs fully — the two Minimax pairings are reported as
"pending (agent not implemented yet)" and the Random vs Rule-Based pairing
produces real numbers. Once minimax lands, re-run for the complete table.
"""

import argparse
import platform
import statistics
import time

from engine import ConnectFour
from random_agent import RandomAgent
from rule_agent import RuleAgent
from minimax_agent import MinimaxAgent


# ---------------------------------------------------------------------- #
#  Agent factories: build a fresh, seeded agent for a given side.        #
#  Each pairing/game gets fresh instances so the random tie-break varies #
#  between games while staying reproducible from the master seed.        #
# ---------------------------------------------------------------------- #
def make_random(player, seed, depth):
    return RandomAgent(player=player, seed=seed, name="Random")


def make_rule(player, seed, depth):
    return RuleAgent(player=player, seed=seed, name="Rule-Based")


def make_minimax(player, seed, depth):
    # The minimax stub currently takes no seed; pass one if/when it accepts it,
    # so the harness keeps working either way.
    try:
        return MinimaxAgent(player=player, depth=depth, seed=seed, name="Minimax")
    except TypeError:
        return MinimaxAgent(player=player, depth=depth, name="Minimax")


# ---------------------------------------------------------------------- #
#  One timed game                                                        #
# ---------------------------------------------------------------------- #
def play_timed_game(agent1, agent2):
    """
    Play one game. agent1 is player 1 (moves first), agent2 is player 2.

    Returns (winner, times) where winner is 1, 2, or 0 (draw) and times is
    {1: [seconds per move...], 2: [...]}.
    """
    game = ConnectFour()
    agents = {1: agent1, 2: agent2}
    times = {1: [], 2: []}

    while not game.is_terminal():
        mover = game.current_player
        start = time.perf_counter()
        col = agents[mover].select_move(game)
        times[mover].append(time.perf_counter() - start)
        game.apply_move(col)

    result = game.winner()
    return (result if result is not None else 0), times


# ---------------------------------------------------------------------- #
#  One pairing: N games, alternating who moves first                     #
# ---------------------------------------------------------------------- #
def run_pairing(label_a, make_a, label_b, make_b, games, base_seed, depth):
    """
    Play `games` games between agent A and agent B, swapping the first move
    every game. Returns a results dict, or None if an agent is not implemented.
    """
    wins = {label_a: 0, label_b: 0, "draw": 0}
    times = {label_a: [], label_b: []}

    for g in range(games):
        # Distinct seeds per game and per side: independent yet reproducible.
        agent_a = make_a(0, base_seed + g * 2, depth)
        agent_b = make_b(0, base_seed + g * 2 + 1, depth)

        if g % 2 == 0:                       # A moves first on even games
            first, second = agent_a, agent_b
            first_label, second_label = label_a, label_b
        else:                                # B moves first on odd games
            first, second = agent_b, agent_a
            first_label, second_label = label_b, label_a
        # The mover's player id is fixed by position; set it for agents that use it.
        first.player, second.player = 1, 2

        try:
            winner, times_by_player = play_timed_game(first, second)
        except NotImplementedError:
            return None                      # an agent isn't implemented yet

        if winner == 0:
            wins["draw"] += 1
        elif winner == 1:
            wins[first_label] += 1
        else:
            wins[second_label] += 1

        times[first_label].extend(times_by_player[1])
        times[second_label].extend(times_by_player[2])

    return {"wins": wins, "times": times}


# ---------------------------------------------------------------------- #
#  Reporting                                                             #
# ---------------------------------------------------------------------- #
def _pct(n, total):
    return "%5.1f%%" % (100.0 * n / total) if total else "   n/a"


def _avg_ms(seq):
    return 1000.0 * statistics.mean(seq) if seq else 0.0


def print_pairing(label_a, label_b, result, games, rows):
    print("\n" + "=" * 62)
    print("  %s  vs  %s   (%d games, ~%d each way)"
          % (label_a, label_b, games, games // 2))
    print("=" * 62)

    if result is None:
        print("  pending -- one of these agents is not implemented yet.")
        return

    wins, times = result["wins"], result["times"]
    header = "  %-12s %8s %10s %10s %16s" % (
        "Agent", "Wins", "Win rate", "Draws", "Avg ms/move")
    print(header)
    print("  " + "-" * (len(header) - 2))
    for label in (label_a, label_b):
        print("  %-12s %8d %10s %10s %16.3f"
              % (label, wins[label], _pct(wins[label], games),
                 _pct(wins["draw"], games), _avg_ms(times[label])))
        rows.append(("%s_vs_%s" % (label_a, label_b), label, wins[label],
                     "%.1f" % (100.0 * wins[label] / games),
                     wins["draw"], "%.1f" % (100.0 * wins["draw"] / games),
                     "%.3f" % _avg_ms(times[label])))


# ---------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Connect Four experiments")
    ap.add_argument("--games", type=int, default=30, help="games per pairing")
    ap.add_argument("--seed", type=int, default=42, help="master random seed")
    ap.add_argument("--depth", type=int, default=4, help="minimax search depth")
    ap.add_argument("--csv", type=str, default=None, help="optional CSV output path")
    args = ap.parse_args()

    print("Connect Four - Experimental Evaluation")
    print("Machine : %s %s (%s) | Python %s"
          % (platform.system(), platform.release(),
             platform.machine(), platform.python_version()))
    print("CPU     : %s" % (platform.processor() or "see report"))
    print("Seed    : %d    Games/pairing: %d    Minimax depth: %d"
          % (args.seed, args.games, args.depth))

    # The three required pairings. Each pairing's seed space is offset so no two
    # pairings replay the same games.
    pairings = [
        ("Random", make_random, "Rule-Based", make_rule),
        ("Rule-Based", make_rule, "Minimax", make_minimax),
        ("Minimax", make_minimax, "Random", make_random),
    ]

    csv_rows = []
    for i, (la, ma, lb, mb) in enumerate(pairings):
        result = run_pairing(la, ma, lb, mb, args.games,
                             args.seed + i * 100_000, args.depth)
        print_pairing(la, lb, result, args.games, csv_rows)

    if args.csv:
        header = ("pairing", "agent", "wins", "win_rate_pct",
                  "draws", "draw_rate_pct", "avg_ms_per_move")
        with open(args.csv, "w") as fh:
            fh.write(",".join(header) + "\n")
            for row in csv_rows:
                fh.write(",".join(str(x) for x in row) + "\n")
        print("\nWrote CSV -> %s" % args.csv)


if __name__ == "__main__":
    main()
