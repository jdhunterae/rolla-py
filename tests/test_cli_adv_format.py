from rolla.cli import main


def run(argv, monkeypatch, capsys):
    import sys
    old = sys.argv[:]
    sys.argv = ["rolla"] + argv
    try:
        code = main()
        out = capsys.readouterr()
        return code, out.out
    finally:
        sys.argv = old


def test_advantage_includes_attempt_blocks(monkeypatch, capsys):
    code, out = run(["--seed", "7", "-a", "1d20+2"], monkeypatch, capsys)
    assert code == 0
    assert "Attempt 1 - Rolled" in out
    assert "Attempt 1 - Result:" in out
    assert "Attempt 2 - Rolled" in out
    assert "Attempt 2 - Result:" in out
    assert "Advantage applied: kept higher of" in out
    assert "Final:" in out


def test_disadvantage_includes_attempt_blocks(monkeypatch, capsys):
    code, out = run(["--seed", "7", "-d", "2d10"], monkeypatch, capsys)
    assert code == 0
    assert "Disadvantage applied: kept lower of" in out
