import pandas as pd
from getdata import Getdata
from parseargs import Parseargs
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt


class CalculateData:
    """
    Class which contains several methods for the final statistics computations.
    """
    def __init__(self):
        """
        When this object is initialised, it automatically parses arguments and 
        gets the first and last trading days, storing them as attributes.
        """
        self.list_arguments = Parseargs().parse_arguments() 
        list_first_last_trading_days = Getdata(self.list_arguments[1], self.list_arguments[2], self.list_arguments[0][0]).get_first_last_trading_days()
        self.start_day = list_first_last_trading_days[0]
        self.end_day = list_first_last_trading_days[1]
    
    def get_num_days(self):
        """
        this object returns the number of days by calculating the days between the end date and the start date
        """
        days_delta = self.end_day - self.start_day
        return days_delta.days
    
    def get_total_return(self,initial_aum, final_aum):
        """
        this object returns the total return of the AUM invested by using data from initial and final AUM of the stock. 
        """
        return 100*(final_aum - initial_aum) / initial_aum

    def get_annualized_rate_of_return(self, initial_aum, final_aum):
        """
        this object returns annualized rate of return by using data from total return and number of days as input and calculating them to get the rate of return in a yearly basis. 
        """
        total_return = self.get_total_return(initial_aum, final_aum)
        years = self.get_num_days() / 365.25
        return ((1 + (total_return / 100)) ** (1 / years) - 1) * 100

    def get_final_AUM(self,df):
        """
        returns the final AUM
        """
        return df['AUM'][-1]

    def get_average_daily_AUM(self,df):
        """
        returns the mean of the AUMs in the dataframe as the average daily AUM
        """
        return df['AUM'].mean()
    
    def get_maximum_daily_AUM(self,df):
        """
        Returns the maximum data in the AUM dataframe as the maximum daily AUM
        """
        return df['AUM'].max() 
     
    def get_pnl(self,initial_aum, final_aum):
        """
        computes profit and loss by calculating the difference between final and initial aum
        """
        pnl = final_aum - initial_aum
        return pnl
    
    def get_daily_returns(self, df):
        """
        Returns a pandas series of daily returns for the given AUM dataframe.
        """
        return df['AUM'].pct_change()

    def get_average_daily_return(self, df):
        """
        Returns the average daily return.
        """
        daily_returns = self.get_daily_returns(df)
        return daily_returns.mean()

    def get_std_daily_return(self, df):
        """
        Returns the standard deviation of daily returns.
        """
        daily_returns = self.get_daily_returns(df)
        return daily_returns.std()

    def get_sharpe_ratio(self, df, risk_free_rate=0.02):
        """
        Returns the Sharpe ratio given the AUM dataframe and risk-free rate.
        """
        avg_daily_return = self.get_average_daily_return(df)
        std_daily_return = self.get_std_daily_return(df)
        return (avg_daily_return - risk_free_rate) / std_daily_return

    def get_monthly_cumulative_ic(self, df):
        """
        Returns a pandas series of monthly cumulative Information Coefficient (IC).
        """
        daily_returns = self.get_daily_returns(df)
        daily_returns = daily_returns.dropna()
        daily_returns.index = pd.to_datetime(daily_returns.index)
        monthly_returns = daily_returns.resample('M').sum()
        cumulative_ic = monthly_returns.cumsum()
        return cumulative_ic
    
    def plot_data(self, df):
        """
        Plots daily AUM and monthly cumulative IC.
        """
        # Daily AUM plot
        df['AUM'].plot(title='Daily AUM', xlabel='Date', ylabel='AUM', grid=True)
        plt.show()

        # Monthly cumulative IC plot
        monthly_cumulative_ic = self.get_monthly_cumulative_ic(df)
        monthly_cumulative_ic.plot(title='Monthly Cumulative Information Coefficient (IC)', xlabel='Date', ylabel='IC', grid=True)
        plt.show()




    def print_data(self,initial_aum, final_aum, df):
        """
        Prints all the statistics needed
        """
        print('Begin date is', self.start_day)
        print('End date is', self.end_day)
        print('Number of days is', self.get_num_days())
        print('Total stock return:', self.get_total_return(initial_aum, final_aum), '%')
        print('Total return:', self.get_total_return(initial_aum, final_aum), '%')
        print('Annualized rate of return:', self.get_annualized_rate_of_return(initial_aum, final_aum), '%')
        print('Initial AUM:', initial_aum)
        print('Final AUM:', final_aum)
        print('Average daily AUM:', self.get_average_daily_AUM(df))
        print('Maximum AUM', self.get_maximum_daily_AUM(df))
        print('Profit and Loss:', self.get_pnl(initial_aum, final_aum))
        print('Sharpe ratio:', self.get_sharpe_ratio(df))
        print('Average daily return:', self.get_average_daily_return(df))
        self.plot_data(df)


    @staticmethod
    def generate_random_data():
        """
        Generates random AUM data for demonstration purposes. Only for if this is run 
        as the main file and for debugging purposes.
        """
        date_range = pd.date_range(start='2020-01-01', end='2022-12-31', freq='B')
        aum = np.random.randint(1000, 2000, size=len(date_range)) + np.random.random(size=len(date_range))
        df = pd.DataFrame({'AUM': aum}, index=date_range)
        return df

if __name__ == "__main__":
    # Initialize the CalculateData object
    calc_data = CalculateData()

    # Generate random AUM data for demonstration purposes
    df = calc_data.generate_random_data()

    # Get the initial and final AUM values
    initial_aum = df['AUM'][0]
    final_aum = calc_data.get_final_AUM(df)

    # Print the results
    calc_data.print_data(initial_aum, final_aum, df)


        
