import argparse
from args_check import ArgsCheck

class Parseargs:
    """
    A class which parses the arguments passed into a program.
    """
    def __init__(self):
        """
        Requires the following arguments:
        --tickers: Space separated list of tickers e.g. AAPL MSFT KO
        --b: Beginning date in YYYYMMDD format
        --e: End date in YYYYMMDD format
        --initial_aum: A number > 0. e.g. 1000
        --strategy_type: M or R
        --days: Number of days to factor into backtesting.
        --top_pct: The percentage of stocks we want to consider as 'top' and buy at the end of a backtesting period.
        """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--tickers', nargs='+', type=str, help='list of tickers')
        self.parser.add_argument('--b', type=str, help='start date in YYYYMMDD format')
        self.parser.add_argument('--e', type=str, help='end date in YYYYMMDD format')
        self.parser.add_argument('--initial_aum', type=float, help='initial assets under management')
        self.parser.add_argument('--strategy_type', type=str, help='type of strategy')
        self.parser.add_argument('--days', type=int, help='number of days for calculation')
        self.parser.add_argument('--top_pct', type=int, help='top percentile for calculation')


    def parse_arguments(self, arguments = None):
        """
        Parses arguments and returns a list where arguments are in the following index order:
        0: tickers
        1: beginning date
        2: end date
        3: initial aum
        4: strategy type
        5: num days
        6: top pct
        """
        namespace_args = self.parser.parse_args(namespace = arguments)
        list_arguments = [namespace_args.tickers, 
                          namespace_args.b, 
                          namespace_args.e, 
                          namespace_args.initial_aum, 
                          namespace_args.strategy_type, 
                          namespace_args.days, 
                          namespace_args.top_pct]
        """
        Code below uses ArgsCheck from args_check.py
        to see if the arguments pass the tests.

        If the arguments do not pass the tests, an error message will be printed and the 
        program will exit.
        """
        ArgsCheck.ticker_check(list_arguments[0])
        ArgsCheck.date_check(list_arguments[1], list_arguments[2])
        ArgsCheck.aum_check(list_arguments[3])
        ArgsCheck.strategy_check(list_arguments[4])
        return list_arguments
    
if __name__ == '__main__':
    x = Parseargs()
    print(x.parse_arguments())