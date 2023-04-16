from getdata import Getdata
from parseargs import Parseargs
from calculatedata import CalculateData
from datetime import datetime, timedelta, date
import math
import heapq
import pandas as pd
import numpy as np

"""
This is the main file to run the program. Sample input below: 

python3 strategy.py --tickers AAPL MSFT HD VZ PG KO --b 20180101 --e 20220314 --initial_aum 1000000 --strategy_type M --days 30 --top_pct 20
"""

class Strategy:
    def __init__(self, stocks, start_day, end_day, aum, strategy_type,n_days, top_pct):
        assert isinstance(stocks, list), "Stocks must be a list"
        assert isinstance(start_day, str), "Start day must be a string"
        assert isinstance(end_day, str), "End day must be a string"
        assert isinstance(top_pct, int), "Top percentile must be an integer" #change back to int
        assert isinstance(n_days, int), "Number of days must be an integer"
        assert n_days <= 250, "Number of days must be less than or equal to 250"
        assert isinstance(aum, float), "AUM must be a floats"
        assert aum > 0, "AUM must be greater than 0"
        assert top_pct > 0, "Top percentile must be greater than 0"
        assert top_pct <= 100, "Top percentile must be less than or equal to 100"
        assert len(start_day) == 8, "Start day must be in YYYYMMDD format"
        assert len(end_day) == 8, "End day must be in YYYYMMDD format"
        assert start_day < end_day, "Start day must be before end day"
        assert len(stocks) > 0, "Stocks must be a non-empty list"
        assert strategy_type in ["M", 'R'], "Strategy type must be momentum or reversal"

        self.stocks = stocks
        self.start_day = start_day
        self.end_day = end_day
        self.top_pct = top_pct
        self.n_days = n_days 
        self.aum = aum
        self.strategy_type = strategy_type
        self.lookback = 20
        self.stock_data = {}

    def strategy(self):
        """
        Computes the AUM for each buy-sell interval for the provided dates.

        Returns a pandas dataframe with 2 columns: The AUM under 'AUM' and 
        the period as a string.
        """
        list_arguments = Parseargs().parse_arguments()  
        stocks = list_arguments[0]
        today = date.today()
        self.start_day = datetime.strptime(self.start_day, '%Y%m%d').date()
        self.end_day = datetime.strptime(self.end_day, '%Y%m%d').date()
        actual_start_day = Getdata(datetime.strftime(self.start_day,"%Y%m%d"),list_arguments[2], stocks[0]).getdata().index[0] #first trading day
        data_collection_start_date = self.start_day - timedelta(days=400) # 400 days of data for lookback
        for stock in stocks:
            self.stock_data[stock] = Getdata(datetime.strftime(data_collection_start_date,"%Y%m%d"),list_arguments[2], stock).getdata()

        if self.strategy_type == 'M':
            self.lookback = 20
        else:
            self.lookback = 0

        backtest_start_date = self.backdate(actual_start_day, (self.lookback+self.n_days))
        backtest_end_date = self.backdate(actual_start_day, self.lookback)

        performance_df = pd.DataFrame(columns = ['AUM', 'Period'])

        if (self.end_day > today):
            buy_sell_days = Getdata(
                                list_arguments[1], 
                                datetime.strftime(today,"%Y%m%d"), #Use today's date 
                                stocks[0] #Get the first stock in the list
                                ).buy_sell_dates() #Returns a list of the last trading days of each month given a valid date period.
        else:
            buy_sell_days = Getdata(
                                list_arguments[1], 
                                datetime.strftime(self.end_day,"%Y%m%d"), #Use the input end date
                                stocks[0] #Get the first stock in the list
                                ).buy_sell_dates() #Returns a list of the last trading days of each month given a valid date period.
        
        
        
        initial_stocks = self.backtest(backtest_start_date, backtest_end_date, stocks)#intial backtest
        
        """
        Iterative walk forward investing where we buy the top stocks 
        from the previous backtest period and sell at the end of month
        returns a dataframe of the AUM and the period
        """
        aum = self.aum #initial AUM

        for i in range(len(buy_sell_days)-2): #here the -2 is special because the length of the list is 1 more than the number of elements which start at index 0 and the number of periods is one less than the number of elements
            aum_per_stock = aum / len(initial_stocks)#AUM per stock
            stocks_pct_returns = self.compute_returns(buy_sell_days[i], buy_sell_days[i+1], initial_stocks) #computes percentage returns for each stock
            stock_return_values = [] #empty list to append actual returns
            for value in stocks_pct_returns.values():#iterates through the dictionary
                stock_return_values.append(value)#appends the percentage returns to the list
            for j in range (len(stock_return_values)):#iterates through the list
                stock_return_values[j]=(aum_per_stock *(1 + stock_return_values[j]))#multiplies the AUM per stock by the percentage return to get actual return value
            period = str(buy_sell_days[i]) + " to " + str(buy_sell_days[i+1])#period string
            aum = np.sum(stock_return_values)#sums the actual return values to get the new AUM
            performance_df.loc[i] = [aum, period]#adds the new AUM and period to the dataframe
            """
            Here we will look at the top stocks from the new backtest period
            """
            new_backtest_start_date = self.backdate(buy_sell_days[i+1],(self.lookback+self.n_days))#gets the new backtest start date
            initial_stocks = self.backtest(new_backtest_start_date, buy_sell_days[i+1], stocks)#new backtest
        
        results = performance_df #Store a dataframe with the AUM for the period.

        return results



    def compute_top_stocks (self):
        """
        Computes the number of top stocks based on top_pct and rounds up to nearest integer.
        """
        num_stocks = len(self.stocks)#number of stocks in the list
        num_top_stocks = math.ceil(num_stocks * self.top_pct / 100)#number of top stocks based on top_pct and rounded up to nearest integer
        return num_top_stocks


    def compute_returns (self, start_day, end_day, tickers):
        """
        Computes the returns for each stock in the list of stocks for a given period.
        Returns a dictionary of the stock and the percentage change over the given period.
        """
        start_day = datetime.strftime(start_day,"%Y-%m-%d")
        end_day = datetime.strftime(end_day,"%Y-%m-%d")
        returns = {} #Create an empty dictionary
        for ticker in tickers:
            df =self.stock_data[ticker]
            start_price = df.loc[start_day, 'Adj Close']
            end_price = df.loc[end_day, 'Adj Close']
            pct_change = (end_price - start_price) / start_price
            returns[ticker] =pct_change
        return returns
    

    def backtest (self, backtest_start_date, backtest_end_date, stocks):
        """
        Backtest function that computes the top stocks based on the 
        backtest_start_date, backtest_end_date, stocks and top percentage.
        returns a list of the top stocks.
        """
        self.backtest_start_date = backtest_start_date
        self.backtest_end_date = backtest_end_date
        self.stocks = stocks
        number_of_top_stocks = self.compute_top_stocks() #uses the value of top_pct to compute the number of top stocks
        backtest_data = self.compute_returns(backtest_start_date, backtest_end_date, stocks)# returns a dict of the given ticker and percentage change over given time period
        if self.strategy_type == 'M': #selection of the top stocks based on the strategy type
            stock_returns= heapq.nlargest(number_of_top_stocks, backtest_data, key=backtest_data.get)# sorts the dict key value pairs of the top stocks
        elif self.strategy_type == 'R': #selection of the bottom stocks based on the strategy type
            stock_returns = heapq.nsmallest(number_of_top_stocks, backtest_data, key=backtest_data.get)# sorts the dict key value pairs of the bottom stocks
        top_tickers_backtest = [] # empty list to store the tickers of the top stocks (key of backtest_data)
        for key in stock_returns: #iterates through the top stocks and appends the ticker to the list
            top_tickers_backtest.append(key)
        return top_tickers_backtest
    
    def backdate (self, original_date, trading_days):
            generic_df = next(iter(self.stock_data.values())) #returns the first dataframe
            row_number = generic_df.index.get_loc(original_date) #gets the row number of the given date
            start_date = generic_df.index[row_number - trading_days] #gets the new backtest start date
            return start_date

if __name__ == '__main__':
    list_arguments = Parseargs().parse_arguments() 
    #print(list_arguments)
    obj = Strategy(list_arguments[0], 
                           list_arguments[1], 
                           list_arguments[2], 
                           list_arguments[3], 
                           list_arguments[4], 
                           list_arguments[5],
                           list_arguments[6])
    results = obj.strategy()

    CalculateData().print_data(initial_aum = obj.aum, final_aum = results['AUM'].iloc[-1], df = results)