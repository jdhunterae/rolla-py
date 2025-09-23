import sys
import argparse
from .parser import parse
from .roller import roll, RNG, roll_with_advantage, roll_with_disadvantage
from .errors import UsageError, ValidationError


class _NoExitArgumentParser(argparse.ArgumentParser):
    """Raise UsageError instead of exiting, so we control stderr + exit codes."""

    def error(self, message):
        raise UsageError(message)


def _print_attempt(n: int, expr, rr):
    if expr.keep == expr.count:
        print(
            f"Attempt {n} - Rolled {expr.count}d{expr.sides}: {', '.join(map(str, rr.rolls))}")
    else:
        kept_desc = ", ".join(map(str, sorted(rr.kept, reverse=True)))
        if len(rr.dropped) == 1:
            print(
                f"Attempt {n} - Rolled {expr.count}d{expr.sides} (keeping {expr.keep}): {kept_desc}; lowest: {rr.dropped[0]}")
        else:
            print(
                f"Attempt {n} - Rolled {expr.count}d{expr.sides} (keeping {expr.keep}): {kept_desc}; dropped: {', '.join(map(str, rr.dropped))}")

    print(f"Attempt {n} - Result: {rr.total}")


def _print_human(out, expr):
    if hasattr(out, "attempts"):
        a1, a2 = out.attempts
        _print_attempt(1, expr, a1)
        _print_attempt(2, expr, a2)
        hi, lo = (max(a1.total, a2.total), min(a1.total, a2.total))
        if out.final == hi:
            print(
                f"Advantage applied: kept higher of {a1.total} and {a2.total}")
        else:
            print(
                f"Disadvantage applied: kept lower of {a1.total} and {a2.total}")
        print(f"Final: {out.final}")
        return

    # (single attempt unchanged)
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
    p = _NoExitArgumentParser(prog="rolla", add_help=True)
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
