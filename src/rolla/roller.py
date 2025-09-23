from dataclasses import dataclass
import random
from typing import List
from .parser import DiceExpr


class RNG:
    def __init__(self, seed=None):
        self._r = random.Random(seed)

    def randint(self, a, b):
        return self._r.randint(a, b)


@dataclass(frozen=True)
class RollResult:
    rolls: List[int]
    kept: List[int]
    dropped: List[int]
    modifier: int
    total: int


def roll(expr: DiceExpr, rng: RNG) -> RollResult:
    rolls = [rng.randint(1, expr.sides) for _ in range(expr.count)]
    # choose top-K by value; stable: sort by value desc, index asc
    indexed = list(enumerate(rolls))
    indexed.sort(key=lambda t: (-t[1], t[0]))
    kept_idx = set(i for i, _ in indexed[:expr.keep])
    kept = [v for i, v in enumerate(rolls) if i in kept_idx]
    dropped = [v for i, v in enumerate(rolls) if i not in kept_idx]
    total = sum(kept) + expr.modifier
    return RollResult(rolls=rolls, kept=kept, dropped=dropped, modifier=expr.modifier, total=total)
