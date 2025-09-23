from dataclasses import dataclass
import re
from .errors import UsageError, ValidationError

_DICE_RE = re.compile(r"^(\d+)[d](\d+)(?:[kK](\d+))?(?:([+-])(\d+))?$")


@dataclass(frozen=True)
class DiceExpr:
    count: int
    sides: int
    keep: int
    modifier: int


def parse(text: str) -> DiceExpr:
    m = _DICE_RE.match(text or "")

    if not m:
        raise UsageError(
            "Invalid expression: expected expected NdS[k#][+M|-M]")

    count = int(m.group(1))
    sides = int(m.group(2))
    keep = int(m.group(3)) if m.group(3) else count

    if m.group(4) and m.group(5):
        sign = -1 if m.group(4) == "-" else 1
        modifier = sign * int(m.group(5))
    elif m.group(4) or m.group(5):
        raise UsageError("Invalid modifier")
    else:
        modifier = 0

    # Validations
    if count < 1:
        raise ValidationError("Invalid dice count: must be >= 1")
    if sides < 2:
        raise ValidationError("Invalid die sides: must be >= 2")
    if keep < 1 or keep > count:
        raise ValidationError("Invalid keep: must be 1..Count")

    return DiceExpr(count=count, sides=sides, keep=keep, modifier=modifier)
