import pytest
from rolla import __version__
# parser will be imported in Phase 1 to go red


def test_version_string():
    assert isinstance(__version__, str)
