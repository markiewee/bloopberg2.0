import pytest
import pandas as pd
import numpy as np
from stock_strategy import StockStrategy
from regression_strategy import RegressionStrategy

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

def test_regression_strategy(sample_stock_data):
    stock_strategy = StockStrategy('2020-01-01', '2021-12-31', sample_stock_data)
    momentum_list = stock_strategy.calculate_momentum()
    reversal_list = stock_strategy.calculate_reversal()

    regression_strategy = RegressionStrategy(momentum_list, reversal_list, 50)
    top_stocks_history = regression_strategy.perform_strategy()

    assert len(top_stocks_history) > 0
    for month, top_stocks in top_stocks_history:
        assert len(top_stocks) <= len(sample_stock_data) // 2
