import pytest
from argparse import ArgumentError
from my_module import ParseArgs


class TestParseArgs:
    @staticmethod
    def test_parse_arguments():
        # Test valid arguments
        sys_argv = ['--tickers', 'AAPL,MSFT,KO', '--b', '20220101', '--e', '20220301', '--initial_aum', '100000',
                    '--strategy1_type', 'M', '--strategy2_type', 'R', '--days1', '10', '--days2', '20', '--top_pct', '20']
        parser = ParseArgs()
        assert parser.parse_arguments() == [['AAPL', 'MSFT', 'KO'], '20220101', '20220301', 100000, 'M', 'R', 10, 20, 20]

        # Test missing required argument
        sys_argv = ['--tickers', 'AAPL,MSFT,KO', '--e', '20220301', '--initial_aum', '100000',
                    '--strategy1_type', 'M', '--strategy2_type', 'R', '--days1', '10', '--days2', '20', '--top_pct', '20']
        parser = ParseArgs()
        with pytest.raises(ArgumentError):
            parser.parse_arguments()

        # Test invalid argument
        sys_argv = ['--tickers', 'AAPL,MSFT,KO', '--b', '20220101', '--e', '20220301', '--initial_aum', '100000',
                    '--strategy1_type', 'M', '--strategy2_type', 'X', '--days1', '10', '--days2', '20', '--top_pct', '20']
        parser = ParseArgs()
        with pytest.raises(SystemExit):
            parser.parse_arguments()
