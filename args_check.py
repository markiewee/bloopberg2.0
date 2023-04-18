import pandas_market_calendars as mcal
from datetime import datetime
import pandas as pd
import sys

class ArgsCheck:
    """
    Uses Pandas Market Calendars to get a list of trading dates without needing to call 
    the yfinance api. Used to check the arguments.
    """
    def date_check(start_date, end_date):
        """
        Checks the start and end date
        """ 
        if (start_date == None or end_date == None):
            sys.exit('Error: No beginning or end date provided.')
            
        if start_date > end_date:
            sys.exit('Error: Start date after end date. Enter a start date before or equal to the end date.')
        else:
            try:
                date_1 = datetime.strptime(start_date, '%Y%m%d').date()
                date_2 = datetime.strptime(end_date, '%Y%m%d').date()
            except ValueError:

                """
                If user enters date in an invalid format, print an error and exit the program.

                Example case: start_date = 203/20/299. Then the try statement will fail, so print error.
                """

                sys.exit('Error: Dates entered in invalid format.')


            today = datetime.today().date()
            
            """
            Now we get today's date e.g. 2023-03-14 such that we can check whether the start date is valid.
            
            """
            if date_1 > today:
                sys.exit('Error: Start date is in the future.')
            else:
                nyse = mcal.get_calendar('NYSE')
                
                """
                Use pandas mcal to get the trading days for the NYSE exchange 
                (since we are using predominantly US stocks)
                
                """

                if date_2 <= today:
                    try:
                        #Get trading days in a df between provided start and end date
                        df_trading_days = nyse.schedule(date_1,date_2)
                    
                    except pd.errors.OutOfBoundsDatetime:

                        """
                        An error here indicates that the user probably put in the start and/or end dates
                        way before the stock market existed in its current form.

                        e.g. start_date = 100/01/01 and end_date = 500/01/01 will return this error.

                        Say that the dates are out of bounds, and exit.
                        """

                        sys.exit('Error: Dates out of bounds.')

                    if len(df_trading_days) == 0:

                        """
                        If the provided dates don't result in an error, but the length of the dataframe is 0,
                        then no trading days were found. Then, print an error saying there were no trading
                        days found for the specified period.
                        """
                        sys.exit('Error: No trading days found for specified period.')
                    
                    else:
                        #Otherwise the function passes because there are valid dates.
                        return 1
                else:
                    """
                    This is if the end date is in the future.
                    """
                    try:
                        #Get trading days between the start date and today.
                        df_trading_days = nyse.schedule(date_1, today)

                    except pd.errors.OutOfBoundsDatetime:

                        """
                        An error here indicates that the user probably put in the start and/or end dates
                        way before the stock market existed in its current form.

                        e.g. start_date = 100/01/01 and end_date = 5000/01/01 will return this error.

                        Say that the dates are out of bounds, and exit.
                        """
                        sys.exit('Error: Dates out of bounds.')

                    if len(df_trading_days) == 0:
                        """
                        If the provided dates don't result in an error, but the length of the dataframe is 0,
                        then no trading days were found. Then, print an error saying there were no trading
                        days found for the specified period.
                        """

                        sys.exit('Error: No trading days found for specified period.')
                    
                    else:
                        #Otherwise the function passes because there are valid dates.
                        return 1
    
    def aum_check(aum):
        """
        Checks that the user input for initial_aum is greater than 0.
        """
        if aum == None:
            sys.exit('Error: Enter a valid AUM.') 
        if aum <= 0:
            sys.exit('Error: Initial AUM must be greater than 0.')

    def strategy_check(strategy):
        """
        Checks that the strategy provided is either 'M' or 'R'.
        """
        if strategy not in ['M', 'R']:
            sys.exit("Error: Strategy must be M or R (momentum or reversal).")
    
    def ticker_check(list):
        if list == None:
            sys.exit("Error: Please provide at least one ticker.")