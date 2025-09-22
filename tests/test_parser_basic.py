import pytest
from rolla import __version__
from rolla import errors, parser


def test_version_string():
    assert isinstance(__version__, str)


def test_parse_nds_minimal():
    expr = parser.parse("1d20")
    assert expr.count == 1
    assert expr.sides == 20
    assert expr.keep == 1  # default keep = count
    assert expr.modifier == 0


@pytest.mark.parametrize("bad", ["d20", "2d", "2x6", ""])
def test_parse_rejects_bad_syntax(bad):
    with pytest.raises(errors.UsageError):
        parser.parse(bad)


@pytest.mark.parametrize("bad", ["0d6", "1d1"])
def test_parse_rejects_semantic(bad):
    with pytest.raises(errors.ValidationError):
        parser.parse(bad)
