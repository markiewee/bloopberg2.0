import sys
import pytest
sys.path.append('../')
from args_check import ArgsCheck
"""
Tests methods in the ArgsCheck class to make sure that they are robust enough
to detect wrong inputs passed by the user into parseargs.
"""
def test_ticker_check_none():
    #Check that system exits if no ticker provided.
    with pytest.raises(SystemExit) as sample:
        ArgsCheck.ticker_check(None)
    assert sample.type == SystemExit
    assert sample.value.code == "Error: Please provide at least one ticker."

def test_ticker_check_one():
    #Check that the ticker check works for one ticker
    output = ArgsCheck.ticker_check(['AAPL'])
    assert output == None

def test_ticker_check_multiple():
    #Check that the ticker check works for multiple tickers
    output = ArgsCheck.ticker_check(['AAPL', 'GOOG', 'HBT'])
    assert output == None

def test_aum_check_none():
    #Check that a system exit is raised when no ticker was provided.
    with pytest.raises(SystemExit) as sample:
        ArgsCheck.aum_check(None)
    assert sample.type == SystemExit

def test_aum_check_negative():
    #Check that a system exit is raised when provided AUM is negative.
    with pytest.raises(SystemExit) as sample:
        ArgsCheck.aum_check(-80)
    assert sample.type == SystemExit

def test_aum_check_zero():
    #Check that a system exit is raised when provided AUM is 0.
    with pytest.raises(SystemExit) as sample:
        ArgsCheck.aum_check(0)
    assert sample.type == SystemExit

def test_aum_check_float():
    #Check that our program accepts float AUM input.
    output = ArgsCheck.aum_check(1000.5)
    assert output == None

def test_aum_check_int():
    #Check that our program accepts whole number positive AUM.
    for i in range(1, 100000):
        #Test from range 1 to 100000
        output = ArgsCheck.aum_check(i)
        assert output == None

def test_date_check_future():
    #Check that program exits gracefully when future dates are provided. 
    date1 = '20800101'
    date2 = '20900101'
    with pytest.raises(SystemExit) as sample:
        ArgsCheck.date_check(date1, date2)
    assert sample.type == SystemExit
    assert sample.value.code == 'Error: Start date is in the future.'

def test_date_check_start_after_end():
    #Check that program exits gracefully when start date is after end date. 
    date1 = '20000101'
    date2 = '19980101'
    with pytest.raises(SystemExit) as sample:
        ArgsCheck.date_check(date1, date2)
    assert sample.type == SystemExit
    assert sample.value.code == 'Error: Start date after end date. Enter a start date before or equal to the end date.'

def test_date_check_format():
    #Check that program exits gracefully when dates are in wrong format. 
    date1 = '1996/01/01'
    date2 = '1998/01/01'
    with pytest.raises(SystemExit) as sample:
        ArgsCheck.date_check(date1, date2)
    assert sample.type == SystemExit
    assert sample.value.code == 'Error: Dates entered in invalid format.'

def test_date_check_format_2():
    #Check that program exits gracefully when dates are in wrong format. 
    date1 = '1996-01-01'
    date2 = '1998-01-01'
    with pytest.raises(SystemExit) as sample:
        ArgsCheck.date_check(date1, date2)
    assert sample.type == SystemExit
    assert sample.value.code == 'Error: Dates entered in invalid format.'

def test_date_check_format_3():
    #Check that program exits gracefully when dates are in wrong format. 
    date1 = '01-01-2003'
    date2 = '01-01-2006'
    with pytest.raises(SystemExit) as sample:
        ArgsCheck.date_check(date1, date2)
    assert sample.type == SystemExit
    assert sample.value.code == 'Error: Dates entered in invalid format.'

def test_date_check_no_input():
    #Check that program exits gracefully when user did not provide any dates. 
    date1 = None
    date2 = None
    with pytest.raises(SystemExit) as sample:
        ArgsCheck.date_check(date1, date2)
    assert sample.type == SystemExit
    assert sample.value.code == 'Error: No beginning or end date provided.'

def test_date_check_no_valid_day():
    #Check that program exits gracefully when there are no valid trading days in the period provided. 
    date1 = '20230101'
    date2 = '20230101'
    with pytest.raises(SystemExit) as sample:
        ArgsCheck.date_check(date1, date2)
    assert sample.type == SystemExit
    assert sample.value.code == 'Error: No trading days found for specified period.'

def test_date_check_normal():
    #Check that program works with a typical set of dates. 
    date1 = '20230203'
    date2 = '20230303'
    output = ArgsCheck.date_check(date1, date2)
    assert output == 1