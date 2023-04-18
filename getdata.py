import yfinance as yf
import pandas as pd
from parseargs import ParseArgs
from datetime import datetime
from datetime import timedelta


class Getdata:
    """
    A class to get financial data for a given stock ticker using the yfinance library.

    Attributes:
        start_date (datetime): The start date for the data retrieval period.
        end_date (datetime): The end date for the data retrieval period.
        ticker (str): The stock ticker symbol for the desired data.
    """

    def __init__(self, start_date, end_date, ticker):
        """
        Initializes the Getdata class with the given start_date, end_date, and ticker.

        Args:
            start_date (str): The start date as a string in the format YYYYMMDD.
            end_date (str): The end date as a string in the format YYYYMMDD.
            ticker (str): The stock ticker symbol for the desired data.
        """
        self.start_date = datetime.strptime(start_date, '%Y%m%d')
        self.end_date = datetime.strptime(end_date, '%Y%m%d')
        self.ticker = ticker

    def getdata(self):
        """
        Retrieves and returns one stock's data from the yfinance API for the specified period.

        Returns:
            data (pd.DataFrame): A DataFrame containing the stock data for the given period.
        """
        ticker_data = yf.Ticker(self.ticker)

        # Get historical price data
        price_data = ticker_data.history(start=self.start_date, end=self.end_date)
        price_data = price_data.reset_index()[['Date', 'Close']]

        # Get dividend data
        dividend_data = ticker_data.dividends
        dividend_data = pd.DataFrame(dividend_data).reset_index()
        dividend_data.columns = ['Date', 'Dividends']

        # Merge price and dividend data
        data = pd.merge(price_data, dividend_data, on='Date', how='left').fillna(0)

        return data

    def buy_sell_dates(self):
        """
        Returns a list of the last trading days of each month within the specified date period.

        Returns:
            monthly_final_trading_days (list): A list of the last trading days of each month.
        """
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        data = pd.DataFrame(data)
        trading_dates = data.index
        series_trading_dates = pd.Series(trading_dates)
        monthly_final_trading_days = series_trading_dates.groupby(series_trading_dates.dt.strftime('%Y-%m')).max().tolist()
        return monthly_final_trading_days

    def get_first_last_trading_days(self):
        """
        Returns the first and last trading days within the specified date period.

        Returns:
            list: A list containing the first and last trading days as pandas Timestamp objects.
        """
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        data = pd.DataFrame(data)
        trading_dates = data.index
        return [trading_dates[0], trading_dates[-1]]


if __name__ == '__main__':
    start_date = '20200101'
    end_date = '20201231'
    ticker = 'DVN'

    data_obj = Getdata(start_date, end_date, ticker)
    data_df = data_obj.getdata()
    print(data_df)
