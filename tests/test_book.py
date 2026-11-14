"""Tests for the Book class."""
import pytest
from book import Book


def test_new_book_has_title_author_and_condition():
    book = Book("The Little Prince", "Antoine de Saint-Exupery", "good", "fiction")
    assert book.title == "The Little Prince"
    assert book.author == "Antoine de Saint-Exupery"
    assert book.condition == "good"


@pytest.mark.parametrize("condition, expected_points", [
    ("new", 30),
    ("good", 20),
    ("fair", 10),
])
def test_points_value_depends_on_condition(condition, expected_points):
    book = Book("Ikigai", "Hector Garcia", condition, "non-fiction")
    assert book.points_value == expected_points


def test_empty_title_is_rejected():
    with pytest.raises(ValueError):
        Book(" ", "Some Author", "new", "fiction")


def test_unknown_condition_is_rejected():
    with pytest.raises(ValueError):
        Book("Ikigai", "Hector Garcia", "torn", "fiction")


def test_search_matches_ignore_uppercase():
    book = Book("Clean Code", "Robert C. Martin", "fair", "technology")
    assert book.matches("clean") is True
    assert book.matches("CODE") is True
    assert book.matches("python") is False


def test_two_books_with_same_title_and_author_are_equal():
    first = Book("Ikigai", "Hector Garcia", "new", "non-fiction")
    second = Book("IKIGAI", "hector garcia", "good", "non-fiction")
    assert first == second