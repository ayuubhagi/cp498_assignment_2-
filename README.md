# CP468 Assignment 2 - Connect Four Agents

A Connect Four engine and a set of AI agents that play it, plus an experiment
harness that pits them against each other. Group project for CP468.

## Team (5 members)

| # | Member | Part | Status |
|---|---|---|---|
| 1 | Ayuub | engine + random agent (Part 1) | done |
| 2 | Mohanad139 | group member (part not chosen yet) | - |
| 3 | YakupBastug06 | Minmax Agent + video | - |
| 4 | KhaledM0barak | rule_agent + experiment | done |
| 5 | orhangundogan | Minmax Agent + video | done |

Only Part 1 is claimed so far. Parts still open to claim: rule-based agent,
minimax / alpha-beta agent, experiment harness, and report + demo video. Grab
one, then update the table and the layout below with your name.

## Repository layout

| File | Owner | Status |
|---|---|---|
| `engine.py` | Ayuub | done, frozen. Shared rules (see `INTERFACE.md`) |
| `base_agent.py` | Ayuub | done. The `select_move(game)` contract |
| `random_agent.py` | Ayuub | done. Agent 1 (random baseline) |
| `test_engine.py` | Ayuub | done. 8 correctness tests |
| `demo_random_vs_random.py` | Ayuub | done. Full game plus harness template |
| `INTERFACE.md` | Ayuub | done. One-page cheat sheet, build against this |
| `rule_agent.py` | Khaled | done. Rule-based agent |
| `minimax_agent.py` | Orhan - Yakup| stub. Minimax / alpha-beta agent |
| `experiment.py` | Khaled | done. Match runner, results, seeds |
| `Report.pdf` | unassigned | exported from the shared Google Doc at the end |

## Quick start

```bash
git clone <repo-url>
cd A2
python3 test_engine.py            # should print: All 8 engine tests passed.
python3 demo_random_vs_random.py  # watch a full random game play out
```

No dependencies, standard library only, Python 3.8+.

## For teammates building an agent

Read `INTERFACE.md`. It has everything you need: the state you can read, the
methods you can call, both look-ahead patterns (copy vs apply/undo), and the
tie-breaking snippet. You should not need to open `engine.py`.

Subclass `BaseAgent` and implement `select_move(game)`. Do not mutate the `game`
you are handed. Use `game.copy()` or `apply_move()` / `undo_move()`.

## How we work together (git flow)

File ownership is disjoint, so nobody edits the same file and merge conflicts
are basically zero.

1. Clone the repo.
2. Make a branch for your piece: `git checkout -b minimax` (or `rule-based`, `harness`).
3. Commit and push your branch: `git push -u origin minimax`.
4. Open a pull request into `main`. Someone reviews and merges.

One hard rule: `main` must always pass `python3 test_engine.py`. Do not merge
anything that breaks it. That is what stops the harness person from inheriting a
broken engine the night before the deadline.

If a teammate cannot use git yet, send your one file to Ayuub and it gets
committed for you. But git is worth learning, it is one afternoon.

## Report and video

The written report lives in a shared Google Doc. Co-write there, it handles five
people editing prose and tables far better than the repo does. Export to
`Report.pdf` at the very end and drop it in the repo. The demo video goes to
YouTube (unlisted) or Drive. Link it here and in the report.

**Demo video:** https://www.youtube.com/watch?v=y9G-oM2I6Ys
