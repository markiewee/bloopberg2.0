import pandas as pd
import numpy as np
import math
import functools

class StockStrategy:
    def __init__(self, start_date, end_date, stock_data_frames):
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.stock_data_frames = stock_data_frames

    def calculate_momentum(self, lookback_period=12):
        momentum_list = []

        for df in self.stock_data_frames:
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            df = df.loc[self.start_date:self.end_date]
            df['adjusted_price'] = df['price'] - df['dividend']
            df['return'] = df['adjusted_price'].pct_change()
            df['momentum'] = df['adjusted_price'].shift(1) / df['adjusted_price'].shift(1 + lookback_period) - 1
            df = df.reset_index()
            momentum_list.append(df)

        return momentum_list

    def calculate_reversal(self, formation_period=12, holding_period=1):
        reversal_list = []

        for df in self.stock_data_frames:
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            df = df.loc[self.start_date:self.end_date]
            df['adjusted_price'] = df['price'] - df['dividend']
            df['return'] = df['adjusted_price'].pct_change()
            df['rolling_return'] = df['return'].rolling(window=formation_period).sum()
            df['reversal'] = -df['rolling_return'].shift(holding_period)
            df = df.reset_index()
            reversal_list.append(df)

        return reversal_list

    def select_top_stocks(self, stock_data_list, top_pct):
        merged_df = functools.reduce(lambda left, right: pd.merge(left, right, on='date', how='outer'), stock_data_list)
        merged_df.set_index('date', inplace=True)

        col_list = [col for col in merged_df.columns if 'momentum' in col or 'reversal' in col]
        merged_df['top_stock'] = merged_df[col_list].apply(
            lambda x: x.nlargest(math.ceil(len(col_list) * top_pct / 100)).idxmin(), axis=1
        )

        top_stocks_list = []
        for df in stock_data_list:
            df = df.set_index('date')
            col = list(set(df.columns).intersection(set(merged_df['top_stock'].unique())))[0]
            if col:
                top_stock_df = df.loc[merged_df['top_stock'] == col]
                top_stocks_list.append(top_stock_df.reset_index())

        return top_stocks_list
