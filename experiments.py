from algoEFIM import EFIM
from algoEFIM import create_logger

if __name__ == '__main__':
    datasets = [#'accidents',
                #'bms',
                #'chess',
                'connect',
                'foodmart',
                'mushroom',
                'chainstore',
                'pumnsb',
                'kosarak']
    minutils = {'accidents': [17500, 20000, 22500, 25000, 27500],
                'bms': [2240, 2250, 2260, 2270, 2280],
                'chess': [350, 400, 450, 500, 550],
                'connect': [13000, 14000, 15000, 16000, 17000],
                'foodmart': [0.001, 1, 2, 2.5, 3],
                'mushroom': [80, 85, 90, 95, 100],
                'chainstore': [2000, 2500, 3000, 3500, 4000],
                'pumnsb': [12100, 12200, 12300, 12400, 12500],
                'kosarak': [1100, 1200, 1300, 1400, 1500]}          # in thousands

    # Create a logger
    logger = create_logger(verbose=False)

    # Run the EFIM algorithm
    logger.info("Starting EFIM algorithm...")

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
