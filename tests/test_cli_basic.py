import pytest
import shutil
import subprocess
import sys
import os

BIN = shutil.which('python')  # run module as a script for now


def run_cli(*args):
    # until packaging, simulate: python -m rolla <args> or call entry via -c
    # easier: import main via -c is messy; invoke installed console script later
    from rolla.cli import main
    return main  # placeholder to keep this file valid; next commit will go RED


def test_cli_runs_and_prints_result(monkeypatch, capsys):
    from rolla.cli import main
    monkeypatch.setattr("ROLLA_SEED", 42)  # we'll support env seed
    # emulate sys.argv
    monkeypatch.setenv("PYTHONWARNINGS", "ignore")
    import sys
    old = sys.argv[:]
    sys.argv = ['rolla', '2d10']
    try:
        code = main()
        captured = capsys.readouterr()
    finally:
        sys.argv = old

    assert code == 0
    assert "Rolled 2d10:" in captured.out
    assert "Result:" in captured.out
