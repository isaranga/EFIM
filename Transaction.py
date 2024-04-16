class Transaction:
    """
    A class representing a single transaction of a dataset.
    """

    def __init__(self, items: list, trans_utility: int, utilities: list) -> None:
        self.items: list = items
        self.trans_utility: int = trans_utility
        self.utilities: list = utilities

    def __repr__(self) -> str:
        return f"Transaction({self.items}, {self.trans_utility}, {self.utilities})"
