# rolla — Console Dice Roller (Python, v1.0)

A tiny, test-driven Python CLI that parses tabletop dice notation and returns results with clear, reproducible output. Supports keep/drop and advantage/disadvantage.

---

## Goals & Non-Goals

**Goals (v1.0):**

* Parse a single dice expression from the command line and roll it.
* Support `NdS`, optional keep `kK`, and optional modifier `+M`/`-M`.
* Support `--advantage/-a` and `--disadvantage/-d`.
* Deterministic, stable output formatting (great for scripts & tests).
* Clear errors + non-zero exit codes for invalid inputs.
* TDD from the start (unit, CLI, property tests).

**Non-Goals (v1.0):**

* Multiple expressions in one command.
* Exploding dice / rerolls / success-count systems.
* Fate/Fudge dice, percentile shorthands, labels, or comments.

---

## CLI Overview

```bash
# basic
rolla 1d20
rolla 2d10
rolla 4d6k3
rolla 3d8+2
rolla 3d8k2-1

# advantage/disadvantage
rolla -a 1d20+2
rolla --disadvantage 1d20+2

# general
-h, --help
--seed <int>    # optional seed for reproducible rolls (test/debug)
```

**Flag rules (v1.0):**

* `-a` and `-d` are mutually exclusive; if both present → error (exit 2).

**Exit codes:**

* `0`: success
* `2`: invalid usage/args (parse/format errors, conflicting flags)
* `3`: semantic/validation error (e.g., `0d6`, `d0`, `k0` out of range)

---

## Dice Notation (v1.0)

```
Expression := Count 'd' Sides [ 'k' Keep ] [ Modifier ]
Count      := integer >= 1
Sides      := integer >= 2
Keep       := integer where 1 <= Keep <= Count
Modifier   := ('+'|'-') integer (>= 0)
```

**Defaults/assumptions:**

* If `k` omitted → keep all dice (`k = Count`).
* No internal whitespace in the expression.
* Lowercase `d` required.

---

## Behavior & Examples

1. `rolla 1d20`

```
Rolled 1d20: 17
Result: 17
```

2. `rolla 2d10`

```
Rolled 2d10: 8, 4
Result: 12
```

3. `rolla 4d6k3`

```
Rolled 4d6 (keeping 3): 5, 3, 2; lowest: 1
Result: 10
```

4. `rolla -a 1d20+2` (advantage) — the *entire* expression is rolled twice (incl. modifier); keep higher **final result**:

```
Attempt 1 — Rolled 1d20: 9
Attempt 1 — Result: 11
Attempt 2 — Rolled 1d20: 17
Attempt 2 — Result: 19
Advantage applied: kept higher of 11 and 19
Final: 19
```

5. `rolla -d 2d10` (disadvantage) — keep the lower **final result**.

---

## Validation Rules

* Count < 1 → `Invalid dice count: must be >= 1` (exit 3)
* Sides < 2 → `Invalid die sides: must be >= 2` (exit 3)
* Keep < 1 or Keep > Count → `Invalid keep: must be 1..Count` (exit 3)
* Bad format → `Invalid expression: expected NdS[kK][+M|-M]` (exit 2)
* Both `-a` and `-d` → `Cannot use advantage and disadvantage together` (exit 2)
* Malformed modifier → `Invalid modifier` (exit 2)

Errors print to **stderr** with `Error:` prefix.

---

## Output Formatting (acceptance)

Human-readable, stable, newline-terminated.

* Rolls listed in *roll order*.
* Keep line:

  * If exactly one die is dropped: show `lowest: X` (or `dropped: X` when not strictly the lowest by value due to duplicates).
  * If multiple drops: `dropped: a, b, c` (consistent order).
* `Result:` is always the final line for a single attempt.
* With (dis)advantage:

  * Two “Attempt N — …” blocks, then:
  * `Advantage applied: kept higher of X and Y` / `Disadvantage applied: kept lower of X and Y`
  * `Final: Z`

Example multiple drops:

```
Rolled 6d6 (keeping 3): 6, 5, 4; dropped: 3, 2, 1
Result: 15
```

---

## Implementation Plan (Python)

### Project Structure

```
rolla/
  src/rolla/
    __init__.py
    cli.py          # argparse-based CLI
    parser.py       # parse & validate -> dataclass
    roller.py       # RNG + rolling + keep/drop + adv/disadv
    formatters.py   # human output (json later)
    errors.py
  tests/
    test_parser.py
    test_roller.py
    test_cli.py
    test_properties.py
  pyproject.toml    # build config + entry points
  README.md
  LICENSE
```

