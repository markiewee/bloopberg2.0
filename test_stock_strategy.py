import pytest
import pandas as pd
import numpy as np
from stock_strategy import StockStrategy

@pytest.fixture
def sample_stock_data():
    data = [
        pd.DataFrame({
            'date': pd.date_range('2020-01-01', '2021-12-31', freq='M'),
            'price': np.random.uniform(100, 200, 24),
            'dividend': np.random.uniform(0, 2, 24)
        }),
        pd.DataFrame({
            'date': pd.date_range('2020-01-01', '2021-12-31', freq='M'),
            'price': np.random.uniform(50, 100, 24),
            'dividend': np.random.uniform(0, 1, 24)
        }),
        pd.DataFrame({
            'date': pd.date_range('2020-01-01', '2021-12-31', freq='M'),
            'price': np.random.uniform(20, 50, 24),
            'dividend': np.random.uniform(0, 0.5, 24)
        })
    ]
    return data

def test_stock_strategy_initialization(sample_stock_data):
    strategy = StockStrategy('2020-01-01', '2021-12-31', sample_stock_data)
    assert strategy.start_date == pd.to_datetime('2020-01-01')
    assert strategy.end_date == pd.to_datetime('2021-12-31')
    assert strategy.stock_data_frames == sample_stock_data

def test_calculate_momentum(sample_stock_data):
    strategy = StockStrategy('2020-01-01', '2021-12-31', sample_stock_data)
    momentum_list = strategy.calculate_momentum()

    assert len(momentum_list) == len(sample_stock_data)
    for df in momentum_list:
        assert 'momentum' in df.columns
        assert 'return' in df.columns
        assert 'adjusted_price' in df.columns

def test_calculate_reversal(sample_stock_data):
    strategy = StockStrategy('2020-01-01', '2021-12-31', sample_stock_data)
    reversal_list = strategy.calculate_reversal()

    assert len(reversal_list) == len(sample_stock_data)
    for df in reversal_list:
        assert 'reversal' in df.columns
        assert 'return' in df.columns
        assert 'rolling_return' in df.columns
        assert 'adjusted_price' in df.columns

def test_select_top_stocks(sample_stock_data):
    strategy = StockStrategy('2020-01-01', '2021-12-31', sample_stock_data)
    momentum_list = strategy.calculate_momentum()
    top_stocks_list = strategy.select_top_stocks(momentum_list, 50)

    assert len(top_stocks_list) == len(sample_stock_data) // 2
