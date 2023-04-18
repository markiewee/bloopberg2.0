import sys
import pytest
import pandas as pd
import numpy as np
import math
sys.path.append('../')
from getdata import Getdata
"""
Tests methods from the Getdata class, including checking that data from yfinance's API 
is accurate.

In the actual program, inputs to Getdata used for initializing a Getdata object 
will be tested by ArgsCheck. So we can assume here that the inputs are all valid.
"""
def test_getdata_ticker():
    """
    Checks that every single element in the dataframe downloaded through the yfinance api 
    is very close (at most 0.01% rounding difference) to what we previously downloaded 
    before into our own database. 

    Checks that yfinance is working well for AAPL from 2020/01/01 to 2021/02/03.
    """
    output = True #Set output to true first
    expected = pd.read_csv('getdata_aapl.csv', index_col = 0)
    try:
        #This should only fail if the api isn't working
        downloaded_data = Getdata('20200101', '20210203', 'AAPL').data
        col_names = expected.columns
        for k in range(len(col_names)):
            list_1 = expected[col_names[k]].values
            list_2 = downloaded_data[col_names[k]].values
            for i in range(len(list_1)):
                #Use the math isclose function because of float rounding error
                if not math.isclose(list_1[i], list_2[i], rel_tol= 0.0001):
                    output = False
    except: 
        #If we failed to downloaded the data from yfinance, then this test should fail.
        output = False
    assert output == True

def test_getdata_etf():
    """
    Checks that every single element in the dataframe downloaded through the yfinance api 
    is very close (at most 0.01% rounding difference) to what we previously downloaded 
    before into our own database. 

    Checks that yfinance is working well for SPY from a wide range of 1980/01/01 to 2023/02/03.
    """
    output = True #Set output to true first
    expected = pd.read_csv('getdata_spy.csv', index_col = 0)
    try:
        #This should only fail if the api isn't working
        downloaded_data = Getdata('19800101', '20230203', 'SPY').data
        col_names = expected.columns
        for k in range(len(col_names)):
            list_1 = expected[col_names[k]].values
            list_2 = downloaded_data[col_names[k]].values
            for i in range(len(list_1)):
                #Use the math isclose function because of float rounding error
                if not math.isclose(list_1[i], list_2[i], rel_tol= 0.0001):
                    output = False
    except: 
        #If we failed to downloaded the data from yfinance, then this test should fail.
        output = False
    assert output == True

def test_buy_sell_dates():
    """
    We have a list of expected end trading dates for a certain period.

    This function compares that list to what we get from Getdata.
    """
    expected = ['2020-01-31 00:00:00', 
                '2020-02-28 00:00:00', 
                '2020-03-31 00:00:00', 
                '2020-04-30 00:00:00', 
                '2020-05-29 00:00:00', 
                '2020-06-30 00:00:00', 
                '2020-07-31 00:00:00', 
                '2020-08-31 00:00:00', 
                '2020-09-30 00:00:00', 
                '2020-10-30 00:00:00', 
                '2020-11-30 00:00:00', 
                '2020-12-31 00:00:00', 
                '2021-01-29 00:00:00', 
                '2021-02-02 00:00:00']
    downloaded = Getdata('20200101', '20210203', 'MSFT').buy_sell_dates()
    assert expected == [str(i) for i in downloaded]

def test_get_first_last_trading_days():
    """
    Uses sample AAPL data downloaded and compares to see that first and 
    last trading days are correctly extracted.
    """
    expected = ['2020-01-02 00:00:00', '2021-02-02 00:00:00']
    downloaded = Getdata('20200101', '20210203', 'AAPL').get_first_last_trading_days()
    assert expected == [str(i) for i in downloaded]