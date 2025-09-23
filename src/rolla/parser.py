from dataclasses import dataclass
import re
from .errors import UsageError, ValidationError

_DICE_RE = re.compile(r"^(\d+)[d](\d+)(?:[kK](\d+))?(?:([+-])(\d+))?$")
MAX_COUNT = 100
MAX_SIDES = 100


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
            "Invalid expression: expected NdS[k#][+M|-M]")

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
    if count < 1 or count > MAX_COUNT:
        raise ValidationError(f"Invalid dice count: must be 1...{MAX_COUNT}")
    if sides < 2 or sides > MAX_SIDES:
        raise ValidationError(f"Invalid die sides: must be 2...{MAX_SIDES}")
    if keep < 1 or keep > count:
        raise ValidationError("Invalid keep: must be 1..Count")

    return DiceExpr(count=count, sides=sides, keep=keep, modifier=modifier)
