import yfinance as yf
import pandas as pd
from datetime import datetime
from datetime import timedelta
from parseargs import Parseargs
from getdata import Getdata
import math

class Strategy:
    def __init__(self, tickers, start_date, end_date, days, strategy, top_pct):
        self.tickers = tickers
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.days = days
        self.top_pct = top_pct

    def calc_top_pct(self):
        top_n = int(self.top_pct * len(self.tickers))
        return top_n
    
    def compute_top_stocks (self):
        """
        Computes the number of top stocks based on top_pct and rounds up to nearest integer.
        """
        num_stocks = len(self.tickers)#number of stocks in the list
        num_top_stocks = math.ceil(num_stocks * self.top_pct / 100)#number of top stocks based on top_pct and rounded up to nearest integer
        return num_top_stocks

    def get_data_for_all_tickers(self, start_date):
        all_data = {}
        start_date = self.start_date - timedelta(days=365)
        for ticker in self.tickers:
            data_obj = Getdata(start_date, self.end_date, ticker)
            data_df = data_obj.getdata()
            all_data[ticker] = data_df
        return all_data

    def calculate_returns(self):
        all_data = self.get_data_for_all_tickers()
        returns = {}
        for ticker, data in all_data.items():
            start_price = data.iloc[0]['Close']
            end_price = data.iloc[-1]['Close']
            stock_return = (end_price - start_price) / start_price
            returns[ticker] = stock_return
        return returns

    def momentum(self):
        returns = self.calculate_returns()
        sorted_returns = sorted(returns.items(), key=lambda item: item[1], reverse=True)
        top_n = int(self.top_pct * len(self.tickers))
        top_momentum_stocks = [item[0] for item in sorted_returns[:top_n]]
        return top_momentum_stocks

    def reversal(self):
        returns = self.calculate_returns()
        sorted_returns = sorted(returns.items(), key=lambda item: item[1])
        top_n = int(self.top_pct * len(self.tickers))
        top_reversal_stocks = [item[0] for item in sorted_returns[:top_n]]
        return top_reversal_stocks

if __name__ == '__main__':
    tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'FB', 'TSLA', 'BRK-B', 'JPM', 'JNJ', 'V']
    strategy = 'momentum'
    start_date = '20200101'
    end_date = '20201231'
    top_pct = 0.4

    strategy_obj = Strategy(tickers, start_date, end_date, strategy, top_pct)

    if strategy == 'momentum':
        top_momentum_stocks = strategy_obj.momentum()
        print("Top momentum stocks:", top_momentum_stocks)
    elif strategy == 'reversal':
        top_reversal_stocks = strategy_obj.reversal()
        print("Top reversal stocks:", top_reversal_stocks)
