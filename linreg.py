import yfinance as yf
import pandas as pd
from datetime import datetime
from datetime import timedelta
from sklearn.linear_model import LinearRegression
import stock_strategy
import pandas_market_calendars as mcal

class Linreg:

    def __init__(self, tickers, start_date, end_date, days_1, days_2, strategy_1, strategy_2, top_pct,aum):
        self.tickers = tickers
        self.strategy_1 = strategy_1
        self.strategy_2 = strategy_2
        self.days_1 = days_1
        self.days_2 = days_2
        self.aum = aum

        self.start_date = start_date
        self.end_date = end_date
        self.top_pct = top_pct
        self.Strategy = stock_strategy.Strategy(tickers, start_date, end_date, 10, "M",top_pct)

    def merge_data(self):
        """Merges momentum and reversal data frames for each stock."""
        ticker_data = self.Strategy.get_data_for_all_tickers(self.start_date, self.end_date, self.tickers)

        strategy_1_returns_df = self.Strategy.run_strategy(self.start_date, self.end_date, self.days_1, self.strategy_1, self.tickers)
        strategy_2_returns_df = self.Strategy.run_strategy(self.start_date, self.end_date, self.days_2, self.strategy_2, self.tickers)


        merged_df = pd.merge(strategy_1_returns_df,strategy_2_returns_df, on='Stock', how='inner')
        

        actual_performance = self.Strategy.actual_performance(self.start_date, self.end_date)
        merged_df = pd.merge(merged_df, actual_performance, on='Stock', how='inner')

        merged_df = merged_df.rename(columns={'Return_x': 'Return_strategy_1', 'Return_y': 'Return_strategy_2', 'Return': 'Return_actual'})

        #print(merged_df)

        return merged_df
    
    def predict_performance(self, X_train, y_train, X_test):
        # Fit a linear regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predict stock returns
        predicted_returns = model.predict(X_test)
        return predicted_returns
    


    def perform_strategy(self):
        """Fits a multiple linear regression model to predict stock returns and selects the top stocks based on the --top_pct score."""
        nyse = mcal.get_calendar('NYSE')
        schedule = nyse.schedule(start_date=self.start_date, end_date=self.end_date)
        last_trading_days = schedule.resample('M', closed='right', label='right').last().index

        aum = self.aum

        for i in range(len(last_trading_days) - 1):
            current_month_start = last_trading_days[i].strftime('%Y%m%d')
            current_month_end = last_trading_days[i + 1].strftime('%Y%m%d')
            prev_month_start = (last_trading_days[i] - pd.DateOffset(months=1)).strftime('%Y%m%d')


            # Get data for previous and current months
            prev_month_data = self.Strategy.get_data_for_all_tickers(prev_month_start, current_month_start, self.tickers)
            current_month_data = self.Strategy.get_data_for_all_tickers(current_month_start, current_month_end, self.tickers)

            # Run strategies for previous and current months
            prev_month_strat1 = self.Strategy.run_strategy(prev_month_start, current_month_start, self.days_1, self.strategy_1, self.tickers)
            prev_month_strat2 = self.Strategy.run_strategy(prev_month_start, current_month_start, self.days_2, self.strategy_2, self.tickers)
            current_month_strat1 = self.Strategy.run_strategy(current_month_start, current_month_end, self.days_1, self.strategy_1, self.tickers)
            current_month_strat2 = self.Strategy.run_strategy(current_month_start, current_month_end, self.days_2, self.strategy_2, self.tickers)

            # Merge data
            prev_month_merged = pd.merge(prev_month_strat1, prev_month_strat2, on='Stock', how='inner')
            prev_month_actual_performance = self.Strategy.actual_performance(prev_month_start, current_month_start)
            prev_month_merged = pd.merge(prev_month_merged, prev_month_actual_performance, on='Stock', how='inner')
            prev_month_merged = prev_month_merged.rename(columns={'Return_x': 'Return_strategy_1', 'Return_y': 'Return_strategy_2', 'Return': 'Return_actual'})

            current_month_merged = pd.merge(current_month_strat1, current_month_strat2, on='Stock', how='inner')
            current_month_actual_performance = self.Strategy.actual_performance(current_month_start, current_month_end)
            current_month_merged = pd.merge(current_month_merged, current_month_actual_performance, on='Stock', how='inner')
            current_month_merged = current_month_merged.rename(columns={'Return_x': 'Return_strategy_1', 'Return_y': 'Return_strategy_2', 'Return': 'Return_actual'})

            # Prepare the data for the regression model
            X_train = prev_month_merged[['Return_strategy_1', 'Return_strategy_2']]
            y_train = prev_month_merged['Return_actual']
            X_test = current_month_merged[['Return_strategy_1', 'Return_strategy_2']]

            # Predict stock returns using the linear regression model
            predicted_returns = self.predict_performance(X_train, y_train, X_test)
            current_month_merged['Predicted_Return'] = predicted_returns

            top_stocks = self.Strategy.compute_top_stocks(self.top_pct)
            sorted_df = current_month_merged.sort_values(by='Predicted_Return', ascending=False)
            top_pct_df = sorted_df.head(top_stocks)
            # Store the top-performing stocks for each month
            if i == 0:
                all_top_stocks = top_pct_df
            else:
                all_top_stocks = all_top_stocks.append(top_pct_df, ignore_index=True)
            # Calculate average return and update AUM
            average_return = top_pct_df['Return_actual'].mean()
            aum = (aum * (1 + average_return))

        return aum, all_top_stocks

    
    

        

import matplotlib.pyplot as plt

# Replace these parameters with your own values
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
start_date = '20210105'
end_date = '20211228'
days_1 = 30
day_2 =60
strategy_1 = 'M'
strategy_2 = 'R'
top_pct = 30
aum = 100000

# Create an instance of the Linreg class
linreg = Linreg(tickers, start_date, end_date, days_1, day_2, strategy_1, strategy_2, top_pct,aum)


updated_aum, top_stocks = linreg.perform_strategy()
print(updated_aum)

# Plot the graph comparing the actual and predicted returns of the top stocks
fig, ax = plt.subplots()
x_labels = top_stocks['Stock'].unique().tolist()
actual_returns = top_stocks.groupby('Stock')['Return_actual'].mean()
predicted_returns = top_stocks.groupby('Stock')['Predicted_Return'].mean()
ax.bar(x_labels, actual_returns, label='Actual', alpha=0.5, color='b')
ax.bar(x_labels, predicted_returns, label='Predicted', alpha=0.5, color='r')
ax.set_xlabel('Stocks')
ax.set_ylabel('Returns (%)')
ax.set_title('Comparison of Actual and Predicted Returns')
ax.legend(loc='best')

plt.show()