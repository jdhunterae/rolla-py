import pytest
from rolla import errors, parser


def test_parse_with_positive_modifier():
    e = parser.parse("3d8+2")
    assert e.count == 3 and e.sides == 8 and e.keep == 3 and e.modifier == 2


def test_parse_with_negative_modifier():
    e = parser.parse("3d8k2-1")
    assert e.count == 3 and e.sides == 8 and e.keep == 2 and e.modifier == -1


@pytest.mark.parametrize("bad", ["2d6+", "2d6-", "2d6+-1", "2d6+X"])
def test_modifier_malformed(bad):
    with pytest.raises(errors.UsageError):
        parser.parse(bad)
