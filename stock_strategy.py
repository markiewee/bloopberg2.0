import yfinance as yf
import pandas as pd
from datetime import datetime
from datetime import timedelta
from parseargs import ParseArgs 
from getdata import Getdata
import math
import heapq

class Strategy:
    def __init__(self, tickers, start_date, end_date, days, strategy, top_pct):
        self.tickers = tickers
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.days = days
        self.top_pct = top_pct

    def compute_top_stocks (self, top_pct):
        self.top_pct = top_pct
        """
        Computes the number of top stocks based on top_pct and rounds up to nearest integer.
        """
        num_stocks = len(self.tickers)#number of stocks in the list
        num_top_stocks = math.ceil(num_stocks * self.top_pct / 100)#number of top stocks based on top_pct and rounded up to nearest integer
        return num_top_stocks

    def get_data_for_all_tickers(self, start_date, end_date, tickers):
        self.end_date = end_date
        self.tickers = tickers
        """
        Saves on runtime by calling API once per stock. 
        Calls API for each stock in the list of tickers with data_start_date being one year before actual start_date.
        Allows for maximum of 250 trading days for backtesting.
        
        Returns:
            all_data (dict): Dictionary of dataframes with ticker as key and dataframe as value.
        """
        all_data = {}
        start_date_datetime = datetime.strptime(start_date, '%Y%m%d')
        data_start_date = start_date_datetime - timedelta(days=400)
        for ticker in self.tickers:
            data_obj = Getdata(data_start_date.strftime('%Y%m%d'), self.end_date, ticker)
            data_df = data_obj.getdata()
            all_data[ticker] = data_df
        return all_data


    def calculate_returns(self, start_date, days, strategy, ticker_data, tickers):

        """
        identifies the proper date by using iloc to locate the row of the dataframe that corresponds to the start_date.
        moves back the correct number of days to get the backtest_start_date and backtest_end_date.
        ranks stocks in ascending order of returns as a dict with ticker as key and return as value."""

        backtest_returns = {}

        for ticker in tickers:
            df = ticker_data[ticker]
            start_date_row_number = df.loc[df['Date'] == start_date].index

            if len(start_date_row_number) == 0:
                print(f"Warning: No data found for {ticker} on {start_date}. Skipping...")
                continue
            else:
                start_date_row_number = start_date_row_number[0]

            

            if strategy == "M":
                backtest_start_date = df.loc[(start_date_row_number - days - 20), 'Date']
                backtest_end_date = df.loc[(start_date_row_number - 20), 'Date']
            elif strategy == "R":
                backtest_start_date = df.loc[(start_date_row_number - days), 'Date']
                backtest_end_date = df.loc[(start_date_row_number), 'Date']
            else:
                raise ValueError(f"Invalid strategy '{strategy}'. Strategy must be either 'M' or 'R'.")


            backtest_start_date_row_number = df.loc[df['Date'] == backtest_start_date].index.item()
            backtest_end_date_row_number = df.loc[df['Date'] == backtest_end_date].index.item()
            backtest_start_price = df.loc[(backtest_start_date_row_number), 'Close']
            backtest_end_price = df.loc[(backtest_end_date_row_number), 'Close']
            backtest_return = (backtest_end_price - backtest_start_price) / backtest_start_price

            backtest_returns[ticker] = backtest_return
        return backtest_returns


    def run_strategy(self, start_date, end_date, days, strategy, tickers):

        """
        Returns a dataframe of each of the stocks. If stock is not in top_pct, return is 0 else return is the return of the stock.
        """
        data = self.get_data_for_all_tickers(start_date, end_date, tickers)

        returns = self.calculate_returns(start_date, days, strategy, data, tickers)

        num_top_stocks = len(tickers)


        if strategy == 'M':  # selection of the top stocks based on the strategy type
            selected_stocks = heapq.nlargest(num_top_stocks, returns, key=returns.get)  # sorts the dict key value pairs of the top stocks
        elif strategy == 'R':  # selection of the bottom stocks based on the strategy type
            selected_stocks = heapq.nsmallest(num_top_stocks, returns, key=returns.get)  # sorts the dict key value pairs of the bottom stocks

        print(selected_stocks)

        # Create a DataFrame with all the stocks and their returns initialized to 0
        stock_returns_df = pd.DataFrame(data={'Stock': tickers, 'Return': [0] * len(tickers)})

        # Update the returns for the stocks selected based on the top_pct criteria
        for stock in selected_stocks:
            stock_returns_df.loc[stock_returns_df['Stock'] == stock, 'Return'] = returns[stock]

        return stock_returns_df
    





    def actual_performance(self, start_date, end_date):
        backtest_data = self.run_strategy(self.start_date, self.end_date, self.days, self.strategy, self.tickers)
        stocks_list = []
        for index, row in backtest_data.iterrows():
            if row['Return'] > 0:
                stocks_list.append(row['Stock'])

        start_date_formatted = datetime.strptime(start_date, "%Y%m%d").strftime("%Y-%m-%d")
        end_date_formatted = datetime.strptime(end_date, "%Y%m%d").strftime("%Y-%m-%d")

        stock_returns = []

        for stock in stocks_list:
            stock_data = yf.download(stock, start=start_date_formatted, end=end_date_formatted)
            
            if not stock_data.empty:
                stock_return = (stock_data['Close'][-1] - stock_data['Close'][0])/stock_data['Close'][0]
                stock_returns.append({'Stock': stock, 'Return': stock_return})

        result_df = pd.DataFrame(stock_returns, columns=['Stock', 'Return'])
        
        return result_df



        
        
if __name__ == '__main__':
    tickers = ['AMZN', 'AAPL', 'SPY', 'NFLX']
    start_date = '20230112'
    end_date = '20230212'
    days = 10
    strategy_type = 'M'
    top_pct = 50

    strategy_obj = Strategy(tickers, start_date, end_date, days, strategy_type, top_pct)
    result = strategy_obj.run_strategy(start_date, end_date, days, strategy_type, tickers)
    result_1 = strategy_obj.actual_performance(start_date, end_date)
    print(result_1)   

        



