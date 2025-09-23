from rolla.cli import main


def run(argv, capsys):
    import sys
    old = sys.argv[:]
    sys.argv = ["rolla"] + argv
    try:
        code = main()
        out = capsys.readouterr()
        return code, out.out, out.err
    finally:
        sys.argv = old


def test_usage_error_returns_2(capsys):
    code, out, err = run(["2dk"], capsys)         # bad syntax
    assert code == 2
    assert "Invalid expression" in err


def test_validation_error_returns_3(capsys):
    code, out, err = run(["2d6k0"], capsys)       # semantic range
    assert code == 3
    assert "Invalid keep" in err
