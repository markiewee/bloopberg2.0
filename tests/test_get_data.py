import pytest
from datetime import datetime
from getdata import Getdata


def test_init():
    start_date = '20200101'
    end_date = '20201231'
    ticker = 'DVN'
    data_obj = Getdata(start_date, end_date, ticker)

    assert data_obj.start_date == datetime.strptime(start_date, '%Y%m%d')
    assert data_obj.end_date == datetime.strptime(end_date, '%Y%m%d')
    assert data_obj.ticker == ticker


def test_getdata():
    start_date = '20200101'
    end_date = '20201231'
    ticker = 'DVN'
    data_obj = Getdata(start_date, end_date, ticker)
    data_df = data_obj.getdata()

    assert not data_df.empty
    assert 'Date' in data_df.columns
    assert 'Close' in data_df.columns
    assert 'Dividends' in data_df.columns


def test_buy_sell_dates():
    start_date = '20200101'
    end_date = '20201231'
    ticker = 'DVN'
    data_obj = Getdata(start_date, end_date, ticker)
    monthly_final_trading_days = data_obj.buy_sell_dates()

    assert len(monthly_final_trading_days) > 0
    assert isinstance(monthly_final_trading_days[0], pd.Timestamp)


def test_get_first_last_trading_days():
    start_date = '20200101'
    end_date = '20201231'
    ticker = 'DVN'
    data_obj = Getdata(start_date, end_date, ticker)
    first_last_trading_days = data_obj.get_first_last_trading_days()

    assert len(first_last_trading_days) == 2
    assert isinstance(first_last_trading_days[0], pd.Timestamp)
    assert isinstance(first_last_trading_days[1], pd.Timestamp)



