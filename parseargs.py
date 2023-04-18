import argparse
from args_check import ArgsCheck

class ParseArgs:
    """
    A class which parses the arguments passed into a program.
    """
    def __init__(self):
        """
        Requires the following arguments:
        --tickers: Comma-separated list of tickers e.g. AAPL,MSFT,KO
        --b: Beginning date in YYYYMMDD format (required)
        --e: End date in YYYYMMDD format (optional)
        --initial_aum: Initial amount of money to invest (required)
        --strategy1_type: M or R (momentum or reversal)
        --strategy2_type: M or R (momentum or reversal)
        --days1: Number of days for calculation for strategy1
        --days2: Number of days for calculation for strategy2
        --top_pct: The percentage of stocks we want to consider as 'top' and buy at the end of a backtesting period.
        """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--tickers', type=str, help='comma-separated list of tickers')
        self.parser.add_argument('--b', type=str, required=True, help='start date in YYYYMMDD format')
        self.parser.add_argument('--e', type=str, default=None, help='end date in YYYYMMDD format')
        self.parser.add_argument('--initial_aum', type=float, help='initial amount of money to invest')
        self.parser.add_argument('--strategy1_type', type=str, help='type of strategy 1')
        self.parser.add_argument('--strategy2_type', type=str, help='type of strategy 2')
        self.parser.add_argument('--days1', type=int, help='number of days for calculation for strategy1')
        self.parser.add_argument('--days2', type=int, help='number of days for calculation for strategy2')
        self.parser.add_argument('--top_pct', type=int, help='top percentile for calculation')

        list_arguments = self.parse_arguments()
        ArgsCheck.date_check(list_arguments[1], list_arguments[2])
        ArgsCheck.strategy_check(list_arguments[4])
        ArgsCheck.strategy_check(list_arguments[5])

    def parse_arguments(self):
        """
        Parses arguments and returns a list where arguments are in the following index order:
        0: tickers
        1: beginning date
        2: end date
        3: initial_aum
        4: strategy1_type
        5: strategy2_type
        6: days1
        7: days2
        8: top_pct
        """
        args = self.parser.parse_args()
        tickers = args.tickers.split(',')
        return [tickers, args.b, args.e, args.initial_aum, args.strategy1_type, args.strategy2_type, args.days1, args.days2, args.top_pct]

if __name__ == '__main__':
    parser = ParseArgs()
    list_arguments = parser.parse_arguments()
    ArgsCheck.date_check(list_arguments[1], list_arguments[2])
    ArgsCheck.strategy_check(list_arguments[4])
    ArgsCheck.strategy_check(list_arguments[5])
    print(list_arguments)