### Dependencies

* **Runtime:** Python stdlib only (`argparse`, `random`, `re`, `dataclasses` if needed).
* **Dev/Test:** `pytest`, `hypothesis` (property tests), `pytest-cov` (optional).

### Entry Point (pyproject)

```toml
[project]
name = "rolla"
version = "1.0.0"
requires-python = ">=3.9"
dependencies = []

[project.scripts]
rolla = "rolla.cli:main"

[tool.pytest.ini_options]
addopts = "-q"
```

### Parsing Strategy

* Regex: `^(\d+)[d](\d+)(?:[kK](\d+))?(?:([+-])(\d+))?$`
* Build a dataclass:

  ```python
  @dataclass(frozen=True)
  class DiceExpr:
      count: int
      sides: int
      keep: int
      modifier: int
  ```

* Validation post-parse (range checks).

### Randomness & Seeding

* Use a dedicated RNG instance (no global mutation):

  ```python
  rng = random.Random(seed)  # seed is None unless --seed provided
  rng.randint(1, sides)
  ```

### Rolling Algorithm

1. Roll `count` times → list `[1..sides]`.
2. If `keep < count`:

   * Determine kept dice as top `keep` by value (stable/consistent tie behavior).
   * Dropped = multiset difference.
3. Sum(kept) + modifier → total.
4. For (dis)advantage: evaluate twice independently using the same RNG instance state progression (seeded at start), then pick max/min by **total**.

---

## TDD Plan

### Unit — Parser (`tests/test_parser.py`)

* Accept:

  * `1d20`, `2d10`, `4d6k3`, `3d8+2`, `3d8k2-1`
* Reject with specific messages:

  * `0d6`, `1d1`, `2d6k0`, `2d6k3`, `d6`, `2dk`, `2d6+`, `2d6-`, `2d6+-1`
* Defaults: missing `k` → `keep = count`; missing modifier → `0`.

### Unit — Roller (`tests/test_roller.py`)

* With a fixed seed, assert:

  * Deterministic roll lists and totals for simple cases.
  * Keep/drop correctness (`4d6k3`, `6d6k3` including duplicate handling).

### Unit — Adv/Disadv (`tests/test_roller.py`)

* With seed, assert which attempt wins/loses and exact final total chosen.

### CLI — Behavior (`tests/test_cli.py`)

* Use `subprocess.run` or `typer.testing` if swapped later.
* Success paths return exit `0` and exact stdout lines (with `--seed`).
* Invalid inputs return exit `2`/`3` and error to stderr.

### Property Tests — Hypothesis (`tests/test_properties.py`)

* Generate valid tuples `(count>=1, sides>=2, 1<=keep<=count, modifier in [-1000,1000])`
* Properties:

  * Every roll in `[1, sides]`
  * `len(kept) == keep`
  * `sum(kept) ∈ [keep, keep*sides]`
  * `total == sum(kept) + modifier`

### Golden/Snapshot (optional)

* Seeded inputs mapped to expected stdout files.

---

## Build, Test, Install

```bash
# setup
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .[dev]     # if you add extras for pytest/hypothesis

# run tests
pytest

# package + local install (pipx recommended)
python -m build
pipx install dist/rolla-1.0.0-py3-none-any.whl

# try it
rolla --seed 42 4d6k3
```

---

## Performance & Limits

* Plenty fast for tabletop ranges. Hard caps (to avoid accidental abuse):

  * `count <= 10_000`, `sides <= 10_000`
* If exceeded → validation error (exit 3).

---

## Security

* No eval, no shelling out, no file I/O.
* Pure parse → compute → print.

---

## Roadmap

**v1.1**

* `--json` (machine-friendly output).
* `--sum-only` / `--quiet`.
* Multiple expressions in one call, optional labels.

**v1.2**

* Exploding dice (e.g., `!`), rerolls (`r1`).

**v1.3**

* Success counting (`>=TN`), e.g., `10d10>=8`.
* Fate/Fudge (`4dF`).

**v1.4**

* Config profiles; colorized output with `--color/--no-color`.

---

## Definition of Done (v1.0)

* [ ] Parser accepts/rejects per spec (tests passing).
* [ ] Roller keeps/drops correctly; totals correct (unit + property tests).
* [ ] Advantage/disadvantage implemented with clear output.
* [ ] CLI returns proper exit codes; stderr on errors.
* [ ] Seeded runs produce deterministic, testable output.
* [ ] Packaging works; entry point exposes `rolla`; tag `v1.0.0`.
