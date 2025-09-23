# rolla — Console Dice Roller (Python)

A tiny, test-driven Python CLI that parses tabletop dice notation and returns results with clear, reproducible output. Supports keep/drop and advantage/disadvantage.

---

## Features (v1.0 scope)

- Parse a single dice expression: `NdS[kK][+M|-M]`
- Keep/drop with `k#` (e.g., `4d6k3`)
- Modifier `+M`/`-M` (e.g., `1d20+5`, `3d8k2-1`)
- Advantage/Disadvantage flags (`-a` / `-d`)
- Deterministic runs with `--seed`
- Clear, stable output (great for scripts & tests)
- Proper exit codes and error messages

Non-goals (v1.0): multiple expressions, exploding/rerolls, success thresholds, FATE/Fudge.

---

## CLI

```bash
# basic
rolla 1d20
rolla 2d10
rolla 4d6k3
rolla 3d8+2
rolla 3d8k2-1

# advantage / disadvantage
rolla -a 1d20+2
rolla -d 2d10

# deterministic output
rolla --seed 42 4d6k3

# help
rolla -h
````

**Flag rules**

- `-a` and `-d` are allowed independently; using both is an error.

**Exit codes**

- `0` success
- `2` usage/argv errors (bad syntax, conflicting flags, missing args)
- `3` validation errors (out-of-range, e.g., `0d6`, `1d1`, `2d6k0`)

---

## Dice Notation

```
Expression := Count 'd' Sides [ 'k' Keep ] [ Modifier ]
Count      := integer >= 1
Sides      := integer >= 2
Keep       := integer where 1 <= Keep <= Count (default: Keep = Count)
Modifier   := ('+'|'-') integer (>= 0; default: 0)
```

No internal whitespace; lowercase `d` required.

---

## Examples

```
$ rolla 1d20
Rolled 1d20: 17
Result: 17
```

```
$ rolla 2d10
Rolled 2d10: 8, 4
Result: 12
```

```
$ rolla 4d6k3
Rolled 4d6 (keeping 3): 5, 3, 2; lowest: 1
Result: 10
```

Advantage prints attempt blocks with em dashes and a final decision:

```
$ rolla -a 1d20+2
Attempt 1 — Rolled 1d20: 9
Attempt 1 — Result: 11
Attempt 2 — Rolled 1d20: 17
Attempt 2 — Result: 19
Advantage applied: kept higher of 11 and 19
Final: 19
```

---

## Errors (stderr)

- Syntax: `Error: Invalid expression: expected NdS[k#][+M|-M]` → exit `2`
- Conflict: `Error: Cannot use advantage and disadvantage together` → exit `2`
- Range: `Error: Invalid keep: must be 1..Count` → exit `3`
- (Optional guardrails if enabled):
  `Error: Dice count too large (>10000)` / `Error: Die sides too large (>10000)` → exit `3`

---

## Project Layout

```
rolla/
  src/rolla/
    __init__.py        # version
    errors.py          # RollaError, UsageError, ValidationError
    parser.py          # parse & validate → DiceExpr
    roller.py          # RNG, roll(), roll_with_advantage(), roll_with_disadvantage()
    cli.py             # argparse CLI, prints human output
  tests/
    # parser, roller, CLI, adv/disadv formatting, exit codes, properties
  pyproject.toml       # build config + console entry point
  README.md
  LICENSE
  .gitignore
```

**Runtime deps:** stdlib only.
**Dev/test (suggested):** `pytest`, `hypothesis`, `pytest-cov`.

---

## Determinism & RNG

- `--seed <int>` seeds an internal `random.Random` instance (no global RNG mutation).
- Advantage/disadvantage evaluate the *entire expression* twice (including keep/modifier); the higher/lower **final total** wins.

---

## TDD Workflow

1. Write failing tests for a narrow behavior (RED)
2. Implement the smallest change to pass (GREEN)
3. Refactor with tests staying green (REFACTOR)

Suggested phases already in tests:

- Parser: `NdS` → `k#` → modifiers → validation messages
- Roller: keep/drop selection (stable ties), totals
- Advantage/Disadvantage: selection and detailed formatting
- CLI: argv parsing, `--seed`, exit codes
- Properties: bounds/invariants across many random inputs

---

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .[dev]      # if you add extras for pytest/hypothesis
pytest
```

---

## Build & Install

```bash
pip install build
python -m build
# creates dist/rolla-<version>-py3-none-any.whl

# try it with pipx
pipx install dist/rolla-1.0.0-py3-none-any.whl
rolla --seed 42 4d6k3
```

---

## Design Notes

- The CLI uses an `argparse` subclass that raises `UsageError` instead of exiting,
  so the app consistently maps:

  - `UsageError → exit 2`
  - `ValidationError → exit 3`
- Output strings are deterministic and formatting-stable (em dashes in attempt lines) to keep tests resilient.

---

## Roadmap

- **v1.1**: `--json`, `--quiet`, multiple expressions with optional labels
- **v1.2**: exploding dice (`!`), rerolls (`r1`)
- **v1.3**: success thresholds (`>=TN`), Fate/Fudge (`4dF`)
- **v1.4**: config profiles; optional color output

---

## License

MIT
