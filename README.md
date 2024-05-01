Implementation of the EFIM algorithm.

```
usage: algoEFIM.py [-h] [--min_utility MIN_UTILITY] [--sep SEP] [--verbose] input_file <input_file> --output_file <output_file>

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
```algoEFIM.py example-Zida.txt --min_utility 30 --verbose --output_file output.txt ```

An easy-to-use notebook is attached to example a running of the algorithm.
To run this notebook make sure you run on google colab.
The notebook examples the run of one dataset: bms, as the others are taking too much time (run time in colab is longer than offline).
Download the dataset/bms.ds file and drop it into your notebook run folder.
Then, run the cells by their order.
