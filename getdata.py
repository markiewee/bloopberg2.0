import yfinance as yf
import pandas as pd
from parse_args import Parseargs
from datetime import datetime

class Getdata:
    """
    Uses yfinance to get data of a given ticker.
    """
    def __init__(self, start_date, end_date, ticker):
        self.start_date =datetime.strptime(start_date, '%Y%m%d')
        self.end_date =datetime.strptime(end_date, '%Y%m%d')     
        self.ticker = ticker
        self.data = self.getdata()

    def getdata(self):
        """
        Returns one stock's data from the yf API for the period specified.
        """
        data = yf.download(self.ticker, start = self.start_date, end = self.end_date)
        data = pd.DataFrame(data)
        return data
    
    def buy_sell_dates(self):
        """
        Returns a list of the last trading days of each month given a valid date period.
        """
        trading_dates = self.data.index
        series_trading_dates = pd.Series(trading_dates)
        monthly_final_trading_days = series_trading_dates.groupby(series_trading_dates.dt.strftime('%Y-%m')).max().tolist()
        return monthly_final_trading_days

    def get_first_last_trading_days(self):
        """
        Gets first and last trading period for the Getdata object's period.
        """
        trading_dates = self.data.index
        return [trading_dates[0], trading_dates[-1]]

if __name__ == '__main__':
    list_arguments = Parseargs().parse_arguments()
    print(list_arguments)
    
    