import os
import sys
from .parser import parse
from .roller import roll, RNG


def _print_human(out, expr):
    # verify small formatter for now
    if expr.keep == expr.count:
        print(
            f"Rolled {expr.count}d{expr.sides}: {', '.join(map(str, out.rolls))}")
    else:
        # Show kept (desc) and dropped
        kept_desc = ", ".join(map(str, sorted(out.kept, reverse=True)))
        if len(out.dropped) == 1:
            print(
                f"Rolled {expr.count}d{expr.sides} (keeping {expr.keep}): {kept_desc}; lowest: {out.dropped[0]}")
        else:
            print(
                f"Rolled {expr.count}d{expr.sides} (keeping {expr.keep}): {kept_desc}; dropped: {', '.join(map(str, out.dropped))}")

    print(f"Result: {out.total}")


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print("usage: rolla [-a|-d] [--seed N] EXPRESSION")
        return 0
    # seed via flag later; accept env for now to keep tests simple
    seed = os.getenv("ROLLA_SEED")
    try:
        expr = parse(argv[-1])
        out = roll(expr, RNG(int(seed) if seed is not None else None))
        _print_human(out, expr)
        return 0
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
