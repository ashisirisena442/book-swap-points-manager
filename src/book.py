"""A single book in the swap library."""


class Book:
    # Points a donor earns, by condition of the book.
    POINTS_BY_CONDITION = {
        "new": 30,
        "good": 20,
        "fair": 10,
    }

    def __init__(self, title, author, condition, genre):
        title = title.strip()
        author = author.strip()
        if not title:
            raise ValueError("Title cannot be empty.")
        if not author:
            raise ValueError("Author cannot be empty.")
        if condition not in self.POINTS_BY_CONDITION:
            allowed = ",".join(self.POINTS_BY_CONDITION)
            raise ValueError(
                f"Condition must be one of: {allowed}. "
                f"Got '{condition}'."
            )
        
        # Validate and set genre
        genre = genre.strip()
        if not genre:
            raise ValueError("Genre cannot be empty.")

        self.title = title
        self.author = author
        self.condition = condition
        self.due_date = None
        self.genre = genre

    @property
    def points_value(self):
        """Points earned when donated, charged when redeemed."""
        return self.POINTS_BY_CONDITION[self.condition]

    def matches(self, query):
        """Case-insensitive: does the title contain the query?"""
        return query.lower() in self.title.lower()

    def __eq__(self, other):
        """Two books are 'the same book' if title AND author match."""
        if not isinstance(other, Book):
            return NotImplemented
        return (
            self.title.lower() == other.title.lower()
            and self.author.lower() == other.author.lower()
        )

    def __repr__(self):
        return (f"Book({self.title!r}, {self.author!r}, "
                f"{self.condition!r}, {self.genre!r})")