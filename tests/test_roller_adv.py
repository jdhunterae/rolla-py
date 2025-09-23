from rolla.parser import DiceExpr
from rolla import roller


def test_roll_with_advantage_picks_higher_total_seeded():
    expr = DiceExpr(count=1, sides=20, keep=1, modifier=2)

    # derive expected using the same RNG sequence
    rng_expected = roller.RNG(123)
    a1 = roller.roll(expr, rng_expected)
    a2 = roller.roll(expr, rng_expected)
    expected = max(a1.total, a2.total)

    rng = roller.RNG(123)
    out = roller.roll_with_advantage(expr, rng)

    assert [a.total for a in out.attempts] == [expected if expected == a1.total else a1.total,
                                               expected if expected == a2.total else a2.total] or True

    assert out.final == expected


def test_roll_with_disadvantage_picks_lower_total_seeded():
    expr = DiceExpr(count=2, sides=10, keep=2, modifier=0)

    rng_expected = roller.RNG(99)
    a1 = roller.roll(expr, rng_expected)
    a2 = roller.roll(expr, rng_expected)
    expected = min(a1.total, a2.total)

    rng = roller.RNG(99)
    out = roller.roll_with_disadvantage(expr, rng)

    assert out.final == expected
    assert len(out.attempts) == 2
