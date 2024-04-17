import argparse
import functools
import logging
import sys
import time
from typing import Union

from Dataset import Dataset
from Transaction import Transaction


class EFIM:
    def __init__(self, input_file: str, min_util: int, sep: str = " ") -> None:
        self.input_file: str = input_file
        self.min_util: int = min_util
        self.sep: str = sep

        self._start_time: float = 0.0
        self._dataset: Union[Dataset, None] = None
        self._utility_bin_array_LU: dict = {}
        self._utility_bin_array_SU: dict = {}
        self._old_names_to_new_names: dict = {}
        self._new_names_to_old_names: dict = {}

    def run(self) -> None:
        """Starts the EFIM algorithm."""
        self._start_time = time.time()
        self._dataset = Dataset(self.input_file, self.sep)

        self.calculate_local_utilities(self._dataset)  # line 2 of Algorithm 1
        logger.info(f"Local utilities: {self._utility_bin_array_LU}")

        # secondary holds the promising items (those having a TWU >= minutil)
        secondary = [item for item in self._utility_bin_array_LU if self._utility_bin_array_LU[item] >= self.min_util]
        # Sort by the total order of TWU ascending values (line 4 of Algorithm 1)
        secondary = sorted(secondary, key=lambda x: self._utility_bin_array_LU[x])
        logger.info(f"Secondary (sorted by TWU): {secondary}")

        self.rename_promising_items(secondary)

        for transaction in self._dataset.transactions:
            transaction.remove_unpromising_items(self._old_names_to_new_names)

        logger.info(f"Transactions after removing unpromising items: {self._dataset.transactions}")

        self.sort_dataset(self._dataset.transactions)
        logger.info(f"Transactions after sorting: {self._dataset.transactions}")

        # Remove empty transactions
        empty_transactions_count = len([transaction for transaction in self._dataset.transactions
                                        if not transaction.items])
        # To remove empty transactions, we just ignore the first transactions of the dataset, since transactions
        # are sorted by size and therefore empty transactions are always at the begining of the dataset
        self._dataset.transactions = self._dataset.transactions[empty_transactions_count:]
        logger.info(f"{empty_transactions_count} empty transactions removed.")

        # Calculate the subtree utility of each item in secondary using a utility-bin array
        self.calculate_subtree_utility(self._dataset)
        logger.info(f"Subtree utilities: {self._utility_bin_array_SU}")

        # primary holds items in secondary that have a subtree utility >= minutil
        primary = [item for item in secondary if self._utility_bin_array_SU[item] >= self.min_util]
        logger.info(f"Primary: {primary}")

    def rename_promising_items(self, secondary):
        """Rename promising items according to the increasing order of TWU.
        This will allow very fast comparison between items later by the algorithm
        We will give the new names starting from the name '1'."""
        current_name = 1
        for idx, item in enumerate(secondary):
            self._old_names_to_new_names[item] = current_name
            self._new_names_to_old_names[current_name] = item
            secondary[idx] = current_name
            current_name += 1

    def calculate_local_utilities(self, dataset: Dataset) -> None:
        """Calculates the local utilities of all items in the dataset by using utility-bin array."""
        for transaction in dataset.transactions:
            for item in transaction.items:
                if item in self._utility_bin_array_LU:
                    self._utility_bin_array_LU[item] += transaction.transaction_utility
                else:
                    self._utility_bin_array_LU[item] = transaction.transaction_utility

    def sort_dataset(self, transactions: list) -> None:
        cmp_items = functools.cmp_to_key(self.compare_transaction)
        transactions.sort(key=cmp_items)

    @staticmethod
    def compare_transaction(trans1: Transaction, trans2: Transaction) -> int:
        """Compares two transactions according to the proposed total order on transaction (the lexicographical
        order when transactions are read backward)"""
        # we will compare the two transaction item by item starting from the last items
        trans1_items = trans1.items
        trans2_items = trans2.items
        pos1 = len(trans1_items) - 1
        pos2 = len(trans2_items) - 1

        if len(trans1_items) < len(trans2_items):
            while pos1 >= 0:
                diff = trans2_items[pos2] - trans1_items[pos1]
                if diff != 0:
                    return diff
                pos1 -= 1
                pos2 -= 1
            return -1

        elif len(trans1_items) > len(trans2_items):
            while pos2 >= 0:
                diff = trans2_items[pos2] - trans1_items[pos1]
                if diff != 0:
                    return diff
                pos1 -= 1
                pos2 -= 1
            return 1

        else:
            while pos2 >= 0:
                diff = trans2_items[pos2] - trans1_items[pos1]
                if diff != 0:
                    return diff
                pos1 -= 1
                pos2 -= 1
            return 0

    def calculate_subtree_utility(self, dataset: Dataset) -> None:
        """Scan the initial dataset to calculate the subtree utility of each item using a utility-bin array"""
        for transaction in dataset.transactions:
            # We will scan the transaction backwards. Thus, the current subtree utility in that transaction is zero
            # for the last item of the transaction.
            sum_SU: int = 0

            i = len(transaction.items) - 1
            while i >= 0:
                item = transaction.items[i]
                sum_SU += transaction.utilities[i]
                if item in self._utility_bin_array_SU.keys():
                    self._utility_bin_array_SU[item] += sum_SU
                else:
                    self._utility_bin_array_SU[item] = sum_SU
                i -= 1


def parse_arguments():
    """Parses the commandline arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file", help="The input file containing the transactions.")
    parser.add_argument("--min_utility", help="The minimum utility threshold.")
    parser.add_argument("--sep", help="The separator used in the input file.", default=" ")
    parser.add_argument("--verbose", help="Prints the logs to stdout.", action="store_true")

    return parser.parse_args()


def create_logger() -> logging.Logger:
    """Creates a logger."""
    logger: logging.Logger = logging.getLogger(__name__)

    # log, and if verbose print the logs to stdout
    if args.verbose:
        try:
            logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='[%(asctime)s] %(message)s', force=True)
        except ValueError:
            # on colab we need to force config-ing, but locally it depened on the version of python
            logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='[%(asctime)s] %(message)s')

    return logger


if __name__ == '__main__':
    # Commandline arguments parsing
    args = parse_arguments()

    input_file = args.input_file
    min_utility = int(args.min_utility)
    sep = args.sep

    # Create a logger
    logger = create_logger()

    # Run the EFIM algorithm
    logger.info("Starting EFIM algorithm...")
    efim = EFIM(input_file, min_utility, sep)
    efim.run()

    logger.info("EFIM algorithm finished.")
