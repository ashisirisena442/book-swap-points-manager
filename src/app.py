"""Small menu that uses the library. NOTE: no unit tests live here.

app.py only asks the user questions and prints answers. All decisions
(rules) live in book.py, member.py and library.py -- that is what makes
those parts easy to test automatically.
"""
from book import Book
from member import Member
from library import BookSwapLibrary

def parse_choice(text: str):
    """Returns 1-5 as an integer, or None if the input is invalid."""
    text = text.strip()
    if text in ("1", "2", "3", "4", "5"):
        return int(text)
    return None

def main():
    library = BookSwapLibrary()
    print("--= Book Swap Points Manager --=")

    while True:
        print(
            "\n1) Register member  2) Donate a book  3) Redeem a book"
            "  4) Search books  5) Quit"
        )
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            name = input("Member name: ")
            member_id = input("Member ID: ")
            try:
                library.register(Member(name, member_id))
                print(f"Welcome, {name}!")
            except ValueError as error:
                print(f"Could not register: {error}")

        elif choice == "2":
            member_id = input("Your member ID: ")
            title = input("Book title: ")
            author = input("Author: ")
            condition = input("Condition (new/good/fair): ").lower()
            try:
                book = Book(title, author, condition)
                balance = library.donate(book, member_id)
                print(f"Thank you! You earned "
                      f"{book.points_value} points.")
                print(f"New balance: {balance} points.")
            except ValueError as error:
                print(f"Could not donate: {error}")

        elif choice == "3":
            member_id = input("Your member ID: ")
            query = input("Search for a book to redeem: ")
            try:
                found = library.search(query)
                if not found:
                    print("No matching books right now.")
                    continue
                for index, book in enumerate(found, start=1):
                    print(f"{index}) {book.title} - {book.author} "
                          f"({book.points_value} points)")
                pick = int(input("Which one? (number): ")) - 1
                balance = library.redeem(found[pick], member_id)
                print(f"Enjoy your book! Remaining balance: {balance}.")
            except (ValueError, IndexError) as error:
                print(f"Could not redeem: {error}")

        elif choice == "4":
            query = input("Search for: ")
            try:
                for book in library.search(query):
                    print(f"- {book.title} by {book.author} "
                          f"({book.condition})")
            except ValueError as error:
                print(f"Could not search: {error}")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Please choose 1-5.")


if __name__ == "__main__":
    main()