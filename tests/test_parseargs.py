from argparse import Namespace
import sys
import pytest
sys.path.append('../')
from parse_args import Parseargs
"""
Tests that arguments passed in are parsed correctly.

In the actual program, arguments are also tested to see whether they are valid.
We test that the functions from args_check are working correctly in the 
test_args_check.py file.
"""
def test_parse_arguments_two():
    #Tests that arguments are parsed correctly with 2 tickers provided.
    args = Namespace()
    args.tickers = ['AAPL', 'GOOG']
    args.b = '20220101'
    args.e = '20220301'
    args.initial_aum = 100000
    args.strategy_type = 'M'
    args.days = 30
    args.top_pct = 20
    parser = Parseargs()
    expected = [['AAPL', 'GOOG'], '20220101', '20220301', 100000.0, 'M', 30, 20]
    actual = parser.parse_arguments(args)
    assert actual == expected

def test_parse_arguments_one_ticker():
    #Tests that arguments are parsed correctly with 1 ticker provided. 
    args = Namespace()
    args.tickers = ['KO']
    args.b = '20220101'
    args.e = '20220301'
    args.initial_aum = 100000
    args.strategy_type = 'M'
    args.days = 30
    args.top_pct = 20
    parser = Parseargs()
    expected = [['KO'], '20220101', '20220301', 100000.0, 'M', 30, 20]
    actual = parser.parse_arguments(args)
    assert actual == expected

