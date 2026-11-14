"""The Book Swap library: all rules live here, ready to test."""

from datetime import date, timedelta
class BookSwapLibrary:
    def __init__(self):
        self.available = []      # books waiting to be redeemed
        self.members = {}        # member_id -> Member

    def register(self, member):
        if member.member_id in self.members:
            raise ValueError(
                f"Member ID {member.member_id} already exists."
            )
        self.members[member.member_id] = member

    def _require_member(self, member_id):
        if member_id not in self.members:
            raise ValueError(f"No member with ID {member_id}.")
        return self.members[member_id]

    def donate(self, book, member_id):
        """Add a book and award the donor its points value."""
        member = self._require_member(member_id)
        if book in self.available:
            raise ValueError(
                f"'{book.title}' by {book.author} already exists."
            )
        self.available.append(book)
        
        # Calculate points earned
        points_earned = book.points_value
        
        # Loyalty bonus: if they have already donated 5 or more books
        if len(member.donated) >= 5:
            points_earned += 10

        member.earn(points_earned)
        member.donated.append(book)
        return member.points

    def redeem(self, book, member_id):
        """Give an available book to a member who has enough points."""
        member = self._require_member(member_id)
        if book not in self.available:
            raise ValueError(f"'{book.title}' is not available.")
        member.spend(book.points_value)
        self.available.remove(book)
        member.redeemed.append(book)
        return member.points

    def search(self, query):
        """All available books matching the query (case-insensitive)."""
        query = query.strip()
        if not query:
            raise ValueError("Search query cannot be empty.")
        return [b for b in self.available if b.matches(query)]

    def search_by_genre(self, genre):
        """All available books matching the given genre (case-insensitive)."""
        genre = genre.strip().lower()
        if not genre:
            raise ValueError("Genre query cannot be empty.")
        return [b for b in self.available if b.genre.lower() == genre]
    def borrow(self, book, member_id):
        """Lend an available book to a member for 14 days."""
        member = self._require_member(member_id)
        if book not in self.available:
            raise ValueError(f"'{book.title}' is not available.")
        self.available.remove(book)
        book.due_date = date.today() + timedelta(days=14)
        member.borrowed.append(book)
        return book.due_date