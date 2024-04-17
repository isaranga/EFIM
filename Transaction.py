class Transaction:
    """
    A class representing a single transaction of a dataset.
    """

    offset: int = 0

    def __init__(self, items: list, trans_utility: int, utilities: list) -> None:
        self.items: list = items
        self.transaction_utility: int = trans_utility
        self.utilities: list = utilities

    def __repr__(self) -> str:
        return f"Transaction({self.items}, {self.transaction_utility}, {self.utilities})"

    def remove_unpromising_items(self, old_names_to_new_names: dict) -> None:
        """This method removes unpromising items from the transaction and at the same time rename items
        from old names to new names."""
        temp_items = []
        temp_utilities = []

        for idx, item in enumerate(self.items):
            # if the item is promising (it has a new name), then we keep it and its utility,
            # otherwise we subtract its utility from the transaction utility
            if item in old_names_to_new_names:
                temp_items.append(old_names_to_new_names[item])
                temp_utilities.append(self.utilities[idx])
            else:
                self.transaction_utility -= self.utilities[idx]

        self.items = temp_items
        self.utilities = temp_utilities

        # Sort by increasing TWU values
        self.insertion_sort()

    def insertion_sort(self) -> None:
        """Sorts the items of the transaction by increasing order of TWU values."""
        for i in range(1, len(self.items)):
            key = self.items[i]
            utility_j = self.utilities[i]
            j = i - 1

            while j >= 0 and key < self.items[j]:
                self.items[j + 1] = self.items[j]
                self.utilities[j + 1] = self.utilities[j]
                j -= 1

            self.items[j + 1] = key
            self.utilities[j + 1] = utility_j
