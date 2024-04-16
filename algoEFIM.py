import argparse
import time
from typing import Union

from Dataset import Dataset


class EFIM:
    def __init__(self, input_file: str, min_util: int, sep: str = " ") -> None:
        self.input_file: str = input_file
        self.min_util: int = min_util
        self.sep: str = sep

        self._start_time: float = 0.0
        self._dataset: Union[Dataset, None] = None
        self._utility_bin_array_LU: dict = {}

    def run(self) -> None:
        """Starts the EFIM algorithm."""
        self._start_time = time.time()
        self._dataset = Dataset(self.input_file, self.sep)

        self.calculate_local_utilities(self._dataset)   # line 2 of Algorithm 1

    def calculate_local_utilities(self, dataset: Dataset) -> None:
        """Calculates the local utilities of all items in the dataset by using utility-bin array."""
        for transaction in dataset.transactions:
            for item in transaction.items:
                if item in self._utility_bin_array_LU:
                    self._utility_bin_array_LU[item] += transaction.transaction_utility
                else:
                    self._utility_bin_array_LU[item] = transaction.transaction_utility


def parse_arguments():
    """Parses the commandline arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file", help="The input file containing the transactions.")
    parser.add_argument("--min_utility", help="The minimum utility threshold.")
    parser.add_argument("--sep", help="The separator used in the input file.", default=" ")

    return parser.parse_args()


if __name__ == '__main__':
    # Commandline arguments parsing
    args = parse_arguments()

    input_file = args.input_file
    min_utility = int(args.min_utility)
    sep = args.sep

    # Run the EFIM algorithm
    efim = EFIM(input_file, min_utility, sep)
    efim.run()
