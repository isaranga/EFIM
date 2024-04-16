import argparse


class EFIM:
    def __init__(self, input_file: str, min_util: int, sep: str = " ") -> None:
        self.input_file = input_file
        self.min_util = min_util
        self.sep = sep


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
