import hypothesis.strategies as st
from hypothesis import given
from rolla.parser import DiceExpr
from rolla import roller


@given(
    count=st.integers(min_value=1, max_value=50),
    sides=st.integers(min_value=2, max_value=100),
    keep=st.integers(min_value=1, max_value=50),
    modifier=st.integers(min_value=-100, max_value=100),
    seed=st.integers(min_value=0, max_value=10_000)
)
def test_roll_properties(count, sides, keep, modifier, seed):
    keep = min(keep, count)
    e = DiceExpr(count=count, sides=sides, keep=keep, modifier=modifier)
    out = roller.roll(e, roller.RNG(seed))

    assert len(out.rolls) == count
    assert all(1 <= r <= sides for r in out.rolls)
    assert len(out.kept) == keep
    assert sum(out.kept) >= keep and sum(out.kept) <= keep * sides
    assert out.total == sum(out.kept) + modifier
