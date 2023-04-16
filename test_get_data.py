import pytest
import yfinance as yf
import pandas as pd
from datetime import datetime
from getdata import Getdata

@pytest.fixture
def data_obj():
    return Getdata("20200101", "20201231", "AAPL")

# Test if the Getdata class initializes with the correct attributes.
def test_init(data_obj):
    assert data_obj.start_date == datetime.strptime("20200101", '%Y%m%d')
    assert data_obj.end_date == datetime.strptime("20201231", '%Y%m%d')
    assert data_obj.ticker == "AAPL"

# Test if the getdata method returns a DataFrame with data within the specified date range.
def test_getdata(data_obj):
    data = data_obj.getdata()
    assert isinstance(data, pd.DataFrame)
    assert data.index[0] >= data_obj.start_date
    assert data.index[-1] <= data_obj.end_date

# Test if the buy_sell_dates method returns a list of last trading days of each month within the specified date range.
def test_buy_sell_dates(data_obj):
    monthly_final_trading_days = data_obj.buy_sell_dates()
    assert isinstance(monthly_final_trading_days, list)
    assert all(isinstance(date, pd.Timestamp) for date in monthly_final_trading_days)

# Test if the get_first_last_trading_days method returns a list containing the first and last trading days within the specified date range.
def test_get_first_last_trading_days(data_obj):
    first_last_trading_days = data_obj.get_first_last_trading_days()
    assert isinstance(first_last_trading_days, list)
    assert len(first_last_trading_days) == 2
    assert isinstance(first_last_trading_days[0], pd.Timestamp)
    assert isinstance(first_last_trading_days[1], pd.Timestamp)
