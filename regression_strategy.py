import pandas as pd
import numpy as np
import math
import functools
from sklearn.linear_model import LinearRegression



class RegressionStrategy:
    """
    A class to perform a multiple linear regression strategy based on momentum and reversal features.

    Attributes
    ----------
    momentum_list : list of pd.DataFrame
        A list of data frames containing the momentum data calculated by StockStrategy.
    reversal_list : list of pd.DataFrame
        A list of data frames containing the reversal data calculated by StockStrategy.
    top_pct : int
        An integer from 1 to 100 indicating the percentage of stocks to select with the highest score.

    Methods
    -------
    perform_strategy():
        Fits a multiple linear regression model to predict stock returns and selects the top stocks
        based on the --top_pct score.
    """

    def __init__(self, momentum_list, reversal_list, top_pct):
        self.momentum_list = momentum_list
        self.reversal_list = reversal_list
        self.top_pct = top_pct

    def _merge_data(self):
        """Merges momentum and reversal data frames for each stock."""
        merged_list = []

        for mom_df, rev_df in zip(self.momentum_list, self.reversal_list):
            merged_df = mom_df.merge(rev_df[['date', 'reversal']], on='date')
            merged_list.append(merged_df)

        return merged_list

    def _fit_regression_model(self, merged_data, current_month):
        """
        Fits a multiple linear regression model using the data up to the previous month.

        Parameters
        ----------
        merged_data : list of pd.DataFrame
            A list of data frames containing the merged momentum and reversal data for each stock.
        current_month : pd.Timestamp
            A Timestamp object representing the current month.
        """
        previous_month = current_month - pd.DateOffset(months=1)
        features = []
        labels = []

        for df in merged_data:
            df = df.set_index('date')
            prev_month_data = df.loc[:previous_month]
            current_month_data = df.loc[current_month]

            if not prev_month_data.empty and not current_month_data.empty:
                features.append(prev_month_data[['momentum', 'reversal']].values)
                labels.append(current_month_data['return'].values[0])

        X = np.vstack(features)
        y = np.array(labels)

        model = LinearRegression()
        model.fit(X, y)

        return model

    def perform_strategy(self):
        """
        Performs the multiple linear regression strategy and selects the top stocks based on the --top_pct score.
        """
        merged_data = self._merge_data()
        unique_dates = sorted(list(set([date for df in merged_data for date in df['date']])))
        top_stocks_history = []

        for i in range(1, len(unique_dates)):
            current_month = unique_dates[i]

            # Fit the regression model using data up to the previous month
            model = self._fit_regression_model(merged_data, current_month)

            scores = []
            for df in merged_data:
                df = df.set_index('date')
                current_month_data = df.loc[current_month]
                if not current_month_data.empty:
                    current_features = current_month_data[['momentum', 'reversal']].values.reshape(1, -1)
                    score = model.predict(current_features)[0]
                    scores.append((df.index.name, score))

            # Sort stocks based on their score and select the top stocks
            scores.sort(key=lambda x: x[1], reverse=True)
            top_stocks = scores[:math.ceil(len(scores) * self.top_pct / 100)]

            # Add the top stocks to the history list
            top_stocks_history.append((current_month, top_stocks))

        return top_stocks_history
