class Transaction:
    """
    A class representing a single transaction of a dataset.
    """

    offset: int = 0
    prefix_utility: int = 0

    def __init__(self, items: list, trans_utility: int, utilities: list) -> None:
        self.items: list = items
        self.transaction_utility: int = trans_utility
        self.utilities: list = utilities

    def __repr__(self) -> str:
        return f"Transaction({self.items}, {self.transaction_utility}, {self.utilities})"

    def rename_items(self, old_names_to_new_name: dict) -> None:
        """This method renames items from their old name to the new name obtained by the sort method"""
        temp_items = []
        temp_utilities = []

        for idx, item in enumerate(self.items):
            temp_items.append(old_names_to_new_name[item])
            temp_utilities.append(self.utilities[idx])

        self.items = temp_items
        self.utilities = temp_utilities

        # Sort by increasing values
        self.insertion_sort()

    def remove_unpromising_items(self, promising_items: list) -> None:
        """This method removes unpromising items from the transaction."""
        temp_items = []
        temp_utilities = []

        for idx, item in enumerate(self.items[self.offset:]):
            # if the item is promising, we keep it and its utility,
            # otherwise we subtract its utility from the transaction utility
            if item in promising_items:
                temp_items.append(item)
                temp_utilities.append(self.utilities[idx+self.offset])
            else:
                self.transaction_utility -= self.utilities[idx+self.offset]

        self.items = temp_items
        self.utilities = temp_utilities

        self.offset = 0

    def insertion_sort(self) -> None:
        """Sorts the items of the transaction by increasing order values (obtained by the sort method)."""
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

    def project_transaction(self, offset_e: int):
        """Creates a new Transaction from this transaction starting from offset until the end."""
        new_transaction = Transaction(self.items, self.transaction_utility, self.utilities)
        utility_e = self.utilities[offset_e]

        # Add the  utility of item e to the utility of the whole prefix used to project the transaction
        new_transaction.prefix_utility = self.prefix_utility + utility_e

        # Calculate the remaining utility.
        # It is the transaction utility minus the profit of the element that was removed
        new_transaction.transaction_utility = self.transaction_utility - utility_e
        # Subtract the utility of all items before e but after the previous offset
        for i in range(self.offset, offset_e):
            new_transaction.transaction_utility -= self.utilities[i]

        new_transaction.offset = offset_e + 1

        return new_transaction
