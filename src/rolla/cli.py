import os
import sys
from .parser import parse
from .roller import roll, RNG, roll_with_advantage, roll_with_disadvantage
from .errors import UsageError


def _print_human(out, expr):
    if hasattr(out, "attempts"):  # adv/disadv result
        print(f"Final: {out.final}")
        return
    if expr.keep == expr.count:
        print(
            f"Rolled {expr.count}d{expr.sides}: {', '.join(map(str, out.rolls))}")
    else:
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

    # crude flag parse to keep diff small; argparse arrives next phase
    adv = False
    dis = False
    args = []
    for a in argv:
        if a in ("-a", "--advantage"):
            adv = True
        elif a in ("-d", "--disadvantage"):
            dis = True
        else:
            args.append(a)

    try:
        if adv and dis:
            raise UsageError("Cannot use advantage and disadvantage together")
        expr = parse(args[-1])
        seed_env = os.getenv("ROLLA_SEED")
        rng = RNG(int(seed_env) if seed_env is not None else None)
        if adv:
            out = roll_with_advantage(expr, rng)
        elif dis:
            out = roll_with_disadvantage(expr, rng)
        else:
            out = roll(expr, rng)

        _print_human(out, expr)
        return 0
    except UsageError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
