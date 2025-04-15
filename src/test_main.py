import pytest

from main import extract_title


def test_extract_title():
    with pytest.raises(ValueError):
        extract_title("Hello, World!")


def test_extract_title_with_title():
    assert extract_title("# Hello, World!") == "Hello, World!"
