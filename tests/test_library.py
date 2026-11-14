"""Tests for the BookSwapLibrary rules."""
import pytest
from book import Book
from member import Member
from library import BookSwapLibrary


@pytest.fixture
def library():
    """A fresh library with one member and two donated books."""
    lib = BookSwapLibrary()
    lib.register(Member("Akarsha", "M001"))
    lib.donate(Book("Ikigai", "Hector Garcia", "new", "non-fiction"), "M001")
    lib.donate(Book("Clean Code", "Robert C. Martin", "fair", "technology"), "M001")
    return lib


def test_registering_a_member(library):
    assert "M001" in library.members


def test_duplicate_member_id_is_rejected(library):
    with pytest.raises(ValueError):
        library.register(Member("Someone Else", "M001"))


def test_donating_a_book_awards_points(library):
    # fixture: 'new' Ikigai(30) + 'fair' Clean Code(10)
    assert library.members["M001"].points == 40


def test_donating_the_same_book_twice_is_rejected(library):
    with pytest.raises(ValueError):
        library.donate(Book("Ikigai", "Hector Garcia", "good", "non-fiction"), "M001")


def test_redeeming_removes_book_and_charges_points(library):
    book = library.search("clean")[0]
    library.redeem(book, "M001")
    assert book not in library.available
    assert library.members["M001"].points == 30  # 40 - 10 (fair book)


def test_redeeming_with_too_few_points_is_rejected():
    lib = BookSwapLibrary()
    lib.register(Member("Nimali", "M002"))
    with pytest.raises(ValueError):
        lib.redeem(Book("Ikigai", "Hector Garcia", "new", "non-fiction"), "M002")


def test_redeeming_an_unavailable_book_is_rejected(library):
    book = library.search("ikigai")[0]
    library.redeem(book, "M001")
    with pytest.raises(ValueError):
        library.redeem(book, "M001")  # no longer available


def test_unknown_member_cannot_donate(library):
    with pytest.raises(ValueError):
        library.donate(Book("Dune", "Frank Herbert", "new", "fiction"), "M999")


@pytest.mark.parametrize("query, expected_count", [
    ("ikigai", 1),
    ("clean", 1),
    ("IKIGAI", 1),  # uppercase still finds it
    ("the", 0),     # no title contains 'the'
])
def test_search_matches_any_case(library, query, expected_count):
    assert len(library.search(query)) == expected_count


def test_empty_search_query_is_rejected(library):
    with pytest.raises(ValueError):
        library.search(" ")


# --- EXERCISE 1: Search by Genre Tests ---

def test_search_by_genre_finds_matching_books(library):
    library.donate(Book("Dune", "Frank Herbert", "good", "fiction"), "M001")
    results = library.search_by_genre("fiction")
    assert len(results) == 1
    assert results[0].title == "Dune"


def test_search_by_genre_returns_empty_for_no_match(library):
    results = library.search_by_genre("romance")
    assert len(results) == 0


def test_search_by_genre_rejects_empty_query(library):
    with pytest.raises(ValueError):
        library.search_by_genre(" ")


# --- EXERCISE 2: Loyalty Bonus Tests ---

def test_fifth_donation_gets_no_bonus():
    """Boundary test: The 5th donation should NOT get the bonus."""
    lib = BookSwapLibrary()
    lib.register(Member("Akarsha", "M001"))
    
    # Donate 4 books first (4 * 30 = 120 points)
    for i in range(4):
        lib.donate(Book(f"Book{i}", "Author", "new", "fiction"), "M001")
        
    # The 5th donation
    lib.donate(Book("Book5", "Author", "new", "fiction"), "M001")
    
    # 120 + 30 = 150. No bonus yet.
    assert lib.members["M001"].points == 150


def test_sixth_donation_gets_bonus():
    """Boundary test: The 6th donation SHOULD get the +10 bonus."""
    lib = BookSwapLibrary()
    lib.register(Member("Akarsha", "M001"))
    
    # Donate 5 books first (5 * 30 = 150 points)
    for i in range(5):
        lib.donate(Book(f"Book{i}", "Author", "new", "fiction"), "M001")
        
    # The 6th donation
    lib.donate(Book("Book6", "Author", "new", "fiction"), "M001")
    
    # 150 + 30 (book value) + 10 (bonus) = 190 points.
    assert lib.members["M001"].points == 190
    
def test_borrowing_an_available_book_succeeds(library):
    book = library.search("ikigai")[0]
    library.borrow(book, "M001")
    assert book not in library.available
    assert book in library.members["M001"].borrowed
    assert book.due_date is not None


def test_borrowing_the_same_book_twice_fails(library):
    book = library.search("ikigai")[0]
    library.borrow(book, "M001")
    with pytest.raises(ValueError):
        library.borrow(book, "M001")