def convert_to_efim_format(file_name):
    """
    Convert to type:
    item_a item_b ... item_n:sum_util:util_a util_b ... util_n

    BMS original type:
    item_1 -1 item_2 -1 ... item_n -1 -2
    """
    transactions = []

    with open(file_name, 'r') as file:
        num_lines = len(file.readlines())

    with open(file_name, 'r') as file:
        for i, line in enumerate(file):
            print(f"\rHandling file {file_name} on line {i}/{num_lines}", end='')
            transaction = []
            if line.startswith('#'):
                continue
            for att in line.strip().split(" "):
                if att == '-1':
                    continue
                elif att == '-2':
                    break
                else:
                    transaction.append(str(att))

            transaction_str = f'{" ".join(transaction)}:{len(transaction)}:{" ".join(["1"]*len(transaction))}\n'
            transactions.append(transaction_str)

    output_filename = f'{file_name.split(".")[0]}.ds'
    with open(output_filename, "w") as f:
        for i, transaction in enumerate(transactions):
            print(f"\rWriting line {i}/{num_lines}", end='')
            if i == num_lines-1:
                transaction = transaction[:-1]  # avoid last row \n
            f.write(transaction)

def convert_to_efim_format_b(file_name):
    """
    Convert to type:
    item_a item_b ... item_n:sum_util:util_a util_b ... util_n

    Accidents original type:
    item_1 item_2 ... item_n
    """
    transactions = []

    with open(file_name, 'r') as file:
        num_lines = len(file.readlines())

    with open(file_name, 'r') as file:
        for i, line in enumerate(file):
            print(f"\rHandling file {file_name} on line {i}/{num_lines}", end='')
            transaction = []
            if line.startswith('#'):
                continue
            for att in line.strip().split(" "):
                transaction.append(str(att))

            transaction_str = f'{" ".join(transaction)}:{len(transaction)}:{" ".join(["1"]*len(transaction))}\n'
            transactions.append(transaction_str)

    output_filename = f'{file_name.split(".")[0]}.ds'
    with open(output_filename, "w") as f:
        for i, transaction in enumerate(transactions):
            print(f"\rWriting line {i}/{num_lines}", end='')
            if i == num_lines-1:
                transaction = transaction[:-1]  # avoid last row \n
            f.write(transaction)

def convert_to_efim_format_c(file_name):
    """
    Convert to type:
    item_a item_b ... item_n:sum_util:util_a util_b ... util_n

    Mushrooms original type:
    item_1 item_2 ... item_n:trans_utility:util_1 util_2 ... util_n:timestamp
    """
    transactions = []

    with open(file_name, 'r') as file:
        num_lines = len(file.readlines())

    with open(file_name, 'r') as file:
        for i, line in enumerate(file):
            print(f"\rHandling file {file_name} on line {i}/{num_lines}", end='')
            transaction = []
            if line.startswith('#'):
                continue

            transaction_str = line.rsplit(':', 1)[0]+'\n'
            transactions.append(transaction_str)

    output_filename = f'{file_name.split(".")[0]}.ds'
    with open(output_filename, "w") as f:
        for i, transaction in enumerate(transactions):
            print(f"\rWriting line {i}/{num_lines}", end='')
            if i == num_lines-1:
                transaction = transaction[:-1]  # avoid last row \n
            f.write(transaction)


if __name__ == '__main__':
    convert_to_efim_format_c("dataset/mushroom.txt")
