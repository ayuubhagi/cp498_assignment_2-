# CP468 Assignment 2 — Connect Four Agents

A Connect Four engine and a set of AI agents that play it, plus an experiment
harness that pits them against each other. Group project for CP468.

## Repository layout

| File | Owner | Status |
|---|---|---|
| `engine.py` | Ayuub | **done, frozen** — shared rules (see `INTERFACE.md`) |
| `base_agent.py` | Ayuub | **done** — the `select_move(game)` contract |
| `random_agent.py` | Ayuub | **done** — Agent 1 (random baseline) |
| `test_engine.py` | Ayuub | **done** — 8 correctness tests |
| `demo_random_vs_random.py` | Ayuub | **done** — full game + harness template |
| `INTERFACE.md` | Ayuub | **done** — one-page cheat sheet, build against this |
| `rule_agent.py` | Teammate 2 | stub — rule-based agent |
| `minimax_agent.py` | Teammate 3 | stub — minimax / alpha-beta agent |
| `experiment.py` | Teammate 4 | stub — match runner, results, seeds |
| `Report.pdf` | everyone | exported from the shared Google Doc at the end |

## Quick start

```bash
git clone <repo-url>
cd A2
python3 test_engine.py            # should print: All 8 engine tests passed.
python3 demo_random_vs_random.py  # watch a full random game play out
```

No dependencies — standard library only, Python 3.8+.

## For teammates building an agent

Read `INTERFACE.md`. It has everything: the state you can read, the methods you
can call, both look-ahead patterns (copy vs apply/undo), and the tie-breaking
snippet. You should not need to open `engine.py`.

Subclass `BaseAgent` and implement `select_move(game)`. Don't mutate the `game`
you're handed — use `game.copy()` or `apply_move()`/`undo_move()`.

## How we work together (git flow)

File ownership is disjoint, so nobody edits the same file and merge conflicts
are basically zero.

1. Clone the repo.
2. Make a branch for your piece: `git checkout -b minimax` (or `rule-based`, `harness`).
3. Commit and push your branch: `git push -u origin minimax`.
4. Open a pull request into `main`. Someone reviews and merges.

**One hard rule:** `main` must always pass `python3 test_engine.py`. Don't merge
anything that breaks it — that's what protects the harness person from inheriting
a broken engine the night before the deadline.

If a teammate genuinely can't use git, send your one file to Ayuub and it gets
committed for you — but git is worth learning, it's one afternoon.

## Report & video

The written report lives in a shared Google Doc (co-write there, it's built for
five people editing prose and tables). Export to `Report.pdf` at the very end and
drop it in the repo. The demo video goes to YouTube (unlisted) or Drive; link it
here and in the report.
