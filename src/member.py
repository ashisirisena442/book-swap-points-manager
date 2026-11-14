"""A library member who donates and redeems books."""


class Member:
    def __init__(self, name, member_id):
        name = name.strip()
        if not name:
            raise ValueError("Name cannot be empty.")
        self.name = name
        self.member_id = member_id
        self.points = 0
        self.donated = []   # books this member gave to the library
        self.redeemed = [] 
        self.borrowed = []  # books received from the library

    def earn(self, amount):
        if amount <= 0:
            raise ValueError("Earned points must be positive.")
        self.points += amount

    def spend(self, amount):
        if amount <= 0:
            raise ValueError("Spent points must be positive.")
        if amount > self.points:
            raise ValueError(
                f"Not enough points: has {self.points}, needs {amount}."
            )
        self.points -= amount

    def __repr__(self):
        return f"Member({self.name!r}, points={self.points})"