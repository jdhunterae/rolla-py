from dataclasses import dataclass
import re
from .errors import UsageError, ValidationError

_DICE_RE = re.compile(r"^(\d+)[d](\d+)$")


@dataclass(frozen=True)
class DiceExpr:
    count: int
    sides: int
    keep: int
    modifier: int


def parse(text: str) -> DiceExpr:
    m = _DICE_RE.match(text or "")
    if not m:
        raise UsageError("Invalid expression: expected NdS")
    count = int(m.group(1))
    sides = int(m.group(2))
    if count < 1:
        raise ValidationError("Invalid dice count: must be >= 1")
    if sides < 2:
        raise ValidationError("Invalid die sides: must be >= 2")
    return DiceExpr(count=count, sides=sides, keep=count, modifier=0)
