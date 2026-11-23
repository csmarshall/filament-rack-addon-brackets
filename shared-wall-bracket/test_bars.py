"""Checks that Params(bars=n) derives the bar pattern from the stock 4-bar bracket.

Run with: python3 test_bars.py   (plain asserts, no test framework needed; pytest also collects it)
"""
from shared_wall_bracket import Params, build_bracket, check_tie_slit_strength

STAGGERED_3BAR_SOCKETS = [26.0, 44.0, 110.0, 128.0, 194.0, 212.0]


def test_four_bars_is_the_stock_bracket() -> None:
    p = Params()
    assert p.bar_y == [26.0, 110.0, 194.0, 278.0]
    assert p.length == p.stock_length == 305.0
    assert Params.staggered().length == 322.0


def test_three_bar_in_line_and_end() -> None:
    for p in (Params(bars=3), Params.end(bars=3)):
        assert p.bar_y == [26.0, 110.0, 194.0]
        assert p.length == p.stock_length == 221.0
        assert p.tie_slit_ys == [40.0, 181.0]
        p.validate()
        check_tie_slit_strength(p, build_bracket(p))


def test_three_bar_staggered() -> None:
    for mirror in (False, True):
        p = Params.staggered(bars=3, mirror=mirror)
        assert p.length == 238.0
        assert sorted(set(p.bar_y_left + p.bar_y_right)) == STAGGERED_3BAR_SOCKETS
        assert p.tie_slit_ys == [60.0, 178.0]
        p.validate()
        check_tie_slit_strength(p, build_bracket(p))


def test_bars_out_of_range() -> None:
    for bars in (1, 2, 5, True):
        try:
            Params(bars=bars).validate()
        except ValueError:
            continue
        raise AssertionError(f"bars={bars} was accepted")


def test_inconsistent_bar_y_is_rejected() -> None:
    for p in (Params(bars=3, bar_y=[26.0, 110.0, 194.0, 278.0]), Params(bars=3, bar_y=[26.0, 110.0, 300.0])):
        try:
            p.validate()
        except ValueError:
            continue
        raise AssertionError(f"bar_y={p.bar_y} was accepted")


def test_end_bracket_turned_end_for_end() -> None:
    p = Params.end(bars=3)
    assert sorted(p.length - y for y in p.bar_y)[0] == 27.0


def test_staggered_faces_are_mirrored() -> None:
    a, b = Params.staggered(bars=3), Params.staggered(bars=3, mirror=True)
    assert a.bar_y_left == b.bar_y_right and a.bar_y_right == b.bar_y_left
    assert a.bar_y_left == [26.0, 110.0, 194.0] and a.bar_y_right == [44.0, 128.0, 212.0]
    assert sorted(a.length - y for y in a.bar_y_left) == a.bar_y_right


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
