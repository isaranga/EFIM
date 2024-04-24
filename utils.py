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
            print(f"\rHandling line {i}/{num_lines}", end='')
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

    output_filename = f'{file_name.split(".")[0]}_con.ds'
    with open(output_filename, "w") as f:
        for i, transaction in enumerate(transactions):
            print(f"\rWriting line {i}/{num_lines}", end='')
            if i == num_lines-1:
                transaction = transaction[:-2]  # avoid last row \n
            f.write(transaction)


if __name__ == '__main__':
    convert_to_efim_format("dataset/bms.ds")
