from dataclasses import dataclass
import random
from typing import List
from typing import List, NamedTuple, Optional
from .parser import DiceExpr


class RNG:
    """Thin wrapper so we can inject a deterministic RNG in tests."""

    def __init__(self, seed: Optional[int] = None):
        self._r = random.Random(seed)

    def randint(self, a: int, b: int) -> int:
        return self._r.randint(a, b)


@dataclass(frozen=True)
class RollResult:
    rolls: list[int]
    kept: list[int]
    dropped: list[int]
    modifier: int
    total: int


class AdvResult(NamedTuple):
    attempts: list[RollResult]
    final: int


def roll(expr: DiceExpr, rng: RNG) -> RollResult:
    """Rolls, keeps top-K (stable), applies modifier, returns structured result."""
    rolls = [rng.randint(1, expr.sides) for _ in range(expr.count)]
    # choose top-K by value; stable: sort by value desc, index asc
    indexed = list(enumerate(rolls))
    indexed.sort(key=lambda t: (-t[1], t[0]))
    kept_idx = set(i for i, _ in indexed[:expr.keep])
    kept = [v for i, v in enumerate(rolls) if i in kept_idx]
    dropped = [v for i, v in enumerate(rolls) if i not in kept_idx]
    total = sum(kept) + expr.modifier
    return RollResult(rolls=rolls, kept=kept, dropped=dropped, modifier=expr.modifier, total=total)


def roll_with_advantage(expr: DiceExpr, rng: "RNG") -> AdvResult:
    a1 = roll(expr, rng)
    a2 = roll(expr, rng)
    return AdvResult(attempts=[a1, a2], final=max(a1.total, a2.total))


def roll_with_disadvantage(expr: DiceExpr, rng: "RNG") -> AdvResult:
    a1 = roll(expr, rng)
    a2 = roll(expr, rng)
    return AdvResult(attempts=[a1, a2], final=min(a1.total, a2.total))
