import sys
import pytest
sys.path.append('../')
from stock_strategy import Strategy

def test_compute_top_stocks_zero():
    x = Strategy(tickers = ['A', 'B', 'C', 'D', 'E'],
                 start_date = '19990101',
                 end_date = '20200101',
                 strategy = 'R',
                 days = 50,
                 top_pct = 0)
    expected = 0
    actual = x.compute_top_stocks(0)
    assert expected == actual

def test_compute_top_stocks_fifty():
    x = Strategy(tickers = ['A', 'B', 'C', 'D', 'E'],
                 start_date = '19990101',
                 end_date = '20200101',
                 strategy = 'R',
                 days = 50,
                 top_pct = 50)
    expected = 3
    actual = x.compute_top_stocks(50)
    assert expected == actual

def test_compute_top_stocks_all():
    x = Strategy(tickers = ['A', 'B', 'C', 'D', 'E'],
                 start_date = '19990101',
                 end_date = '20200101',
                 strategy = 'R',
                 days = 50,
                 top_pct = 100)
    expected = 5
    actual = x.compute_top_stocks(100)
    assert expected == actual

def test_calculate_returns():
    pass