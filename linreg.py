import yfinance as yf
import pandas as pd
from datetime import datetime
from datetime import timedelta
from sklearn.linear_model import LinearRegression
import stock_strategy

class Linreg:

    def __init__(self, tickers, start_date, end_date, days, strategy, top_pct):
        self.tickers = tickers
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.days = days
        self.top_pct = top_pct
        self.Strategy = stock_strategy.Strategy(tickers, start_date, end_date, days, strategy, top_pct)

    def merge_data(self):
        """Merges momentum and reversal data frames for each stock."""
        ticker_data = self.Strategy.get_data_for_all_tickers(self.start_date, self.end_date, self.tickers)

        momentum_returns_df = self.Strategy.run_strategy(self.start_date, self.end_date, self.days, 'M', self.tickers)
        reversal_returns_df = self.Strategy.run_strategy(self.start_date, self.end_date, self.days, 'R', self.tickers)

        merged_df = pd.merge(momentum_returns_df, reversal_returns_df, on='Stock', how='inner')
        merged_df = merged_df.rename(columns={'Return_x': 'Return_momentum', 'Return_y': 'Return_reversal'})
        print(merged_df)

        return merged_df

    def predict_performance(self):
        # Merge momentum and reversal data frames
        merged_df = self.merge_data()

        # Get actual performance
        actual_performance = self.Strategy.actual_performance(self.start_date, self.end_date)

        # Merge actual performance with merged_df
        data = pd.merge(merged_df, actual_performance, on='Stock', how='inner')
        
        # Split the dataset into features (X) and target (y)
        X = data[['Return_momentum', 'Return_reversal']]
        y = data['Return']

        # Fit a linear regression model
        model = LinearRegression()
        model.fit(X, y)

        # Predict stock returns
        predicted_returns = model.predict(X)
        data['Predicted_Return'] = predicted_returns

        return data

    def perform_strategy(self):
        """Fits a multiple linear regression model to predict stock returns and selects the top stocks based on the --top_pct score."""

        # Predict stock returns using the linear regression model
        predicted_data = self.predict_performance()

        # Select the top stocks based on the predicted returns
        top_stocks = predicted_data.nlargest(int(len(predicted_data) * self.top_pct), 'Predicted_Return')

        return top_stocks

import matplotlib.pyplot as plt

# Replace these parameters with your own values
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
start_date = '20210105'
end_date = '20211228'
days = 30
strategy = 'M'
top_pct = 0.5

# Create an instance of the Linreg class
linreg = Linreg(tickers, start_date, end_date, days, strategy, top_pct)

# Perform the strategy and get the top stocks
top_stocks = linreg.perform_strategy()
print(top_stocks)

# Plot the graph comparing the actual and predicted returns of the top stocks
fig, ax = plt.subplots()
x_labels = top_stocks['Stock'].tolist()
ax.bar(x_labels, top_stocks['Return'], label='Actual', alpha=0.5, color='b')
ax.bar(x_labels, top_stocks['Predicted_Return'], label='Predicted', alpha=0.5, color='r')
ax.set_xlabel('Stocks')
ax.set_ylabel('Returns (%)')
ax.set_title('Comparison of Actual and Predicted Returns')
ax.legend(loc='best')

plt.show()