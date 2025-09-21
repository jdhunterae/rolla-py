import pytest
from rolla import __version__
from rolla import errors
from rolla import parser


def test_version_string():
    assert isinstance(__version__, str)


def test_parse_nds_minimal():
    expr = parser.parse("1d20")
    assert expr.count == 1
    assert expr.sides == 20
    assert expr.keep == 1  # default keep = count
    assert expr.modifier == 0


@pytest.mark.parametrize("bad", ["d20", "0d6", "1d1", "2d", "2x6", ""])
def test_parse_rejects_bad_nds(bad):
    with pytest.raises(errors.UsageError):
        parser.parse(bad)
