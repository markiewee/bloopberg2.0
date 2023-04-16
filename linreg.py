import yfinance as yf
import pandas as pd
from datetime import datetime
from datetime import timedelta
from parseargs import Parseargs
from getdata import Getdata
import math

class Linreg:
    def __init__(self, tickers, start_date, end_date, days, strategy, top_pct):
        self.tickers = tickers
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.days = days
        self.top_pct = top_pct

    def get_data_for_all_tickers(self, start_date):
        all_data = {}
        #convert start_date to datetime object
        start_date = datetime.strptime(self.start_date, "%m%d%Y")
        data_start_date = start_date - timedelta(days=365)
        for ticker in self.tickers:
            data_obj = Getdata(data_start_date, self.end_date, ticker)
            data_df = data_obj.getdata()
            all_data[ticker] = data_df
        return all_data

    def print_all_data(self):
        all_data = self.get_data_for_all_tickers(self.start_date)
        for ticker, data in all_data.items():
            print(f"\nTicker: {ticker}")
            print(data)

# Test the print_all_data method
tickers = ["AAPL", "GOOG"]
start_date = "01012020"
end_date = "02022022"
days = 365
strategy = "test_strategy"
top_pct = 0.1

linreg = Linreg(tickers, start_date, end_date, days, strategy, top_pct)
linreg.print_all_data()


