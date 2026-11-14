"""Tests for the app.py helper functions."""
import pytest
from app import parse_choice


@pytest.mark.parametrize("user_input, expected", [
    ("1", 1),
    (" 3 ", 3),       # handles whitespace
    ("5", 5),
    ("9", None),      # out of range
    ("abc", None),    # letters
    ("", None),       # empty string
])
def test_parse_choice(user_input, expected):
    assert parse_choice(user_input) == expected