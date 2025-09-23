import pytest
from rolla.cli import main


def run(argv, monkeypatch, capsys):
    import sys
    old = sys.argv[:]
    try:
        code = main()
        out = capsys.readouterr()
        return code, out.out, out.err
    finally:
        sys.argv = old


def test_cli_advantage_runs(monkeypatch, capsys):
    monkeypatch.setenv("ROLLA_SEED", "42")
    code, out, err = run(['-a', '1d20+2'], monkeypatch, capsys)
    assert code == 0
    assert "Final:" in out


def test_cli_disadvantage_runs(monkeypatch, capsys):
    monkeypatch.setenv("ROLLA_SEED", "42")
    code, out, err = run(['--disadvantage', '2d10'], monkeypatch, capsys)
    assert code == 0
    assert "Final:" in out


def test_cli_adv_and_disadv_conflict(monkeypatch, capsys):
    monkeypatch.setenv("ROLLA_SEED", "42")
    code, out, err = run(['-a', '-d', '1d20'], monkeypatch, capsys)
    assert code == 2
    assert "Error:" in err and "Cannot use advantage and disadvantage together" in err
