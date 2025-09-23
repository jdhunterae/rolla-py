import os
import sys
import argparse
from .parser import parse
from .roller import roll, RNG, roll_with_advantage, roll_with_disadvantage
from .errors import UsageError, ValidationError


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


def _parse_args(argv):
    p = argparse.ArgumentParser(prog="rolla", add_help=True)
    p.add_argument("-a", "--advantage", action="store_true")
    p.add_argument("-d", "--disadvantage", action="store_true")
    p.add_argument("--seed", type=int)
    p.add_argument("expression")
    return p.parse_args(argv)


def main() -> int:
    try:
        ns = _parse_args(sys.argv[1:])
        if ns.advantage and ns.disadvantage:
            raise UsageError("Cannot use advantage and disadvantage together")

        expr = parse(ns.expression)
        rng = RNG(ns.seed)
        if ns.advantage:
            out = roll_with_advantage(expr, rng)
        elif ns.disadvantage:
            out = roll_with_disadvantage(expr, rng)
        else:
            out = roll(expr, rng)
        _print_human(out, expr)
        return 0
    except UsageError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except ValidationError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3
    except SystemExit as e:
        # argparse parse failure (e.g., missing expression). Keep process alive for tests
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
