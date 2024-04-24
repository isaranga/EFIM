from Transaction import Transaction


class Dataset:
    """
    A class representing a list of transactions of a dataset.
    """

    def __init__(self, input_file: str, sep: str = " ") -> None:
        self.input_file: str = input_file
        self.sep: str = sep

        self.transactions: list = []
        self.str_to_int: dict = {}
        self.int_to_str: dict = {}
        self.cnt: int = 1
        self.max_item: int = 0

        self.create_itemsets(self.input_file)

    def __repr__(self) -> str:
        return f"Dataset({len(self.transactions)} transactions, {len(self.str_to_int)} items, max item={self.max_item})"

    def create_itemsets(self, input_file) -> None:
        """Stores the complete transactions of the database/input file in a database variable."""
        self.transactions = []
        with open(input_file, "r") as file:
            for line in file:
                if line.startswith('#'):
                    continue
                trans_list = line.strip().split(':')
                items_string = trans_list[0].strip().split(self.sep)
                trans_utility = int(trans_list[1])
                utility_string = trans_list[2].strip().split(self.sep)
                transaction = self.create_transaction(items_string, trans_utility, utility_string)
                self.transactions.append(transaction)

    def create_transaction(self, items_string, trans_utility, utility_string) -> Transaction:
        """Creates a transaction object."""
        items = []
        utilities = []

        for idx, item in enumerate(items_string):
            if item not in self.str_to_int:
                self.str_to_int[item] = self.cnt
                self.int_to_str[self.cnt] = item
                self.cnt += 1

            item_int = self.str_to_int[item]

            if item_int > self.max_item:
                self.max_item = item_int

            items.append(item_int)
            utilities.append(int(utility_string[idx]))

        return Transaction(items, trans_utility, utilities)
