import pytest
from rolla.parser import DiceExpr
from rolla import roller, errors


def test_roll_nds_no_keep_no_modifier_seeded():
    rng = roller.RNG(42)
    e = DiceExpr(count=2, sides=10, keep=2, modifier=0)
    out = roller.roll(e, rng)
    assert out.total == sum(out.kept) + 0
    assert len(out.rolls) == 2
    assert len(out.kept) == 2


def test_roll_keep_drops_one_seeded():
    rng = roller.RNG(42)
    e = DiceExpr(count=4, sides=6, keep=3, modifier=0)
    out = roller.roll(e, rng)
    assert len(out.kept) == 3 and len(out.dropped) == 1
    assert out.total == sum(out.kept)
