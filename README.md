Implementation of the EFIM algorithm.

```
usage: algoEFIM.py [-h] [--min_utility MIN_UTILITY] [--sep SEP] [--verbose] input_file

positional arguments:
  input_file            The input file containing the transactions.
  --output_file         Output file name for patterns found.
optional arguments:
  -h, --help            show this help message and exit
  --min_utility MIN_UTILITY
                        The minimum utility threshold.
  --sep SEP             The separator used in the input file.
  --verbose             Prints the logs to stdout.
```
For example:
```algoEFIM.py example-Zida.txt --min_utility 30 --verbose ```
