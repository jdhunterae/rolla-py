import pytest
from rolla import errors, parser


def test_parse_with_keep():
    e = parser.parse("4d6k3")
    assert (e.count, e.sides, e.keep, e.modifier) == (4, 6, 3, 0)


@pytest.mark.parametrize("bad", ["4d6k0", "4d6k5"])
def test_keep_range_errors(bad):
    with pytest.raises(errors.ValidationError):
        parser.parse(bad)
