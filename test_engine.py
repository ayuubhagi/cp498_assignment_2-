"""
Correctness tests for the engine. Not part of the graded deliverable, just
proof the rules work in every win direction before teammates build on top.
Run: python3 test_engine.py
"""

from engine import ConnectFour, ROWS, COLS
from random_agent import RandomAgent


def build(moves):
    """Replay a list of columns and return the resulting game."""
    g = ConnectFour()
    for c in moves:
        g.apply_move(c)
    return g


def manual(cells):
    """
    Build a board directly from a {(row, col): player} dict, bypassing turn
    order. Used only to test win detection on a fixed shape.
    """
    g = ConnectFour()
    for (r, c), p in cells.items():
        g.board[r][c] = p
        g.heights[c] = max(g.heights[c], r + 1)
    return g


def test_horizontal():
    # P1 plays cols 0,1,2,3 on the bottom row; P2 parks in col 6.
    g = build([0, 6, 1, 6, 2, 6, 3])
    assert g.winner() == 1, "horizontal win not detected"
    assert g.is_terminal()


def test_vertical():
    # P1 stacks col 3 four times, P2 answers elsewhere.
    g = build([3, 0, 3, 1, 3, 2, 3])
    assert g.winner() == 1, "vertical win not detected"


def test_diagonal_up():
    # "/" diagonal for P1 at (0,0)(1,1)(2,2)(3,3).
    g = manual({(0, 0): 1, (1, 1): 1, (2, 2): 1})
    g.board[0][3] = 2
    g.board[1][3] = 2
    g.board[2][3] = 2
    g.heights[3] = 3
    assert g.check_winning_move(3, 1), "up-diagonal win not detected"


def test_anti_diagonal():
    # "\" diagonal for P1 at (3,0)(2,1)(1,2)(0,3).
    g = manual({(3, 0): 1, (2, 1): 1, (1, 2): 1})
    assert g.check_winning_move(3, 1), "anti-diagonal win not detected"


def test_draw():
    # A genuine full-board draw: 21 vs 21 discs, no four-in-a-row in any
    # direction (rows are bottom-up, matching the engine's board layout).
    pattern = [
        [2, 2, 1, 1, 2, 2, 1],
        [1, 2, 2, 1, 1, 1, 2],
        [2, 2, 1, 2, 2, 2, 1],
        [1, 1, 1, 2, 1, 1, 1],
        [2, 2, 1, 2, 2, 2, 1],
        [2, 1, 2, 1, 1, 1, 2],
    ]
    g = ConnectFour()
    g.board = [row[:] for row in pattern]
    g.heights = [ROWS] * COLS
    g.move_count = ROWS * COLS
    assert not g.legal_moves(), "full board should have no legal moves"
    assert g.is_draw(), "draw not detected"
    assert g.is_terminal()


def test_random_agent_legal():
    g = ConnectFour()
    a = RandomAgent(seed=42)
    while not g.is_terminal():
        m = a.select_move(g)
        assert m in g.legal_moves(), "random agent returned an illegal move"
        g.apply_move(m)


def test_undo_restores_state():
    g = ConnectFour()
    g.apply_move(3)
    snapshot = str(g)
    player_before = g.current_player
    g.apply_move(3)
    g.undo_move()
    assert str(g) == snapshot, "undo did not restore the board"
    assert g.current_player == player_before, "undo did not restore the turn"


def test_check_winning_move_is_nonmutating():
    g = build([0, 6, 1, 6, 2])  # P1 has three in a row on the bottom
    before = str(g)
    assert g.check_winning_move(3, 1) is True
    assert str(g) == before, "check_winning_move mutated the board"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS  {t.__name__}")
    print(f"\nAll {len(tests)} engine tests passed.")
