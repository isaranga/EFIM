from algoEFIM import EFIM
from algoEFIM import create_logger
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

if __name__ == '__main__':
    datasets = ['accidents',
                'bms',
                'chess',
                'connect',
                'foodmart',
                'mushroom',
                'chainstore',
                'pumsb',
                'kosarak']
    minutils = {'accidents': [17500, 20000, 22500, 25000, 27500],
                'bms': [2240, 2250, 2260, 2270, 2280],
                'chess': [350, 400, 450, 500, 550],
                'connect': [13000, 14000, 15000, 16000, 17000],
                'foodmart': [0.001, 1, 2, 2.5, 3],
                'mushroom': [80, 85, 90, 95, 100],
                'chainstore': [2000, 2500, 3000, 3500, 4000],
                'pumsb': [12100, 12200, 12300, 12400, 12500],
                'kosarak': [1100, 1200, 1300, 1400, 1500]}          # in thousands

    # Create a logger
    logger = create_logger(verbose=False)

    # Run the EFIM algorithm
    logger.info("Starting EFIM algorithm...")

    def run_efim():
        for dataset in datasets:
            for minutil in minutils[dataset]:
                for f_type in ['base', 'exp1', 'exp2']:
                    print(f"Run {dataset} {f_type} {minutil}")
                    input_file = f"dataset/{dataset}.ds"
                    sep = ' '
                    output_file = f"{dataset}.out"
                    output_file = output_file.rsplit('.', 1)[0] + f'_{f_type}.' + output_file.rsplit('.', 1)[1]
                    efim = EFIM(input_file, minutil*1000, sep, output_file, logger, f_type)
                    efim.run()
                    efim.print_results(f_type=f_type)

    def analyse():
        stat_file = 'output/output.stat'
        df = pd.read_csv(stat_file, sep="\t\t", engine="python")
        fig, axs = plt.subplots(3, 3, figsize=(12, 12))
        for idx, dataset in enumerate(df["Dataset"].apply(lambda x: x.split('_')[0]).unique()):
            i, j = int(idx / 3), idx % 3
            for f_type, marker, color in zip(['base', 'exp1', 'exp2'], ['o', '^', 's'], ["blue", "orange", "green"]):
                x = df["Minutil"].where(df["Dataset"] == f"{dataset}_{f_type}").dropna()
                y_runtime = df["Time"].where(df["Dataset"] == f"{dataset}_{f_type}").dropna()
                y_nodes = df["Nodes"].where(df["Dataset"] == f"{dataset}_{f_type}").dropna()

                # Choose y_runtime or y_nodes
                axs[i, j].plot(x, y_nodes, label=f_type, marker=marker, color=color, alpha=1)
                axs[i, j].set_xticks(x)

            axs[i, j].set_title(f"{dataset}")
            axs[i, j].legend()
            # axs[i, j].set_yscale('log')
            axs[i, j].set_xlabel("Minutil")
            # Choose "Runtime (s)" or "Visited Nodes"
            axs[i, j].set_ylabel("Visited Nodes")

            if dataset != "foodmart":
                axs[i, j].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x / 1000)}K'))

        plt.tight_layout()
        plt.show()

    analyse()
