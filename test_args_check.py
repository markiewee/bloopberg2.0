import pytest
from datetime import datetime
import pandas_market_calendars as mcal
from args_check import ArgsCheck

def test_date_check_valid():
    # Test valid date inputs
    result = ArgsCheck.date_check("20200101", "20201231")
    assert result == 1

def test_date_check_invalid_format():
    # Test invalid date format
    with pytest.raises(SystemExit):
        ArgsCheck.date_check("2020-01-01", "2020-12-31")

def test_date_check_start_after_end():
    # Test start date after end date
    with pytest.raises(SystemExit):
        ArgsCheck.date_check("20201231", "20200101")

def test_date_check_future_start_date():
    # Test start date in the future
    future_start_date = (datetime.today() + timedelta(days=10)).strftime('%Y%m%d')
    with pytest.raises(SystemExit):
        ArgsCheck.date_check(future_start_date, "20991231")

def test_aum_check_valid():
    # Test valid AUM value
    ArgsCheck.aum_check(1000)

def test_aum_check_invalid():
    # Test invalid AUM value
    with pytest.raises(SystemExit):
        ArgsCheck.aum_check(-1000)

def test_strategy_check_valid_momentum():
    # Test valid momentum strategy input
    ArgsCheck.strategy_check("M")

def test_strategy_check_valid_reversal():
    # Test valid reversal strategy input
    ArgsCheck.strategy_check("R")

def test_strategy_check_invalid():
    # Test invalid strategy input
    with pytest.raises(SystemExit):
        ArgsCheck.strategy_check("InvalidStrategy")
