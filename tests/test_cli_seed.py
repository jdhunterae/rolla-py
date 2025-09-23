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


def test_cli_seed_makes_output_reproducible(monkeypatch, capsys):
    code1, out1 = run(["--seed", "123", "2d10"], monkeypatch, capsys)
    code2, out2 = run(["--seed", "123", "2d10"], monkeypatch, capsys)
    assert code1 == code2 == 0
    assert out1 == out2


def test_cli_different_seeds_change_output(monkeypatch, capsys):
    code1, out1 = run(["--seed", "123", "2d10"], monkeypatch, capsys)
    code2, out2 = run(["--seed", "321", "2d10"], monkeypatch, capsys)
    assert out1 != out2
